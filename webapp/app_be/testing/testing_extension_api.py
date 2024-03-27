import pandas as pd
import sqlalchemy as db
import numpy as np

id = 'aLZ85hb4wjE'
#id = 'aLZ85hb4wjEaLZ85hb4wjE'

try:
    dbConnection = None
    covid_philippines_engine = db.create_engine("mysql+pymysql://user:12345678@158.178.243.83:3306/covid_philippines")
    covid_philippines_dbConnection = covid_philippines_engine.connect()
    covid_philippines = covid_philippines_dbConnection.execute(db.text("SELECT video_id FROM videos WHERE video_id = :id"), {'id': id}).fetchall()
    if (len(covid_philippines) != 0): # if found in covid_philippines database
        dbConnection = covid_philippines_dbConnection
    else:
        covid_vaccine_engine = db.create_engine("mysql+pymysql://user:12345678@158.178.243.83:3306/covid_vaccine")
        covid_vaccine_dbConnection = covid_vaccine_engine.connect()
        covid_vaccine = covid_vaccine_dbConnection.execute(db.text("SELECT video_id FROM videos WHERE video_id = :id"), {'id': id}).fetchall()
        if(len(covid_vaccine) != 0): # if found in covid_vaccine database
            dbConnection = covid_vaccine_dbConnection
        else:
            israel_palestine_engine = db.create_engine("mysql+pymysql://user:12345678@158.178.243.83:3306/israel_palestine_conflict_history")
            israel_palestine_dbConnection = israel_palestine_engine.connect()
            israel_palestine = israel_palestine_dbConnection.execute(db.text("SELECT video_id FROM videos WHERE video_id = :id"), {'id': id}).fetchall()
            if(len(covid_vaccine) != 0): # if found in israel_palestine database
                dbConnection = israel_palestine_dbConnection
    if(dbConnection != None):
        videos_df = pd.DataFrame(dbConnection.execute(
            db.text("""SELECT v.video_title, c.channel_name, c.channel_dop, c.sub_count, c.total_videos,
                        c.profile, vs.vs, vs.category, sl.Facebook, sl.LinkedIn, sl.Twitter, sl.Website,
                        sl.Wiki, sb.Facebook as Facebook_backlink_count, sb.LinkedIn as LinkedIn_backlink_count,
                        sb.Twitter as Twitter_backlink_count, sb.Website as Website_backlink_count, sb.Wiki as Wiki_backlink_count,
                        vrs.e_desc, vrs.fb_desc, vrs.li_desc, vrs.p_desc, vrs.tw_desc, vrs.we_desc, vrs.wi_desc,
                        vb.backlinks
                        FROM videos as v 
                        INNER JOIN channels as c on v.channel_id=c.channel_id
                        INNER JOIN verifiability_scores as vs on v.channel_id=vs.channel_id
                        INNER JOIN vs_raw_scores as vrs on v.channel_id=vrs.channel_id
                        INNER JOIN source_links as sl on v.channel_id=sl.channel_id
                        INNER JOIN source_backlinks as sb on v.channel_id=sb.channel_id
                        INNER JOIN video_backlinks as vb on v.video_id=vb.video_id
                        WHERE v.video_id = :id"""), {'id': id})).drop_duplicates(keep='last')
        dbConnection.close()
        print(videos_df == None)
    else:
        print('Not Found in Database')

except Exception as e:
    if(dbConnection != None): dbConnection.close()
    print(str(e))





