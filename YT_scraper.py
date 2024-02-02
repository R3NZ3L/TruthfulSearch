# Google API Python Client by Google (n.d.)
# https://github.com/googleapis/google-api-python-client
# To install, run the following: pip install google-api-python-client
from googleapiclient.discovery import build

# YouTube Transcript API by Jonas Depoix (2018)
# https://github.com/jdepoix/youtube-transcript-api
# To install, run the following: pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi

import pandas as pd
import numpy as np
from math import ceil
from tqdm import tqdm
import os
from time import sleep
from jellyfish import jaro_similarity
import regex as re

# Put your personal API key here
apiKey = 'AIzaSyCIplXpNgYZ2IS44ZYyEi-hXRu1gzl9I58'

# Search engine ID
cseKey = "23c1c70a203ac4852"

# YouTube API object
youtube = build('youtube', 'v3', developerKey=apiKey)

# Google Custom Search API
google_resource = build("customsearch", "v1", developerKey=apiKey).cse()



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
            print("Description:\n" + repr(vid_specs.get("items")[0].get("snippet").get("description")))
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
               "channel_id", "channel_title", "channel_dop", "sub_count",
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
                repr(vid_specs.get("items")[0].get("snippet").get("description")),  # description
                metadata.get("publishedAt")[:10],  # video_dop
                vid_specs.get("items")[0].get("statistics").get("viewCount"),  # view_count
                vid_specs.get("items")[0].get("statistics").get("likeCount"),  # like_count
                comment_count,  # comment_count
                metadata.get("channelId"),  # channel_id
                metadata.get("channelTitle"),  # channel_title
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
    li_response = google_resource.list(
        q=query,
        cx=cseKey
    ).execute()

    found = False
    pattern = r'https:\/\/www\.linkedin\.com\/(company|in)\/.+'  # Used to find specific profile links

    for i in range(0, 10):
        link = li_response.get("items")[i].get("formattedUrl")
        if re.search(pattern, link) is not None:
            # Get profile name from search result
            match = re.search(r'\w+\s(\w+)?', li_response.get("items")[i].get("htmlTitle"))
            if match is not None:
                profile_name = match.group()

                # Get similarity between found profile name and channel name
                # This is to prevent false positives in finding a LinkedIn profile
                similarity = round(jaro_similarity(channel_name.lower(), profile_name.lower()), 2)

                # If n% similar, consider LinkedIn profile as found
                if similarity >= 0.80:
                    found = True
                    break

    if not found:
        return found, None
    else:
        return found, link


def find_wiki(channel_name, query):
    wiki_response = google_resource.list(
        q=query,
        cx=cseKey
    ).execute()

    found = False
    pattern = r'https:\/\/\w{2}.wikipedia\.org\/wiki\/.+'

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

    if not found:
        return found, None
    else:
        return found, link


def find_website(channel_name, query):
    website_response = google_resource.list(
        q=query,
        cx=cseKey
    ).execute()

    found = False
    # RegEx to exclude YouTube, LinkedIn, and Wikipedia pages
    pattern = r'https\:\/\/(\w{2}.wikipedia\.org\/wiki\/.+|www\.(youtube\.com.+|linkedin\.com.+))'

    for i in range(0, 10):
        title = website_response.get("items")[i].get("title")
        link = website_response.get("items")[i].get("link")
        if channel_name.lower() in title.lower():
            if re.search(pattern, link) is None:
                # The first result among the filtered at this point is MOST LIKELY the official website
                found = True
                break

    if not found:
        return found, None
    else:
        return found, link


def find_fb(channel_name, query):
    fb_response = google_resource.list(
        q=query,
        cx=cseKey
    ).execute()

    found = False
    pattern = r'^https\:\/\/www\.facebook\.com\/.+\/'

    for i in range(0, 10):
        link = fb_response.get("items")[i].get("formattedUrl")
        if re.search(pattern, link) is not None:
            title = fb_response.get("items")[i].get("title")
            similarity = round(jaro_similarity(channel_name.lower(), title.lower()), 2)

            if similarity >= 0.80:
                found = True
                break

    if not found:
        return found, None
    else:
        return found, link


def find_twitter(channel_name, query):
    twitter_response = google_resource.list(
        q=query,
        cx=cseKey
    ).execute()

    found = False
    pattern = r'https\:\/\/(twitter|x)\.com\/.+'

    for i in range(0, 10):
        link = twitter_response.get("items")[i].get("formattedUrl")
        if re.search(pattern, link) is not None:
            title = twitter_response.get("items")[i].get("title")
            similarity = round(jaro_similarity(channel_name.lower(), title.lower()), 2)

            if similarity >= 0.80:
                found = True
                break

    if not found:
        return found, None
    else:
        return found, link


def find_sources(channel_names, channel_IDs):
    pbar = tqdm(total=len(channel_names))
    pbar.set_description("Finding sources...")

    temp_list = []
    columns = [
        "channel_id", "channel_title",
        "profiles", "website", "social_media_presence",
        "vs"
    ]

    query_tail = [
        " LinkedIn",
        " Wiki",
        " Official Website",
        " Facebook",
        " Twitter"
    ]

    for channel_name in channel_names:

        linkedIn_found = find_linkedIn(channel_name, channel_name + query_tail[0])
        wiki_found = find_wiki(channel_name, channel_name + query_tail[1])
        site_found = find_website(channel_name, channel_name + query_tail[2])
        fb_found = find_fb(channel_name, channel_name + query_tail[3])
        twitter_found = find_twitter(channel_name, channel_name + query_tail[4])

        profiles = 0
        website = 0
        social_media_presence = 0

        if linkedIn_found[0] and wiki_found[0]:
            profile = 3
        elif linkedIn_found[0] and not wiki_found[0]:
            profile = 2
        elif not linkedIn_found[0] and wiki_found[0]:
            profile = 1

        if site_found[0]:
            website = 2

        if fb_found[0] or twitter_found[0]:
            social_media_presence = 1

        # '''
        record = [
            channel_name,  # channel_id
            channel_IDs.get(channel_name),  # channel_title
            profiles,  # profiles
            website,  # website
            social_media_presence,  # social_media_presence
            np.nan  # vs
        ]

        temp_list.append(record)

        # '''

        ''' For testing
        print(f"--- {channel_name} ---")
        print("PROFILES")
        print(f"LinkedIn: {linkedIn_found[1]}")
        print(f"Wiki: {wiki_found[1]}")
        print("")

        print("WEBSITE")
        print(f"Official Website: {site_found[1]}")
        print("")

        print("SOCIAL MEDIA PRESENCE")
        if fb_found[0]:
            print(f"Facebook: {fb_found[1]}")

        if twitter_found[0]:
            print(f"Twitter: {twitter_found[1]}")
        print("")
        # '''

        pbar.update(1)
    pbar.close()

    # TODO: Convert temp_list into DataFrame after loop
    pass


def get_vs(df):
    pass


def get_ranking(df):
    # ------------- SEARCHING ------------- #
    pass
    # ------------- SEARCHING ------------- #



if __name__ == '__main__':
    cont = True

    while cont:
        print("Working @ " + os.getcwd())
        print("     [1] Scrape videos from YouTube")
        print("     [2] Find external sources")
        print("     [3] Compute rankings and scores")
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
                print(f"File {filename} found.")

                channel_names = df["channel_title"].unique()
                channel_IDs = df[["channel_id", "channel_title"]].groupby("channel_title").first().to_dict().get("channel_id")

                find_sources(channel_names[0:5], channel_IDs)

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

                # Return to main folder
                os.chdir("..")
                os.chdir("..")

            except FileNotFoundError:
                print("File does not exist")

        elif choice == 4:
            cont = False
            print("")
            print("Ending program...")

        print("---")
        print("")
        sleep(1)





