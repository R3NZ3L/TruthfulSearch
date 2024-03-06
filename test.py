import pandas as pd
import os
from YT_scraper import yt_scrape
from source_checker import find_sources
from TOPSIS import topsis
from TOPSIS import prepare_scores
from backlinks import get_backlinks

if __name__ == '__main__':
    yt_scrape()
