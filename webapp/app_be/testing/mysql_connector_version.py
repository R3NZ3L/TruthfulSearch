import numpy as np
import pandas as pd
import mysql.connector as connection
from sqlalchemy import create_engine

mostVerifiedSort = ['Cannot be verified', 'Not so Verifiable', 'Somewhat Verifiable', 'Verifiable', 'Very Verifiable']

def getdata():
    try:
        mydb = connection.connect(host="158.178.243.83", database = 'covid_vaccine', user="user", passwd="12345678",use_pure=True)
        videos_query = "Select * from videos"
        channels_query = "Select * from channels"
        verifiability_query = "Select * from verifiability_scores"
        source_links_query = "Select * from source_links"
        channel_backlinks_query = "Select * from source_backlinks"
        video_backlinks_query = "Select * from video_backlinks"
        raw_scores_query = "Select * from vs_raw_scores"
        videos_df = pd.read_sql(videos_query,mydb).drop(['video_transcript'], axis=1).drop_duplicates(keep='last')
        videos_df[videos_df.select_dtypes(include=[np.number]).columns] = videos_df.select_dtypes(include=[np.number]).fillna(0) 
        videos_df['thumbnail'] = videos_df['thumbnail'].fillna('https://c0.wallpaperflare.com/preview/287/460/40/black-black-and-white-cubes-dice.jpg')
        videos_df['description'] = videos_df['description'].fillna('').astype(str)
        channels_df = pd.read_sql(channels_query,mydb)
        links_df = pd.read_sql(source_links_query,mydb).fillna('').astype(str)
        verifiability_df = pd.read_sql(verifiability_query,mydb)
        channel_backlinks_df = pd.read_sql(channel_backlinks_query,mydb).drop(['channel_name'], axis=1)
        channel_backlinks_df.rename(columns={'Facebook': 'Facebook_backlink_count',
                                            'Wiki': 'Wiki_backlink_count',
                                            'Twitter': 'Twitter_backlink_count',
                                            'LinkedIn': 'LinkedIn_backlink_count',
                                            'Website': 'Website_backlink_count',
                                            }, inplace=True)
        video_backlinks_df = pd.read_sql(video_backlinks_query,mydb).drop_duplicates(subset=['video_id'], keep='last')
        raw_scores_df = pd.read_sql(raw_scores_query, mydb, columns=['channel_id', 'p_desc', 'e_desc', 'li_desc', 'wi_desc', 'we_desc', 'tw_desc', 'fb_desc'])
        merged_df = videos_df.merge(channels_df, how='inner', on='channel_id').merge(verifiability_df, how='inner', on="channel_id").merge(links_df, how='inner', on='channel_id').merge(raw_scores_df, how='inner', on='channel_id')
        merged_df = merged_df.merge(channel_backlinks_df, how='inner', on='channel_id').merge(video_backlinks_df, how='inner', on='video_id')
        
        print(merged_df)
        mydb.close()
    except Exception as e:
        mydb.close()
        print(str(e))


getdata()