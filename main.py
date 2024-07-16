import pandas as pd
import os
from YT_scraper import yt_scrape
from old_source_checker import find_sources
from TOPSIS import topsis
from TOPSIS import prepare_scores
# from backlinks import get_backlinks
from subjectivity import subjectivity

if __name__ == '__main__':
    print("Working @ " + os.getcwd())


    # ----- YOUTUBE SCRAPING -----
    yt_scrape()
    # ----------------------------

    print("Working @ " + os.getcwd())

    # ----- GOOGLE SERP SCRAPING -----
    try:
        print("Getting unchecked channels...")
        channel_df = pd.read_csv("unchecked.csv", index_col=0)
        os.remove("unchecked.csv")
        unchecked_exists = True
    except FileNotFoundError:
        channel_df = pd.read_csv("channels.csv", index_col=0)
        unchecked_exists = False
    finally:
        video_df = pd.read_csv("videos.csv", index_col=0)

    find_sources(channel_df, video_df, unchecked_exists)
    # --------------------------------



    # ----- BACKLINKS -----
    source_links = pd.read_csv("source_links.csv", index_col=0)

    get_backlinks(video_df, source_links)
    # ---------------------



    # ----- SUBJECTIVITY -----
    subjectivity(video_df)
    # ------------------------



    # ----- COMPUTING SCORES and RANKS -----
    topsis(prepare_scores(output="vs"), output="vs")
    topsis(prepare_scores(output="rank"), output="rank")
    # --------------------------------------



    # Return to main folder
    os.chdir("..")
    os.chdir("..")
    print("Back @ " + os.getcwd())



