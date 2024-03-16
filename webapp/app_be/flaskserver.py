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
    videos_df = pd.read_csv(videos_path).drop(['video_transcript', 'Unnamed: 0'], axis=1)
    videos_df = videos_df.drop_duplicates()
    # fill nan values with 0 for numeric columns
    videos_df[videos_df.select_dtypes(include=[np.number]).columns] = videos_df.select_dtypes(include=[np.number]).fillna(0) 
    videos_df['description'] = videos_df['description'].fillna('').astype(str)
    channels_df = pd.read_csv(channels_path).drop(['Unnamed: 0'], axis=1)
    links_df = pd.read_csv(links_path).drop(['channel_name', 'Unnamed: 0'], axis=1).fillna('').astype(str)
    verifiability_df = pd.read_csv(verifiability_path).drop(['Unnamed: 0'], axis=1)
    raw_scores_df = pd.read_csv(raw_scores_path, usecols=['channel_id', 'p_desc', 'e_desc', 'li_desc', 'wi_desc', 'we_desc', 'tw_desc', 'fb_desc'])
    merged_df = videos_df.merge(channels_df, how='inner', on='channel_id').merge(verifiability_df, how='inner', on="channel_id").merge(links_df, how='inner', on='channel_id').merge(raw_scores_df, how='inner', on='channel_id')
    if sort == 'verifiability':
        merged_df['category'] = pd.Categorical(merged_df['category'], ordered=True, categories=mostVerifiedSort)
        merged_df = merged_df.sort_values('category', ascending=False)
    elif sort == 'upload_date':
        merged_df = merged_df.sort_values('video_dop', ascending=False)

    return(merged_df.to_dict(orient='records'))

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=105)
    app.run(host='0.0.0.0', port=105, debug=False)