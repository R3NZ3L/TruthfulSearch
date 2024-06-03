# Google API Python Client by Google (n.d.)
# https://github.com/googleapis/google-api-python-client
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from jellyfish import jaro_similarity

import pandas as pd
import numpy as np
from tqdm import tqdm
import regex as re
import requests
from bs4 import BeautifulSoup
import json
import os

# Put your personal API key here
# DLSU account key
apiKey = 'AIzaSyCIplXpNgYZ2IS44ZYyEi-hXRu1gzl9I58' # Aldecoa
# apiKey = 'AIzaSyCJBMIMpGpBdmTkx7SRhObSNAyV_aRSjho' # Aquino
# apiKey = 'AIzaSyBTRvkhM6ESdLHu0djfP39-IKHufQogxOI' # Baura
# apiKey = 'AIzaSyA7eqxwuzM6SUDDVTss6DSzKGEt7kSJesg' # Sevillana

# Search engine ID
cseKey = "23c1c70a203ac4852" # Aldecoa
# cseKey = "a7c987e23f0fe448e" # Aquino
# cseKey = "76c19208b12de4763" # Baura
# cseKey = "a674809398a7b46df" # Sevillana

# Google Custom Search API
google_resource = build("customsearch", "v1", developerKey=apiKey).cse()

quota_reached = False
stopped_at = None


def find_linkedIn(channel_name, query):
    found = False
    pattern = r'https:\/\/www\.linkedin\.com\/(company|in)\/.+'  # Used to find specific profile links

    try:
        li_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            link = li_response.get("items")[i].get("formattedUrl")
            if re.search(pattern, link) is not None:
                # Get profile name from search result
                match = re.search(r'\w+\s(\w+)?', li_response.get("items")[i].get("title"))
                if match is not None:
                    profile_name = match.group()

                    # Get similarity between found profile name and channel name
                    # This is to prevent false positives in finding a LinkedIn profile
                    similarity = round(jaro_similarity(channel_name.lower(), profile_name.lower()), 2)

                    # If n% similar, consider LinkedIn profile as found
                    if similarity >= 0.80:
                        found = True
                        break
    except HttpError:
        global quota_reached
        global stopped_at
        if not quota_reached:
            quota_reached = True
            stopped_at = (channel_name, query)

    if not found:
        return found, np.nan
    else:
        return found, link


def find_wiki(channel_name, query):
    found = False
    pattern = r'https:\/\/\w{2}.wikipedia\.org\/wiki\/.+'

    try:
        wiki_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            link = wiki_response.get("items")[i].get("formattedUrl")
            if re.search(pattern, link) is not None:
                # Get Wiki page name from search result
                title = wiki_response.get("items")[i].get("title")
                match = re.search(r'.+(?=\s-\sWikipedia)', title)
                if match is not None:
                    page_name = match.group()

                    # Get similarity between found Wiki page name and channel name
                    # This is to prevent false positives in finding a Wiki page
                    similarity = round(jaro_similarity(channel_name.lower(), page_name.lower()), 2)

                    # If n% similar, consider Wiki page as found
                    if similarity >= 0.80:
                        found = True
                        break
    except HttpError:
        global quota_reached
        global stopped_at
        if not quota_reached:
            quota_reached = True
            stopped_at = (channel_name, query)

    if not found:
        return found, np.nan
    else:
        return found, link


def find_website(channel_name, query):
    found = False
    # RegEx to exclude YouTube, LinkedIn, and Wikipedia pages
    pattern = r'https\:\/\/(\w{2}.wikipedia\.org\/wiki\/.+|www\.(youtube\.com.+|linkedin\.com.+))'

    try:
        website_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            title = website_response.get("items")[i].get("title")
            link = website_response.get("items")[i].get("link")
            if channel_name.lower() in title.lower():
                if re.search(pattern, link) is None:
                    # The first result among the filtered at this point is MOST LIKELY the official website
                    found = True
                    break
    except HttpError:
        global quota_reached
        global stopped_at
        if not quota_reached:
            quota_reached = True
            stopped_at = (channel_name, query)

    if not found:
        return found, np.nan
    else:
        return found, link


def find_fb(channel_name, query):
    found = False
    pattern = r'^https\:\/\/www\.facebook\.com\/.+\/'

    try:
        fb_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            link = fb_response.get("items")[i].get("formattedUrl")
            if re.search(pattern, link) is not None:
                title = fb_response.get("items")[i].get("title")
                similarity = round(jaro_similarity(channel_name.lower(), title.lower()), 2)

                if similarity >= 0.80:
                    found = True
                    break
    except HttpError:
        global quota_reached
        global stopped_at
        if not quota_reached:
            quota_reached = True
            stopped_at = (channel_name, query)

    if not found:
        return found, np.nan
    else:
        return found, link


def find_twitter(channel_name, query):
    found = False
    pattern = r'https\:\/\/(twitter|x)\.com\/.+'

    try:
        twitter_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            link = twitter_response.get("items")[i].get("formattedUrl")
            if re.search(pattern, link) is not None:
                title = twitter_response.get("items")[i].get("title")
                similarity = round(jaro_similarity(channel_name.lower(), title.lower()), 2)

                if similarity >= 0.80:
                    found = True
                    break
    except HttpError:
        global quota_reached
        global stopped_at
        if not quota_reached:
            quota_reached = True
            stopped_at = (channel_name, query)

    if not found:
        return found, np.nan
    else:
        return found, link


def check_desc(channel_id, videos_df, pattern):
    # Get first 5 videos of channel from videos_df
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

            print(f"Found in video description: {match.group()}")

            break

    return found


def check_about_links(pattern, links):
    found = (False, np.nan)

    for i in range(0, len(links)):
        match = re.search(pattern, links[i][1])
        if match is not None:
            found = (True, match.group())

            print(f"Found in About section: {match.group()}")

            links.pop(i)
            break

    return found, links


def find_sources(channel_df, video_df, unchecked_exists):
    global quota_reached
    global stopped_at

    unchecked = pd.DataFrame(columns=channel_df.columns)

    pbar = tqdm(total=channel_df.shape[0])
    pbar.set_description("Finding sources...")

    source_check = []
    source_links = []
    cols = [
        "channel_id", "channel_name",
        "LinkedIn", "Wiki", "Website",
        "Twitter", "Facebook"
    ]

    query_tail = [
        " LinkedIn",
        " Wiki",
        " Official Website",
        " Facebook",
        " Twitter"
    ]

    # --- Patterns to search for links within video descriptions
    desc_linkedIn_pattern = r"(?<=(Linked(in|In)\:\s))(https:\/\/www\.)?linkedin\.com\/(company|in)\/(\w|\w[-_/])+\/"
    # desc_website_pattern = r"(?<=(W|w)ebsite((\:)?\s|\sat\s))https:\/\/\w+(\.(\w|\w[-_])+)?\.\w{3}(\.\w{2})?(\/(\w|\w[-_])+)?"
    desc_website_pattern = r"(?<=(W|w)ebsite((\:)?\s|\sat\s))(\w|[:/.])+"
    desc_fb_pattern = r"(?<=((F|f)acebook\:\s))(https:\/\/www\.)?facebook\.com\/(\w|\w[-_/])+"
    desc_twitter_pattern = r"(?<=((T|t)witter\:\s))(https:\/\/www\.)?(twitter|x)\.com\/(\w|\w[-_/])+"
    # ---

    # --- Patterns to search for links within About sections in channel pages
    about_website_pattern = r"(?<=(W|w)ebsite((\:)?\s|\sat\s))(\w|[:/.])+"
    about_fb_pattern = r"(https:\/\/www\.)?facebook\.com\/(\w|\w[-_/])+"
    about_linkedIn_pattern = r"(https:\/\/www\.)?linkedin\.com\/(company|in)\/(\w|\w[-_/])+"
    about_twitter_pattern = r"(https:\/\/www\.)?twitter\.com\/(\w|\w[-_/])+"
    # ---

    for i in range(0, channel_df.shape[0]):
        linkedIn_found = (False, np.nan)
        wiki_found = (False, np.nan)
        site_found = (False, np.nan)
        twitter_found = (False, np.nan)
        fb_found = (False, np.nan)

        channel_id = channel_df.iloc[i]["channel_id"]
        channel_name = channel_df.iloc[i]["channel_name"]

        if quota_reached:
            unchecked = pd.concat([unchecked, channel_df.loc[channel_df["channel_id"] == str(channel_id)]])
            pbar.update(1)
            continue

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

                    fb_found, links = check_about_links(about_fb_pattern, links)
                    twitter_found, links = check_about_links(about_twitter_pattern, links)
                    linkedIn_found, links = check_about_links(about_linkedIn_pattern, links)

                    site_found = (False, np.nan)

                    for i in range(0, len(links)):
                        match = re.search(about_website_pattern, links[i][0])
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

        # --- Checking descriptions from channel's videos
        if not linkedIn_found[0]:
            linkedIn_found = check_desc(channel_id, video_df, desc_linkedIn_pattern)

        if not site_found[0]:
            site_found = check_desc(channel_id, video_df, desc_website_pattern)

        if not fb_found[0]:
            fb_found = check_desc(channel_id, video_df, desc_fb_pattern)

        if not twitter_found[0]:
            twitter_found = check_desc(channel_id, video_df, desc_twitter_pattern)
        # ---

        # --- If link not found in descriptions, search via Google
        wiki_found = find_wiki(channel_name, channel_name + query_tail[1])

        if not linkedIn_found[0]:
            linkedIn_found = find_linkedIn(channel_name, channel_name + query_tail[0])

        '''
        if not site_found[0]:
            site_found = find_website(channel_name, channel_name + query_tail[2])

        if not fb_found[0]:
            fb_found = find_fb(channel_name, channel_name + query_tail[3])

        if not twitter_found[0]:
            twitter_found = find_twitter(channel_name, channel_name + query_tail[4])
        # '''

        if not quota_reached:
            # Source checks ---
            sc_record = [
                channel_id,  # channel_id
                channel_name,  # channel_name
                linkedIn_found[0],
                wiki_found[0],
                site_found[0],
                twitter_found[0],
                fb_found[0]
            ]
            source_check.append(sc_record)
            # ---

            # Source links ---
            fb_link = np.nan
            twitter_link = np.nan

            if fb_found[0]:
                fb_link = fb_found[1]

            if twitter_found[0]:
                twitter_link = twitter_found[1]

            sl_record = [
                channel_id,
                channel_name,
                linkedIn_found[1],
                wiki_found[1],
                site_found[1],
                twitter_link,
                fb_link
            ]
            source_links.append(sl_record)
            # ---
            pbar.update(1)

        elif quota_reached:
            unchecked = pd.concat([unchecked, channel_df.loc[channel_df["channel_id"] == str(channel_id)]])
            pbar.update(1)
            continue

    pbar.close()

    if quota_reached:
        print("Custom Search API daily quota reached.")
        print(f"Stopped at channel '{stopped_at[0]}' with query '{stopped_at[1]}'")
        print("Saving unchecked channels in unchecked.csv...")
        unchecked.to_csv("unchecked.csv")

    if len(source_check) > 0:
        sc_nparray = np.array(source_check)
        sl_nparray = np.array(source_links)
        sc_df = pd.DataFrame(sc_nparray, columns=cols)
        sl_df = pd.DataFrame(sl_nparray, columns=cols)
    else:
        sc_df = pd.DataFrame(columns=cols)
        sl_df = pd.DataFrame(columns=cols)

    if unchecked_exists:
        old_sc = pd.read_csv("source_check.csv", index_col=0)
        old_sl = pd.read_csv("source_links.csv", index_col=0)

        if old_sc.shape[0] != 0:
            print("Concatenating with old results...")
            sc_df = pd.concat([old_sc, sc_df]).reset_index().drop("index", axis=1)
            sl_df = pd.concat([old_sl, sl_df]).reset_index().drop("index", axis=1)
    else:
        pass

    sc_df.to_csv("source_check.csv")
    sl_df.to_csv("source_links.csv")

    if not quota_reached and unchecked_exists:
        try:
            os.remove("unchecked.csv")
        except FileNotFoundError:
            pass

    print("Source check complete.")


if __name__ == '__main__':
    filename = input("Filename (w/o .csv): ")
    path = os.getcwd() + "/datasets/" + filename
    os.chdir(path)

    try:
        print("Getting unchecked channels...")
        channel_df = pd.read_csv("unchecked.csv", index_col=0)
        os.remove("unchecked.csv")
        unchecked_exists = True
    except FileNotFoundError:
        channel_df = pd.read_csv("channels.csv", index_col=0)
        unchecked_exists = False
    finally:
        video_df = pd.read_csv("videos.csv", index_col=0)

    find_sources(channel_df, video_df, unchecked_exists)

    os.chdir("..")
    os.chdir("..")
