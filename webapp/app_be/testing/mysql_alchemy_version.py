import numpy as np
import pandas as pd
import mysql.connector as connection
import sqlalchemy as db

mostVerifiedSort = ['Cannot be verified', 'Not so Verifiable', 'Somewhat Verifiable', 'Verifiable', 'Very Verifiable']

def getdata():
    try:
        engine = db.create_engine("mysql+pymysql://user:12345678@158.178.243.83:3306/covid_vaccine")
        dbConnection = engine.connect()
        videos_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM videos"))).drop(['video_transcript'], axis=1).drop_duplicates(keep='last')
        videos_df[videos_df.select_dtypes(include=[np.number]).columns] = videos_df.select_dtypes(include=[np.number]).fillna(0) 
        videos_df['thumbnail'] = videos_df['thumbnail'].fillna('https://c0.wallpaperflare.com/preview/287/460/40/black-black-and-white-cubes-dice.jpg')
        videos_df['description'] = videos_df['description'].fillna('').astype(str)
        channels_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM channels")))
        links_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM source_links"))).drop(['channel_name'], axis=1).fillna('').astype(str)
        verifiability_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM verifiability_scores")))
        channel_backlinks_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM source_backlinks"))).drop(['channel_name'], axis=1)
        channel_backlinks_df.rename(columns={'Facebook': 'Facebook_backlink_count',
                                            'Wiki': 'Wiki_backlink_count',
                                            'Twitter': 'Twitter_backlink_count',
                                            'LinkedIn': 'LinkedIn_backlink_count',
                                            'Website': 'Website_backlink_count',
                                            }, inplace=True)
        video_backlinks_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM video_backlinks"))).drop_duplicates(subset=['video_id'], keep='last')
        raw_scores_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM vs_raw_scores")))[['channel_id', 'p_desc', 'e_desc', 'li_desc', 'wi_desc', 'we_desc', 'tw_desc', 'fb_desc']]
        merged_df = videos_df.merge(channels_df, how='inner', on='channel_id').merge(verifiability_df, how='inner', on="channel_id").merge(links_df, how='inner', on='channel_id').merge(raw_scores_df, how='inner', on='channel_id')
        merged_df = merged_df.merge(channel_backlinks_df, how='inner', on='channel_id').merge(video_backlinks_df, how='inner', on='video_id')
        print(merged_df)
        dbConnection.close()
    except Exception as e:
        dbConnection.close()
        print(str(e))

getdata()