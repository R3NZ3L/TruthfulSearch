from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
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

    return(merged_df.to_dict(orient='records'))

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=105)
    app.run(host='0.0.0.0', port=105, debug=False)