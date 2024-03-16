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
    
    videos_path = "datasets/" + "covid_philippines" + "/videos.csv"
    channels_path = "datasets/" + "covid_philippines" + "/channels.csv"

    videos_df = pd.read_csv(videos_path, usecols=['video_id'])['video_id'].tolist()
    channels_df = pd.read_csv(channels_path, usecols=['channel_id'])['channel_id'].tolist()
    thumbnail_links = []
    """
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
                    thumbnail_links.append(video.get('snippet').get('thumbnails').get('standard').get('url'))
                except:
                    thumbnail_links.append('https://play-lh.googleusercontent.com/zaMefYVID82FrctnM3g2b9Ul1Wk9cAR1aYfKNq_uvHnDbGo2wqZgliYVioi8Fa3YTA')

    pd.Series(thumbnail_links).to_csv('thumbnail_links', index=False, header=False)
    """

    """
    channel_profile_links = []
    while (len(channels_df) > 0):
        if(len(channels_df) >= 50):
            channels_request = youtube.channels().list(
                part=['snippet'],
                id=channels_df[0:50]
            )
            channels_df = channels_df[50:]
        else:
            channels_request = youtube.channels().list(
                part=['snippet'],
                id=channels_df[0:len(channels_df)]
            )
            channels_df = channels_df[len(channels_df):]

        channels_data = channels_request.execute()
        for channel in channels_data.get('items'):
                try:
                    channel_profile_links.append(channel.get('snippet').get('thumbnails').get('medium').get('url'))
                except:
                    channel_profile_links.append('https://play-lh.googleusercontent.com/zaMefYVID82FrctnM3g2b9Ul1Wk9cAR1aYfKNq_uvHnDbGo2wqZgliYVioi8Fa3YTA')

    pd.Series(channel_profile_links).to_csv('channel_profile_links', index=False, header=False)
    """
    
yt_assets_scrape()