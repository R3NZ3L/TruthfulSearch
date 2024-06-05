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

        # Using RegEx, find links using given pattern
        match = re.search(pattern, desc)
        if match is not None:
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
    website_pattern = r"(?<=(W|w)ebsite((\:)?\s|\sat\s))(\w|[:/.])+"
    fb_pattern = r"(https:\/\/www\.)?facebook\.com\/(\w|\w[-_/])+"
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

                    '''
                    Extracting official site link is given more priority
                    '''
                    if not site_found[0]:
                        for i in range(0, len(links)):
                            match = re.search(website_pattern, links[i][0])
                            if match is not None:
                                site_found = (True, links[i][1])
                                break

                        for i in range(0, len(links)):
                            link_title = links[i][0]
                            similarity = round(jaro_similarity(channel_name, link_title), 2)
                            if similarity >= 0.60:
                                match = re.search(r"youtube\.com\/.+", links[i][1])
                                if match is None:
                                    site_found = (True, links[i][1])
                                    break

                    '''
                    Use previously declared RegEx patterns to extract links
                    for Facebook, Twitter, and LinkedIn in a channel's About section
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
        '''
        fb_link = np.nan
        twitter_link = np.nan

        if fb_found[0]:
            fb_link = fb_found[1]

        if twitter_found[0]:
            twitter_link = twitter_found[1]
        '''

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


if __name__ == '__main__':
    filename = input("Filename (w/o .csv): ")
    path = os.getcwd() + "/datasets/" + filename
    os.chdir(path)

    print("Reading list of channels...")
    channel_df = pd.read_csv("channels.csv", index_col=0)
    print("Reading list of videos...")
    video_df = pd.read_csv("videos.csv", index_col=0)

    find_sources_via_yt(channel_df, video_df)

    os.chdir("..")
    os.chdir("..")
