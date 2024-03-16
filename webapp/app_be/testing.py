import numpy as np
import pandas as pd
import re

def getdata():
    filename = "covid_vaccine"
    videos_path = "datasets/" + filename + "/videos.csv"
    channels_path = "datasets/" + filename + "/channels.csv"
    verifiability_path = "datasets/" + filename + "/verifiability_scores.csv"
    links_path = "datasets/" + filename + "/source_links.csv"

    videos_df = pd.read_csv(videos_path).drop(['video_transcript', 'Unnamed: 0'], axis=1)
    videos_df = videos_df.drop_duplicates()
    # fill nan values with 0 for numeric columns
    videos_df[videos_df.select_dtypes(include=[np.number]).columns] = videos_df.select_dtypes(include=[np.number]).fillna(0) 
    videos_df['description'] = videos_df['description'].fillna('').astype(str)
    channels_df = pd.read_csv(channels_path).drop(['Unnamed: 0'], axis=1)
    links_df = pd.read_csv(links_path).drop(['channel_name', 'Unnamed: 0'], axis=1).fillna('').astype(str)
    verifiability_df = pd.read_csv(verifiability_path).drop(['Unnamed: 0'], axis=1)
    merged_df = videos_df.merge(channels_df, how='inner', on='channel_id').merge(verifiability_df, how='inner', on="channel_id").merge(links_df, how='inner', on='channel_id')
    
    print(merged_df.info())

getdata()