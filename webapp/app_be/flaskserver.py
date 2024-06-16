from flask import Flask, request, Response
from flask import jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import sqlalchemy as db
import json

app = Flask(__name__)
CORS(app)

mostVerifiedSort = ['Cannot be verified', 'Not so Verifiable', 'Somewhat Verifiable', 'Verifiable', 'Very Verifiable']

@app.route('/', methods=['GET'])
def hello():
    return 'Truthful Search API Homepage'

@app.route('/api/data_main', endpoint='data_main', methods=['GET'])
@app.route('/api/data_extension', endpoint='data_extension', methods=['GET'])
def get_data():
    if (request.endpoint == 'data_main'):
        try:
            dbConnection = None
            topic = request.args.get('topic')
            sort = request.args.get('sort')
            engine = db.create_engine("mysql+pymysql://user:12345678@18.142.50.165:3306/" + topic)
            dbConnection = engine.connect()
            videos_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM videos"))).drop(['video_transcript'], axis=1).drop_duplicates(keep='last')
            videos_df[videos_df.select_dtypes(include=[np.number]).columns] = videos_df.select_dtypes(include=[np.number]).fillna(0) 
            videos_df['thumbnail'] = videos_df['thumbnail'].replace('', 'https://c0.wallpaperflare.com/preview/287/460/40/black-black-and-white-cubes-dice.jpg')
            videos_df['description'] = videos_df['description'].fillna('').astype(str)
            channels_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM channels")))
            links_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM source_links"))).drop(['channel_name'], axis=1).replace({'nan': pd.NA}).fillna('').astype(str)         
            verifiability_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM verifiability_scores")))
            channel_backlinks_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM source_backlinks"))).drop(['channel_name'], axis=1)
            channel_backlinks_df.rename(columns={'Facebook': 'Facebook_backlink_count',
                                                'Wiki': 'Wiki_backlink_count',
                                                'Twitter': 'Twitter_backlink_count',
                                                'LinkedIn': 'LinkedIn_backlink_count',
                                                'Website': 'Website_backlink_count',
                                                'Instagram': 'Instagram_backlink_count'
                                                }, inplace=True)
            video_backlinks_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM video_backlinks"))).drop_duplicates(subset=['video_id'], keep='last')
            raw_scores_df = pd.DataFrame(dbConnection.execute(db.text("SELECT * FROM vs_raw_scores")))[['channel_id', 'p_desc', 'e_desc', 'li_desc', 'wi_desc', 'we_desc', 'tw_desc', 'fb_desc', 'insta_desc']]
            merged_df = videos_df.merge(channels_df, how='inner', on='channel_id').merge(verifiability_df, how='inner', on="channel_id").merge(links_df, how='inner', on='channel_id').merge(raw_scores_df, how='inner', on='channel_id')
            merged_df = merged_df.merge(channel_backlinks_df, how='inner', on='channel_id').merge(video_backlinks_df, how='inner', on='video_id')

            if sort == 'verifiability':
                merged_df['category'] = pd.Categorical(merged_df['category'], ordered=True, categories=mostVerifiedSort)
                merged_df = merged_df.sort_values('category', ascending=False)
            elif sort == 'upload_date':
                merged_df = merged_df.sort_values('video_dop', ascending=False)
            dbConnection.close()

            return(merged_df.to_dict(orient='records'))
        except Exception as e:
            if(dbConnection != None): dbConnection.close()
            return Response(response='Database Connection Error', status=500) # Database Connection Error

    elif(request.endpoint == 'data_extension'):
        try:
            dbConnection = None
            id = request.args.get('id')
            covid_philippines_engine = db.create_engine("mysql+pymysql://user:12345678@18.142.50.165:3306/covid_philippines")
            covid_philippines_dbConnection = covid_philippines_engine.connect()
            covid_philippines = covid_philippines_dbConnection.execute(db.text("SELECT video_id FROM videos WHERE video_id = :id"), {'id': id}).fetchall()
            if (len(covid_philippines) != 0): # if found in covid_philippines database
                dbConnection = covid_philippines_dbConnection
            else:
                covid_vaccine_engine = db.create_engine("mysql+pymysql://user:12345678@18.142.50.165:3306/covid_vaccine")
                covid_vaccine_dbConnection = covid_vaccine_engine.connect()
                covid_vaccine = covid_vaccine_dbConnection.execute(db.text("SELECT video_id FROM videos WHERE video_id = :id"), {'id': id}).fetchall()
                if(len(covid_vaccine) != 0): # if found in covid_vaccine database
                    dbConnection = covid_vaccine_dbConnection
                else:
                    israel_palestine_engine = db.create_engine("mysql+pymysql://user:12345678@18.142.50.165:3306/israel_palestine_conflict_history")
                    israel_palestine_dbConnection = israel_palestine_engine.connect()
                    israel_palestine = israel_palestine_dbConnection.execute(db.text("SELECT video_id FROM videos WHERE video_id = :id"), {'id': id}).fetchall()
                    if(len(israel_palestine) != 0): # if found in israel_palestine database
                        dbConnection = israel_palestine_dbConnection
            
            if(dbConnection != None):
                videos_df = pd.DataFrame(dbConnection.execute(
                    db.text("""SELECT v.video_title, c.channel_name, c.channel_dop, c.sub_count, c.total_videos,
                                c.profile, vs.vs, vs.category, sl.Facebook, sl.LinkedIn, sl.Twitter, sl.Website,
                                sl.Wiki, sl.Instagram, sb.Facebook as Facebook_backlink_count, sb.LinkedIn as LinkedIn_backlink_count,
                                sb.Twitter as Twitter_backlink_count, sb.Website as Website_backlink_count, sb.Wiki as Wiki_backlink_count, 
                                sb.Instagram as Instagram_backlink_count, vrs.e_desc, vrs.fb_desc, vrs.li_desc, vrs.p_desc, vrs.tw_desc, 
                                vrs.we_desc, vrs.wi_desc, vrs.insta_desc, vb.backlinks
                                FROM videos as v 
                                INNER JOIN channels as c on v.channel_id=c.channel_id
                                INNER JOIN verifiability_scores as vs on v.channel_id=vs.channel_id
                                INNER JOIN vs_raw_scores as vrs on v.channel_id=vrs.channel_id
                                INNER JOIN source_links as sl on v.channel_id=sl.channel_id
                                INNER JOIN source_backlinks as sb on v.channel_id=sb.channel_id
                                INNER JOIN video_backlinks as vb on v.video_id=vb.video_id
                                WHERE v.video_id = :id"""), {'id': id})).drop_duplicates(keep='last')
                videos_df[['LinkedIn', 'Facebook', 'Twitter', 'Website', 'Wiki', 'Instagram']] = videos_df[['LinkedIn', 'Facebook', 'Twitter', 'Website', 'Wiki', 'Instagram']].replace({'nan': pd.NA}).fillna('').astype(str)
                dbConnection.close()
                return(videos_df.to_dict(orient='records')[0])
            else:
                return Response(response='Data does not exist in any of the database', status=404) 
        except Exception as e:
            if(dbConnection != None): dbConnection.close()
            return Response(response='Database Connection Error', status=500) # Database Connection Error

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=105)
    app.run(host='0.0.0.0', port=105, debug=True)