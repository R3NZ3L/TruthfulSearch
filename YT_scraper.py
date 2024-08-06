# Google API Python Client by Google (n.d.)
# https://github.com/googleapis/google-api-python-client
from googleapiclient.discovery import build

# YouTube Transcript API by Jonas Depoix (2018)
# https://github.com/jdepoix/youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi

import pandas as pd
import numpy as np
from math import ceil
from tqdm import tqdm
import os

# Put your personal API key here
apiKey = ""

# YouTube API object
youtube = build('youtube', 'v3', developerKey=apiKey)


def yt_scrape():
    search_query = input("Search Query: ")
    num_videos = int(input("Number of Videos: "))
    filename = input("Filename (w/o .csv): ")

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
               "channel_id", "video_transcript"]
    
    temp_channel_list = []
    channel_info_columns = ["channel_id", "channel_name", "channel_dop", 
                            "sub_count", "total_videos"]
    
    temp_comment_list = []
    comment_columns = ['video_id', 'comment']

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
            
            video_transcript = ""

            try:
                transcript_dict = YouTubeTranscriptApi.get_transcript(video.get("id").get("videoId"), languages=['en'])
            except:
                video_transcript = np.nan
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

    path = os.getcwd() + "/datasets/" + filename

    # Saving to a .csv file
    print("Saving as videos as videos.csv...")
    print("Saving as channels as channels.csv...")
    print("Saving as comments as comments.csv...")

    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    finally:
        os.chdir(path)

    video_df.to_csv("videos.csv")
    channel_df.to_csv("channels.csv")
    comment_df.to_csv("comments.csv")
    print("Saved @ " + os.getcwd())
    print("Scraping complete.")


if __name__ == '__main__':
    print("Working @ " + os.getcwd())
    yt_scrape()

    os.chdir("..")
    os.chdir("..")
    print("Back @ " + os.getcwd())
