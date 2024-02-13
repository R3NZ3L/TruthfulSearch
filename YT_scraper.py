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


def search_test():
    searchQuery = input("Search query: ")
    pages = int(input("Number of pages (50 videos per page): "))

    search_request = youtube.search().list(
        part="snippet",
        q=searchQuery,
        type="video",
        maxResults=50,
        order="relevance",
        regionCode="PH"
    )
    search_response = search_request.execute()

    '''
    Response Keys: 
    dict_keys(['kind', 'etag', 'nextPageToken', 'regionCode', 'pageInfo', 'items'])

    Search Results (items) Keys: 
    dict_keys(['kind', 'etag', 'id', 'snippet'])

    Metadata (snippet) Keys: 
    dict_keys(['publishedAt', 'channelId', 'title', 'description', 'thumbnails', 'channelTitle', 'liveBroadcastContent', 'publishTime']) 
    '''
    searchResults = search_response.get("items")

    print("--------------")

    # Returns a number of results; to get multiple results, change range max
    for n in range(0, pages):
        print("----------------------- SEARCH PAGE " + str(n + 1) + " -----------------------")
        for i in range(0, 50):
            video = searchResults[i]
            metadata = video.get("snippet")

            print("[" + str(i + 1) + "]")
            print("Video ID: " + video.get("id").get("videoId"))
            print("Title: " + str(metadata.get("title")))
            print("Channel: " + str(metadata.get("channelTitle") + " (" + metadata.get("channelId") + ")"))
            # print("Description: " + str(metadata.get("description")))

            request = youtube.videos().list(
                part=['snippet, statistics'],
                id=video.get("id").get("videoId"),
                maxResults=1
            )

            vid_specs = request.execute()
            print("----------------------------------------")
            '''
            Video Specifics Keys:
            dict_keys(['kind', 'etag', 'items', 'pageInfo'])
            '''

            # Channel information
            request = youtube.channels().list(
                part=['snippet', 'statistics'],
                id=metadata.get("channelId"),
                maxResults=1
            )
            channel_specs = request.execute()

            print("Channel Subscriber count: " + channel_specs.get("items")[0].get("statistics").get("subscriberCount"))
            print("Channel Total videos uploaded: " + channel_specs.get("items")[0].get("statistics").get("videoCount"))
            print(
                "Channel Date of Publication: " + channel_specs.get("items")[0].get("snippet").get("publishedAt")[:10])

            print("------------------Start of Description------------------")
            print("Description:\n" + vid_specs.get("items")[0].get("snippet").get("description"))
            print("------------------End of Description------------------")

            print("Video Date of Publication: " + metadata.get("publishedAt")[:10])
            print("Video View Count: " + vid_specs.get("items")[0].get("statistics").get("viewCount"))
            print("Video Like Count: " + vid_specs.get("items")[0].get("statistics").get("likeCount"))

            try:
                print("Video Dislike Count: " + vid_specs.get("items")[0].get("statistics").get("dislikeCount"))
            except:
                print("Video Dislike Count: N/A")

            try:
                print("Video Comment Count: " + vid_specs.get("items")[0].get("statistics").get("commentCount"))
            except:
                print("Video Comment Count: N/A")
            '''
            try:
                print("Transcript: " + str(YouTubeTranscriptApi.get_transcript(video.get("id").get("videoId"))))
            except:
                print("Transcript unavailable")
            finally:
                print("")
            # '''
            print("")

        # Next page, if needed
        if n != pages:
            next_page_request = youtube.search().list_next(
                previous_request=search_request,
                previous_response=search_response
            )
            search_response = next_page_request.execute()
            searchResults = search_response.get("items")
            print("")


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
    columns = ["video_id", "video_title", "description", "video_dop",
               "view_count", "like_count", "comment_count",
               "channel_id", "channel_name", "channel_dop", "sub_count",
               "total_videos"]

    pbar = tqdm(total=num_videos)
    pbar.set_description("Scraping...")
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
                metadata.get("channelTitle"),  # channel_name
                channel_specs.get("items")[0].get("snippet").get("publishedAt")[:10],  # channel_dop
                channel_specs.get("items")[0].get("statistics").get("subscriberCount"),  # sub_count
                channel_specs.get("items")[0].get("statistics").get("videoCount")  # total_videos
            ]

            # Append record to list
            temp_video_list.append(record)

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
    # ------------- SCRAPING ------------- #

    # Converting numpy array to DataFrame
    print("Converting to DataFrame...")
    df = pd.DataFrame(temp_nparray, columns=columns)

    # Saving to a .csv file
    print("Saving as " + filename + ".csv...")
    path = os.getcwd() + "/datasets/" + filename

    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    finally:
        os.chdir(path)

    df.to_csv(filename + ".csv")
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


def check_desc(channel_name, videos_df, pattern):
    # Get first 5 videos of channel from videos_df
    videos_df = videos_df.loc[videos_df["channel_name"] == channel_name].reset_index().drop("index", axis=1).head()
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


def find_sources(channel_names, channel_IDs, main_df):
    pbar = tqdm(total=len(channel_names))
    pbar.set_description("Finding sources...")

    source_scores = []
    ss_cols = [
        "channel_id", "channel_name",
        "profiles", "website", "social_media_presence",
        "vs"
    ]

    source_links = []
    sl_cols = [
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
    linkedIn_pattern = r"(?<=(Linked(in|In)\:\s))https:\/\/(www\.)?linkedin\.com\/(company|in)\/(\w|\w[-_])+\/"
    website_pattern = r"(?<=(W|w)ebsite((\:)?\s|\sat\s))https:\/\/\w+(\.(\w|\w[-_])+)?\.\w{3}(\.\w{2})?(\/(\w|\w[-_])+)?"
    fb_pattern = r"(?<=((F|f)acebook\:\s))https:\/\/(www\.)?facebook\.com\/(\w|\w[-_])+"
    twitter_pattern = r"(?<=((T|t)witter\:\s))https:\/\/(www\.)?(twitter|x)\.com\/(\w|\w[-_])+"
    # ---

    for channel_name in channel_names:
        # --- Checking descriptions from channel's videos
        linkedIn_found = check_desc(channel_name, main_df, linkedIn_pattern)
        site_found = check_desc(channel_name, main_df, website_pattern)
        fb_found = check_desc(channel_name, main_df, fb_pattern)
        twitter_found = check_desc(channel_name, main_df, twitter_pattern)
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
        # ---

        profiles = 0
        website = 0
        social_media_presence = 0

        if linkedIn_found[0] and wiki_found[0]:
            profiles = 3
        elif linkedIn_found[0] and not wiki_found[0]:
            profiles = 2
        elif not linkedIn_found[0] and wiki_found[0]:
            profiles = 1

        if site_found[0]:
            website = 2

        if fb_found[0] or twitter_found[0]:
            social_media_presence = 1

        # Source scores ---
        ss_record = [
            channel_IDs.get(channel_name),  # channel_id
            channel_name,  # channel_name
            profiles,  # profiles
            website,  # website
            social_media_presence,  # social_media_presence
            np.nan  # vs
        ]
        source_scores.append(ss_record)
        # ---

        # Source links ---
        fb_link = None
        twitter_link = None

        if fb_found[0]:
            fb_link = fb_found[1]

        if twitter_found[0]:
            twitter_link = twitter_found[1]

        sl_record = [
            channel_IDs.get(channel_name),
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

    ss_nparray = np.array(source_scores)
    sl_nparray = np.array(source_links)

    ss_df = pd.DataFrame(ss_nparray, columns=ss_cols)
    sl_df = pd.DataFrame(sl_nparray, columns=sl_cols)

    ss_df.to_csv("source_scores.csv")
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

                df = pd.read_csv(filename + ".csv")
                df.drop("Unnamed: 0", axis=1, inplace=True)
                print(f"File {filename} found.")

                channel_names = df["channel_name"].unique()
                channel_IDs = df[["channel_id", "channel_name"]].groupby("channel_name").first().to_dict().get("channel_id")

                find_sources(channel_names, channel_IDs, df)

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

                ss_df = pd.read_csv("source_scores.csv")
                ss_df.drop("Unnamed: 0", axis=1, inplace=True)
                print(f"File {filename} found.")

                weights = {
                    "profiles": 0.50,
                    "website": 0.35,
                    "social_media_presence": 0.15
                }

                ss_df["vs"] = topsis(ss_df, weights)
                ss_df.to_csv("source_scores.csv")

                # TODO: Compute for video rank and save to .csv

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





