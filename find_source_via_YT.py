from jellyfish import jaro_similarity

import pandas as pd
import numpy as np
from tqdm import tqdm
import regex as re
import requests
from bs4 import BeautifulSoup
import json
import os


def check_desc(channel_id, videos_df, pattern):
    # Get up to the first 5 videos of a channel from videos_df
    videos_df = videos_df.loc[videos_df["channel_id"] == channel_id].reset_index().drop("index", axis=1).head()
    found = (False, np.nan)

    # For each video
    for i in range(0, videos_df.shape[0]):
        # Get description
        desc = repr(videos_df.iloc[i]["description"]).replace("\\n", " ").replace("  ", " ")
        # print(desc)

        # Using RegEx, find links using given pattern
        match = re.search(pattern, desc)
        if match is not None:
            if len(match.group()) >= 5:
                found = (True, match.group())

                # print(f"Found in video description: {match.group()}")

                break

    return found


def check_about_links(pattern, links):
    found = (False, np.nan)

    for i in range(0, len(links)):
        match = re.search(pattern, links[i][1])
        if match is not None:
            found = (True, match.group())

            # print(f"Found in About section: {match.group()}")

            # Remove found link to shorten search for succeeding calls of check_about_links
            links.pop(i)
            break

    return found, links


def find_sources_via_yt(channel_df, video_df):
    pbar = tqdm(total=channel_df.shape[0])
    pbar.set_description("Finding sources on YouTube...")

    source_check = []
    source_links = []
    cols = [
        "channel_id", "channel_name",
        "LinkedIn", "Wiki", "Website",
        "Twitter", "Facebook", "Instagram"
    ]

    # --- Patterns to search for links within About sections in channel pages and video descriptions
    website_pattern = r"(?<=(W|w)ebsite((\:\s)?|\sat\s))(http(s)?:|\w|[/_.-])+"
    fb_pattern = r"(https:\/\/www\.)?facebook\.com\/(\w|\w[-_/.-])+"
    linkedIn_pattern = r"(https:\/\/www\.)?linkedin\.com\/(company|in)\/(\w|[-_/.])+"
    twitter_pattern = r"(https:\/\/www\.)?twitter\.com\/(\w|\w[-_/])+"
    instagram_pattern = r"(https:\/\/www\.)?instagram\.com\/(\w|\w[-_/])+"
    # ---

    '''
    Iterate through a DataFrame of channels
    '''
    for i in range(0, channel_df.shape[0]):
        '''
        Wiki page will not be searched for via YT channel pages and video descriptions.
        This value will be updated on a separate function (searching via Google using CSE)
        '''
        wiki_found = (False, np.nan)

        channel_id = channel_df.iloc[i]["channel_id"]
        channel_name = channel_df.iloc[i]["channel_name"]

        # --- Checking descriptions from channel's videos
        linkedIn_found = check_desc(channel_id, video_df, linkedIn_pattern)
        site_found = check_desc(channel_id, video_df, website_pattern)
        fb_found = check_desc(channel_id, video_df, fb_pattern)
        twitter_found = check_desc(channel_id, video_df, twitter_pattern)
        instagram_found = check_desc(channel_id, video_df, instagram_pattern)
        # ---

        # --- Checking About section from channel pages
        about_page = requests.get(f'https://www.youtube.com/channel/{channel_id}/about')
        soup = BeautifulSoup(about_page.content, 'html.parser')
        script_tags = soup.find_all("script")

        for script in script_tags:
            results = re.search(r"var ytInitialData = {.*}", script.text)
            if results is not None:
                object = results.group(0).replace("var ytInitialData = ", "")
                try:
                    link_information = (json.loads(object)['onResponseReceivedEndpoints'][0]
                    ['showEngagementPanelEndpoint']
                    ['engagementPanel']
                    ['engagementPanelSectionListRenderer']
                    ['content']
                    ['sectionListRenderer']
                    ['contents'][0]
                    ['itemSectionRenderer']
                    ['contents'][0]
                    ['aboutChannelRenderer']
                    ['metadata']
                    ['aboutChannelViewModel']
                    ['links']
                    )
                except:
                    pass
                else:
                    # print("Available links provided for:", {channel_name})
                    links = []
                    for link in link_information:  # print all available links from the about modal
                        link_title = link['channelExternalLinkViewModel']['title']['content']
                        url = link['channelExternalLinkViewModel']['link']['content']
                        links.append([link_title, url])

                    # print(links)

                    '''
                    Use previously declared RegEx patterns to extract links
                    for Website, Facebook, Twitter, LinkedIn, and Instagram in a channel's About section
                    
                    Extracting official site link is given more priority
                    '''
                    if not site_found[0]:
                        for i in range(0, len(links)):
                            match = re.search(website_pattern, links[i][0])
                            if match is not None:
                                site_found = (True, links[i][1])
                                # print(site_found[1])
                                break

                        ''' This code block got false positives (i.e. App Store links for news
                        #   apps, with the name of the organization in the link title)
                        for i in range(0, len(links)):
                            link_title = links[i][0]
                            similarity = round(jaro_similarity(channel_name, link_title), 2)
                            if similarity >= 0.60:
                                match = re.search(r"youtube\.com\/.+", links[i][1])
                                if match is None:
                                    site_found = (True, links[i][1])
                                    print(site_found[1])
                                    break
                        '''
                    if not fb_found[0]:
                        fb_found, links = check_about_links(fb_pattern, links)

                    if not twitter_found[0]:
                        twitter_found, links = check_about_links(twitter_pattern, links)

                    if not linkedIn_found[0]:
                        linkedIn_found, links = check_about_links(linkedIn_pattern, links)

                    if not instagram_found[0]:
                        instagram_found, links = check_about_links(linkedIn_pattern, links)

        # Source checks ---
        sc_record = [
            channel_id,  # channel_id
            channel_name,  # channel_name
            linkedIn_found[0],
            wiki_found[0],
            site_found[0],
            twitter_found[0],
            fb_found[0],
            instagram_found[0]
        ]
        source_check.append(sc_record)
        # ---

        # Source links ---
        sl_record = [
            channel_id,
            channel_name,
            linkedIn_found[1],
            wiki_found[1],
            site_found[1],
            twitter_found[1],
            fb_found[1],
            instagram_found[1]
        ]
        source_links.append(sl_record)
        # ---
        pbar.update(1)

    pbar.close()

    if len(source_check) > 0:
        sc_nparray = np.array(source_check)
        sl_nparray = np.array(source_links)
        sc_df = pd.DataFrame(sc_nparray, columns=cols)
        sl_df = pd.DataFrame(sl_nparray, columns=cols)
    else:
        sc_df = pd.DataFrame(columns=cols)
        sl_df = pd.DataFrame(columns=cols)

    print("Source extracted from YouTube. Saving tentative checklists and links.")

    sc_df.to_csv("source_check.csv")
    sl_df.to_csv("source_links.csv")


def clean_links():
    checklist = pd.read_csv("source_check.csv", index_col=0)
    links = pd.read_csv("source_links.csv", index_col=0)
    df = links[links.columns[2:]]

    for i in range(df.shape[0]):
        for column in df.columns:
            if checklist.iloc[i][column]:
                link = df.iloc[i][column]

                # Add https:// to links
                if re.search(r'^https:\/\/', link) is None:
                    link = 'https://' + link

                # Remove . at the end of links to avoid Bad Request error
                link = re.sub(r'(?<=\w)\.$', '', link)

                # Change http to https
                link = re.sub(r'^http:\/\/', 'https://', link)

                if column == "Website":
                    if re.search(r'(https:\/\/www\.)?(facebook|twitter|instagram)\.com\/(\w|\w[-_/])+',
                                 link) is not None:
                        checklist.at[i, column] = False
                        links.at[i, column] = np.nan

                # Update link
                links.at[i, column] = link

    links.to_csv("source_links.csv")


if __name__ == '__main__':
    folder = input("Folder name: ")
    path = os.getcwd() + "/datasets/" + folder
    os.chdir(path)

    print("Reading list of channels...")
    channel_df = pd.read_csv("channels.csv", index_col=0)
    print("Reading list of videos...")
    video_df = pd.read_csv("videos.csv", index_col=0)

    find_sources_via_yt(channel_df, video_df)
    clean_links()

    os.chdir("..")
    os.chdir("..")
