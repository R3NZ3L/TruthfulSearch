from flask import Flask, request
from flask import jsonify

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


app = Flask(__name__)

@app.route('/returnmesomedata/', methods=['GET'])
def call_yt_scrape():
    var1 = request.args.get('name')
    var2 = int(request.args.get('name2'))
    var3 = request.args.get('name3')
    try:
        yt_scrape(var1, var2, var3)
        return "Nice"
    except:
        return "YT scrape failed"


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)