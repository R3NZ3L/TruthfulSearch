# Google API Python Client by Google (n.d.)
# https://github.com/googleapis/google-api-python-client
from googleapiclient.discovery import build

import pandas as pd
import numpy as np
import os
import time
import random

# Put your personal API key here
# DLSU account key
apiKey = 'AIzaSyBTRvkhM6ESdLHu0djfP39-IKHufQogxOI' # Baura

# YouTube API object
youtube = build('youtube', 'v3', developerKey=apiKey)


def yt_assets_scrape():
    
    filename = input("Filename (w/o .csv): ")
    path = os.getcwd() + "/datasets/" + filename
    os.chdir(path)

    videos_path =  "videos.csv"
    channels_path = "channels.csv"

    videos_df = pd.read_csv(videos_path, usecols=['video_id'])['video_id'].tolist()
    complete_videos_df = pd.read_csv(videos_path).drop(['Unnamed: 0'], axis=1)
    channels_df = pd.read_csv(channels_path, usecols=['channel_id'])['channel_id'].tolist()
    complete_channels_df = pd.read_csv(channels_path).drop(['Unnamed: 0'], axis=1)

    thumbnail_links = []
    print(channels_df)
    
    while (len(videos_df) > 0):
        if(len(videos_df) >= 50):

            video_request = youtube.videos().list(
                part=['snippet'],
                id=videos_df[0:50]
            )
            videos_df = videos_df[50:]
        else:
            video_request = youtube.videos().list(
                part=['snippet'],
                id=videos_df[0:len(videos_df)]
            )
            videos_df = videos_df[len(videos_df):]

        video_data = video_request.execute()
        for video in video_data.get('items'):
            try:
                thumbnail_links.append(video.get('snippet').get('thumbnails').get('high').get('url'))
            except:
                thumbnail_links.append('https://play-lh.googleusercontent.com/zaMefYVID82FrctnM3g2b9Ul1Wk9cAR1aYfKNq_uvHnDbGo2wqZgliYVioi8Fa3YTA')

    complete_videos_df['thumbnail'] = pd.Series(thumbnail_links)

    channel_profile_links = []
    """
    while (len(channels_df) > 0):
        channels_request = youtube.channels().list(
            part=['snippet'],
            id=channels_df.pop(0)
        )
        channels_data = channels_request.execute()

        try:
            channel_profile_links.append(channels_data.get('items')[0].get('snippet').get('thumbnails').get('medium').get('url'))
        except:
            channel_profile_links.append('https://play-lh.googleusercontent.com/zaMefYVID82FrctnM3g2b9Ul1Wk9cAR1aYfKNq_uvHnDbGo2wqZgliYVioi8Fa3YTA')

    complete_channels_df['profile'] = pd.Series(channel_profile_links)
    print(channel_profile_links)
    """
    complete_videos_df.to_csv('videos.csv')
    """
    complete_channels_df.to_csv('channels.csv')
    """
    os.chdir("..")
    os.chdir("..")
    print("Back @ " + os.getcwd())

yt_assets_scrape()