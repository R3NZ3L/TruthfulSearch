# Google API Python Client by Google (n.d.)
# https://github.com/googleapis/google-api-python-client
# To install, run the following: pip install google-api-python-client
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# YouTube Transcript API by Jonas Depoix (2018)
# https://github.com/jdepoix/youtube-transcript-api
# To install, run the following: pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi

import pandas as pd
import numpy as np
from math import ceil
from math import sqrt
from tqdm import tqdm
import os
from time import sleep
from jellyfish import jaro_similarity
import regex as re
import requests
from bs4 import BeautifulSoup
import json

# Put your personal API key here
# DLSU account key
apiKey = 'AIzaSyCIplXpNgYZ2IS44ZYyEi-hXRu1gzl9I58'
# Personal email account key
# apiKey = 'AIzaSyDrA3VG9qxJOSxgcQKpcuQgjQVA1XjtpbQ'

# Search engine ID
cseKey = "23c1c70a203ac4852"

# YouTube API object
youtube = build('youtube', 'v3', developerKey=apiKey)

# Google Custom Search API
google_resource = build("customsearch", "v1", developerKey=apiKey).cse()

quota_reached = False
stopped_at = None


def yt_scrape(search_query, num_videos, filename):
    # Storing data in a numpy array of lists
    # ------------- SCRAPING ------------- #
    print("")

    if num_videos < 50:
        num_pages = 1
    else:
        num_pages = ceil(num_videos / 50)

    # Order by RELEVANCE or DATE can be done; check documentation for search().list()
    search_request = youtube.search().list(
        part="snippet",
        q=search_query,
        type="video",
        maxResults=50,
        regionCode="PH"
    )

    search_response = search_request.execute()
    search_results = search_response.get("items")

    temp_video_list = []
    """
    columns = ["video_id", "video_title", "description", "video_dop",
               "view_count", "like_count", "comment_count",
               "channel_id", "channel_name", "channel_dop", "sub_count",
               "total_videos", "video_transcript"]
    """

    columns = ["video_id", "video_title", "description", "video_dop",
               "view_count", "like_count", "comment_count", 
               "channel_id", "video_transcript"]
    
    temp_channel_list = []
    channel_info_columns = ["channel_id", "channel_name", "channel_dop", 
                            "sub_count", "total_videos"]
    
    temp_comment_list = []
    comment_columns = ['video_id', 'comment']

    pbar = tqdm(total=num_videos)
    pbar.set_description("Scraping...")

    # List of IDs, to check if list exceeds 20 channels after next iteration
    channels = []

    for n in range(0, num_pages):
        j = 0
        if num_videos > 50:
            num_videos -= 50
            j = 50
        elif num_videos <= 50:
            j = num_videos

        for i in range(0, j):
            # Data from SERP
            video = search_results[i]
            metadata = video.get("snippet")

            '''
            if metadata.get("channelId") in channels:
                pass
            elif len(channels) < 20:
                channels.append(metadata.get("channelId"))
            else:
                continue
            # '''


            # Video-specific data
            request = youtube.videos().list(
                part=['snippet, statistics'],
                id=video.get("id").get("videoId"),
                maxResults=1
            )
            vid_specs = request.execute()

            # Channel-specific data
            request = youtube.channels().list(
                part=['snippet', 'statistics'],
                id=metadata.get("channelId"),
                maxResults=1
            )
            channel_specs = request.execute()
            
            video_transcript = ""

            try:
                transcript_dict = YouTubeTranscriptApi.get_transcript(video.get("id").get("videoId"), languages=['en'])
            except:
                video_transcript = None
                # print("No English Caption for this video")
            else:
                for item in transcript_dict:
                    video_transcript += " " + item['text']
                # print(video_transcript)
                
            # This list will contain data for one record 
            try:
                comment_count = int(vid_specs.get("items")[0].get("statistics").get("commentCount"))
            except:
                comment_count = 0

            record = [
                video.get("id").get("videoId"),  # video_id
                metadata.get("title"),  # video_title
                vid_specs.get("items")[0].get("snippet").get("description"),  # description
                metadata.get("publishedAt")[:10],  # video_dop
                vid_specs.get("items")[0].get("statistics").get("viewCount"),  # view_count
                vid_specs.get("items")[0].get("statistics").get("likeCount"),  # like_count
                comment_count,  # comment_count
                metadata.get("channelId"),  # channel_id
                video_transcript    # video_transcript
            ]

            channel = [
                metadata.get("channelId"),  # channel_id
                metadata.get("channelTitle"),  # channel_name
                channel_specs.get("items")[0].get("snippet").get("publishedAt")[:10],  # channel_dop
                channel_specs.get("items")[0].get("statistics").get("subscriberCount"),  # sub_count
                channel_specs.get("items")[0].get("statistics").get("videoCount"),  # total_videos
            ]
            
            comment_request = youtube.commentThreads().list(
                part=['snippet'],
                videoId=video.get("id").get("videoId"),
                maxResults=10,
                order='relevance',
                textFormat="plainText"
            )

            try:
                video_comments = comment_request.execute()
            except:
                # print("No comment for this video")
                pass
            else:   
                for comment in video_comments.get("items"):
                    temp_comment_list.append([video.get("id").get("videoId"),
                                                comment.get("snippet").get("topLevelComment").get("snippet").get("textDisplay")])
                    
            # Append record to list
            temp_video_list.append(record)

            # Append channel record to list
            unique = True
            for unique_channel in temp_channel_list:
                if unique_channel[0] == channel[0]:
                    unique_channel == channel
                    unique = False
                    break

            if unique:
                temp_channel_list.append(channel)

            # Update progress bar
            pbar.update(1)

        # Next page, if needed
        if n != num_pages:
            next_page_request = youtube.search().list_next(
                previous_request=search_request,
                previous_response=search_response
            )
            search_response = next_page_request.execute()
            search_results = search_response.get("items")
    pbar.close()

    temp_nparray = np.array(temp_video_list)
    temp_channel_nparray = np.array(temp_channel_list)
    temp_comment_nparray = np.array(temp_comment_list)
    # ------------- SCRAPING ------------- #

    # Converting numpy array to DataFrame
    print("Converting to DataFrame...")
    video_df = pd.DataFrame(temp_nparray, columns=columns)

    # print("Converting channels to DataFrame...")
    channel_df = pd.DataFrame(temp_channel_nparray, columns=channel_info_columns)

    # print("Converting comments to DataFrame...")
    comment_df = pd.DataFrame(temp_comment_nparray, columns=comment_columns)

    # Saving to a .csv file
    print("Saving as " + filename + ".csv...")
    path = os.getcwd() + "/datasets/" + filename

    # Saving to a .csv file
    print("Saving as " + filename + "_channels.csv...")

    # Saving to a .csv file
    print("Saving as " + filename + "_comments.csv...")

    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    finally:
        os.chdir(path)

    video_df.to_csv(filename + ".csv")
    channel_df.to_csv(filename + "_channels.csv")
    comment_df.to_csv(filename + "_comments.csv")
    print("Saved @ " + os.getcwd())
    os.chdir("..")
    os.chdir("..")


# Functions
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
        return found, None
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
        return found, None
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
        return found, None
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
        return found, None
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
        return found, None
    else:
        return found, link


def check_desc(channel_id, videos_df, pattern):
    # Get first 5 videos of channel from videos_df
    videos_df = videos_df.loc[videos_df["channel_id"] == channel_id].reset_index().drop("index", axis=1).head()
    found = (False, None)

    # For each video
    for i in range(0, videos_df.shape[0]):
        # Get description
        desc = repr(videos_df.iloc[i]["description"]).replace("\\n", " ").replace("  ", " ")

        # Using RegEx, find links using given pattern
        match = re.search(pattern, desc)
        if match is not None:
            found = (True, match.group())
            break

    return found


def check_about_links(pattern, links):
    found = (False, None)

    for i in range(0, len(links)):
        match = re.search(pattern, links[i][1])
        if match is not None:
            found = (True, match.group())
            links.pop(i)
            break

    return found, links


def find_sources(channel_df, video_df):
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
    desc_linkedIn_pattern = r"(?<=(Linked(in|In)\:\s))https:\/\/(www\.)?linkedin\.com\/(company|in)\/(\w|\w[-_])+\/"
    desc_website_pattern = r"(?<=(W|w)ebsite((\:)?\s|\sat\s))https:\/\/\w+(\.(\w|\w[-_])+)?\.\w{3}(\.\w{2})?(\/(\w|\w[-_])+)?"
    desc_fb_pattern = r"(?<=((F|f)acebook\:\s))https:\/\/(www\.)?facebook\.com\/(\w|\w[-_])+"
    desc_twitter_pattern = r"(?<=((T|t)witter\:\s))https:\/\/(www\.)?(twitter|x)\.com\/(\w|\w[-_])+"
    # ---

    # --- Patterns to search for links within About sections in channel pages
    about_website_pattern = r"(W|w)ebsite"
    about_fb_pattern = r"facebook\.com\/.+"
    about_linkedIn_pattern = r"linkedin\.com\/(company|in)\/.+"
    about_twitter_pattern = r"twitter\.com\/.+"
    # ---

    for i in range(0, channel_df.shape[0]):
        channel_id = channel_df.iloc[i]["channel_id"]
        channel_name = channel_df.iloc[i]["channel_name"]

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

                    site_found = (False, None)

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
        if not linkedIn_found[0]:
            linkedIn_found = find_linkedIn(channel_name, channel_name + query_tail[0])

        if not site_found[0]:
            site_found = find_website(channel_name, channel_name + query_tail[2])

        if not fb_found[0]:
            fb_found = find_fb(channel_name, channel_name + query_tail[3])

        if not twitter_found[0]:
            twitter_found = find_twitter(channel_name, channel_name + query_tail[4])

        wiki_found = find_wiki(channel_name, channel_name + query_tail[1])

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
        fb_link = None
        twitter_link = None

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
    pbar.close()

    global quota_reached
    global stopped_at
    if quota_reached:
        print("Custom Search API daily quota reached.")
        print(f"Stopped at channel '{stopped_at[0]}' with query '{stopped_at[1]}'")

    sc_nparray = np.array(source_check)
    sl_nparray = np.array(source_links)

    ss_df = pd.DataFrame(sc_nparray, columns=cols)
    sl_df = pd.DataFrame(sl_nparray, columns=cols)

    ss_df.to_csv("source_check.csv")
    sl_df.to_csv("source_links.csv")

    print("Complete.")


def topsis(scores, weights):
    wndm = {}

    for column in weights.keys():
        temp_list = []
        x = 0
        for i in range(0, scores.shape[0]):
            num = scores.iloc[i][column] ** 2
            x += num
        denominator = sqrt(x)

        # Normalize scores
        for i in range(0, scores.shape[0]):
            norm_score = scores.iloc[i][column] / denominator
            temp_list.append(norm_score)

        # Apply weight
        for i in range(0, len(temp_list)):
            temp_list[i] *= weights.get(column)

        wndm.update({column: temp_list})

    wndm_df = pd.DataFrame.from_dict(wndm)
    ideal_best = wndm_df.max()
    ideal_worst = wndm_df.min()

    dist_from_best = []
    dist_from_worst = []

    # Euclidean distance from ideal best
    for i in range(0, wndm_df.shape[0]):
        temp_num = 0
        for column in wndm_df.columns:
            temp_num += (wndm_df.iloc[i][column] - ideal_best[column]) ** 2
        dist_from_best.append(sqrt(temp_num))

    # Euclidean distance from ideal worst
    for i in range(0, wndm_df.shape[0]):
        temp_num = 0
        for column in wndm_df.columns:
            temp_num += (wndm_df.iloc[i][column] - ideal_worst[column]) ** 2
        dist_from_worst.append(sqrt(temp_num))

    performance_rank = []
    for i in range(0, wndm_df.shape[0]):
        performance_rank.append(dist_from_worst[i] / (dist_from_best[i] + dist_from_worst[i]))

    performance_rank = pd.Series(np.array(performance_rank))

    return performance_rank


if __name__ == '__main__':
    cont = True

    while cont:
        print("Working @ " + os.getcwd())
        print("     [1] Scrape videos from YouTube")
        print("     [2] Find external sources")
        print("     [3] Compute rankings and verifiability scores")
        print("     [4] End program")
        choice = int(input("Input: "))
        print("----")

        if choice == 1:
            search_query = input("Search Query: ")
            num_videos = int(input("Number of Videos: "))
            filename = input("Filename (w/o .csv): ")

            # Making a dataset
            yt_scrape(search_query, num_videos, filename)

        elif choice == 2:
            filename = input("Filename (w/o .csv): ")

            try:
                # Change directory to specific folder
                os.chdir(os.getcwd() + "/datasets/" + filename)

                print("Working @ " + os.getcwd())

                video_df = pd.read_csv(filename + ".csv").drop("Unnamed: 0", axis=1)
                channel_df = pd.read_csv(filename + "_channels.csv").drop("Unnamed: 0", axis=1)
                print(f"File {filename} found.")

                find_sources(channel_df, video_df)

                # Return to main folder
                os.chdir("..")
                os.chdir("..")

            except FileNotFoundError:
                print("File does not exist")

        elif choice == 3:
            filename = input("Enter dataset filename (w/o .csv): ")

            try:
                # Change directory to specific folder
                os.chdir(os.getcwd() + "/datasets/" + filename)

                print("Working @ " + os.getcwd())

                ##################################

                print("Complete.")

                # Return to main folder
                os.chdir("..")
                os.chdir("..")

            except FileNotFoundError:
                print("File does not exist")

        elif choice == 4:
            cont = False
            print("Ending program...")

        print("---")
        print("")
        sleep(1)