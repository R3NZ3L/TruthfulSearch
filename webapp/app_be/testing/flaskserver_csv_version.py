from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import re

app = Flask(__name__)
CORS(app)

mostVerifiedSort = ['Cannot be verified', 'Not so Verifiable', 'Somewhat Verifiable', 'Verifiable', 'Very Verifiable']

@app.route('/api/data', methods=['GET'])
def get_data():
    topic = request.args.get('topic')
    sort = request.args.get('sort')
    videos_path = "datasets/" + topic + "/videos.csv"
    channels_path = "datasets/" + topic + "/channels.csv"
    verifiability_path = "datasets/" + topic + "/verifiability_scores.csv"
    links_path = "datasets/" + topic + "/source_links.csv"
    raw_scores_path = "datasets/" + topic + "/vs_raw_scores.csv"
    channel_backlink_path = "datasets/" + topic + "/source_backlinks.csv"
    video_backlink_path = "datasets/" + topic + "/video_backlinks.csv"
    videos_df = pd.read_csv(videos_path).drop(['video_transcript', 'Unnamed: 0'], axis=1)
    videos_df = videos_df.drop_duplicates(keep='last')
    # fill nan values with 0 for numeric columns
    videos_df[videos_df.select_dtypes(include=[np.number]).columns] = videos_df.select_dtypes(include=[np.number]).fillna(0) 
    videos_df['thumbnail'] = videos_df['thumbnail'].fillna('https://c0.wallpaperflare.com/preview/287/460/40/black-black-and-white-cubes-dice.jpg')
    videos_df['description'] = videos_df['description'].fillna('').astype(str)
    channels_df = pd.read_csv(channels_path).drop(['Unnamed: 0'], axis=1)
    links_df = pd.read_csv(links_path).drop(['channel_name', 'Unnamed: 0'], axis=1).fillna('').astype(str)
    verifiability_df = pd.read_csv(verifiability_path).drop(['Unnamed: 0'], axis=1)
    channel_backlinks_df = pd.read_csv(channel_backlink_path).drop(['channel_name', 'Unnamed: 0'], axis=1)
    channel_backlinks_df.rename(columns={'Facebook': 'Facebook_backlink_count',
                                         'Wiki': 'Wiki_backlink_count',
                                         'Twitter': 'Twitter_backlink_count',
                                         'LinkedIn': 'LinkedIn_backlink_count',
                                         'Website': 'Website_backlink_count',
                                         }, inplace=True)
    video_backlinks_df = pd.read_csv(video_backlink_path).drop(['Unnamed: 0'], axis=1).drop_duplicates(subset=['video_id'], keep='last')
    links_df = pd.read_csv(links_path).drop(['channel_name', 'Unnamed: 0'], axis=1).fillna('').astype(str)
    raw_scores_df = pd.read_csv(raw_scores_path, usecols=['channel_id', 'p_desc', 'e_desc', 'li_desc', 'wi_desc', 'we_desc', 'tw_desc', 'fb_desc'])
    merged_df = videos_df.merge(channels_df, how='inner', on='channel_id').merge(verifiability_df, how='inner', on="channel_id").merge(links_df, how='inner', on='channel_id').merge(raw_scores_df, how='inner', on='channel_id')
    merged_df = merged_df.merge(channel_backlinks_df, how='inner', on='channel_id').merge(video_backlinks_df, how='inner', on='video_id')
    if sort == 'verifiability':
        merged_df['category'] = pd.Categorical(merged_df['category'], ordered=True, categories=mostVerifiedSort)
        merged_df = merged_df.sort_values('category', ascending=False)
    elif sort == 'upload_date':
        merged_df = merged_df.sort_values('video_dop', ascending=False)

    return(merged_df.to_dict(orient='records'))

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=105)
    app.run(host='0.0.0.0', port=105, debug=False)