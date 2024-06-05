# Google API Python Client by Google (n.d.)
# https://github.com/googleapis/google-api-python-client
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from jellyfish import jaro_similarity

import pandas as pd
import numpy as np
from tqdm import tqdm
import regex as re
import requests
from bs4 import BeautifulSoup
import json
import os

# Put your personal API key here
# DLSU account key
apiKey = 'AIzaSyCIplXpNgYZ2IS44ZYyEi-hXRu1gzl9I58' # Aldecoa
# apiKey = 'AIzaSyCJBMIMpGpBdmTkx7SRhObSNAyV_aRSjho' # Aquino
# apiKey = 'AIzaSyBTRvkhM6ESdLHu0djfP39-IKHufQogxOI' # Baura
# apiKey = 'AIzaSyA7eqxwuzM6SUDDVTss6DSzKGEt7kSJesg' # Sevillana

# Search engine ID
cseKey = "23c1c70a203ac4852" # Aldecoa
# cseKey = "a7c987e23f0fe448e" # Aquino
# cseKey = "76c19208b12de4763" # Baura
# cseKey = "a674809398a7b46df" # Sevillana

# Google Custom Search API
google_resource = build("customsearch", "v1", developerKey=apiKey).cse()

quota_reached = False
stopped_at = None

