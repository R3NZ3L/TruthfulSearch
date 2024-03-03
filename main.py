import pandas as pd
import os
from YT_scraper import yt_scrape
from source_checker import find_sources
from TOPSIS import topsis
from TOPSIS import prepare_scores
from backlinks import get_backlinks

if __name__ == '__main__':
    print("Working @ " + os.getcwd())

    # ----- SCRAPING -----
    search_query = input("Search Query: ")
    num_videos = int(input("Number of Videos: "))
    filename = input("Filename (w/o .csv): ")

    yt_scrape(search_query, num_videos, filename)
    # --------------------

    print("Working @ " + os.getcwd())

    # ----- GETTING SOURCES -----
    video_df = pd.read_csv("videos.csv").drop("Unnamed: 0", axis=1)
    channel_df = pd.read_csv("channels.csv").drop("Unnamed: 0", axis=1)

    find_sources(channel_df, video_df)

    source_links = pd.read_csv("source_links.csv").drop("Unnamed: 0", axis=1)

    get_backlinks(video_df, source_links)
    # ---------------------------



    # ----- COMPUTING SCORES -----
    source_backlinks = pd.read_csv("source_backlinks.csv").drop("Unnamed: 0", axis=1)
    source_check = pd.read_csv("source_check.csv").drop("Unnamed: 0", axis=1)

    topsis(prepare_scores(source_check, source_backlinks))
    # ----------------------------



    # ----- COMPUTING RANKS -----

    # ---------------------------

    # Return to main folder
    os.chdir("..")
    os.chdir("..")



