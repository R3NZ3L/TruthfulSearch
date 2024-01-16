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

# Put your personal API key here
apiKey = 'AIzaSyCIplXpNgYZ2IS44ZYyEi-hXRu1gzl9I58'

# YouTube API object
youtube = build('youtube', 'v3', developerKey=apiKey)


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


def scrape():
    # Storing data in a numpy array of lists
    # ------------- SCRAPING ------------- #
    search_query = input("Search Query: ")
    num_videos = int(input("Number of Videos: "))
    filename = input("Filename (.csv): ")

    print("")

    if num_videos < 50:
        num_pages = 1
    else:
        num_pages = ceil(num_videos / 50)

    search_request = youtube.search().list(
        part="snippet",
        q=search_query,
        type="video",
        maxResults=50,
        order="relevance",
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
            temp_list = []

            # video_id
            temp_list.append(video.get("id").get("videoId"))

            # video_title
            temp_list.append(metadata.get("title"))

            # description
            temp_list.append(repr(vid_specs.get("items")[0].get("snippet").get("description")))

            # video_dop
            temp_list.append(metadata.get("publishedAt")[:10])

            # view_count
            temp_list.append(vid_specs.get("items")[0].get("statistics").get("viewCount"))

            # like_count
            temp_list.append(vid_specs.get("items")[0].get("statistics").get("likeCount"))

            # comment_count
            try:
                temp_list.append(vid_specs.get("items")[0].get("statistics").get("commentCount"))
            except:
                temp_list.append("N/A")

            '''
                        columns = ["video_id", "video_title", "description", "video_dop",
                           "view_count", "like_count", "comment_count",
                           "channel_id", "channel_title", "channel_dop", "sub_count",
                           "total_videos"]
                        '''

            # channel_id
            temp_list.append(metadata.get("channelId"))

            # channel_title
            temp_list.append(metadata.get("channelTitle"))

            # channel_dop
            temp_list.append(channel_specs.get("items")[0].get("snippet").get("publishedAt")[:10])

            # sub_count
            temp_list.append(channel_specs.get("items")[0].get("statistics").get("subscriberCount"))

            # total_videos
            temp_list.append(channel_specs.get("items")[0].get("statistics").get("videoCount"))

            temp_video_list.append(temp_list)

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
    df.to_csv("datasets/" + filename + ".csv")
    print("Complete.")


if __name__ == '__main__':
    # Search test (uncomment line below to test search)
    # search_test()

    # Making a dataset
    scrape()
