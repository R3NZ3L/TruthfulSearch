import numpy as np
import pandas as pd
import re

def getdata():
    videos_path = "datasets/" + "covid_philippines" + "/videos.csv"
    channels_path = "datasets/" + "covid_philippines" + "/channels.csv"
    links_path = "datasets/" + "covid_philippines" + "/source_links.csv"
    verifiability_path = "datasets/" + "covid_philippines" + "/verifiability_scores.csv"

    videos_df = pd.read_csv(videos_path).drop(['video_transcript', 'Unnamed: 0'], axis=1)
    videos_df = videos_df.drop_duplicates()
    videos_df['description'] = videos_df['description'].fillna('').astype(str)
    channels_df = pd.read_csv(channels_path).drop(['Unnamed: 0'], axis=1)
    verifiability_df = pd.read_csv(verifiability_path).drop(['Unnamed: 0'], axis=1)
    merged_df = videos_df.merge(channels_df, how='inner', on='channel_id').merge(verifiability_df, how='inner', on="channel_id")
    
    print(merged_df.columns)

getdata()