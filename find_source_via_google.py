# Google API Python Client by Google (n.d.)
# https://github.com/googleapis/google-api-python-client
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from jellyfish import jaro_similarity

import pandas as pd
import numpy as np
from tqdm import tqdm
import regex as re
import os
import time

# Put your personal API key here
# DLSU account key
# apiKey = 'AIzaSyCIplXpNgYZ2IS44ZYyEi-hXRu1gzl9I58' # Aldecoa
# apiKey = 'AIzaSyCl5w8PQxEpIN8cdePhSXfD9-UDWOpDiV8' # 2nd acct Aldecoa
#apiKey = 'AIzaSyDrA3VG9qxJOSxgcQKpcuQgjQVA1XjtpbQ' # 3rd acct Aldecoa
# apiKey = 'AIzaSyCJBMIMpGpBdmTkx7SRhObSNAyV_aRSjho' # Aquino
apiKey = 'AIzaSyDZlAPC29rxMjh-gu-ZfgTPb8wrRLglrs4' # 2nd acct Aquino
# apiKey = 'AIzaSyAZxwwAfgVoTSys4HCiirvs-h0ynph-rmU' # 3rd acct Aquino
# apiKey = 'AIzaSyDKBteFADAddCvCCvEKrfJRFSxc-ovflsQ' # Baura
# apiKey = 'AIzaSyAPvryNBQ3TkXwqBJdW9_0AkhhCYZRtA2c' # Sevillana

# Search engine ID
#cseKey = "23c1c70a203ac4852" # Aldecoa
cseKey = "a7c987e23f0fe448e" # Aquino
# cseKey = "05e988b88095c4deb" # Baura
# cseKey = "f465f751a15a34c35" # Sevillana

# Google Custom Search API
google_resource = build("customsearch", "v1", developerKey=apiKey).cse()

quota_reached = False


def find_linkedIn(channel_name, query):
    found = False
    pattern = r'https:\/\/(www\.)?linkedin\.com\/(company|in)\/.+'  # Used to find specific profile links

    try:
        li_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            try:
                link = li_response.get("items")[i].get("formattedUrl")
                if re.search(pattern, link) is not None:
                    # Get profile name from search result
                    match = re.search(r'\w+\s(\w+)?', li_response.get("items")[i].get("title"))
                    if match is not None:
                        profile_name = match.group()

                        # Get similarity between found profile name and channel name
                        # This is to prevent false positives in finding a LinkedIn profile
                        similarity = round(jaro_similarity(channel_name.lower(), profile_name.lower()), 2)

                        # If n% similar, consider LinkedIn profile as found
                        if similarity >= 0.80:
                            found = True
                            break
            except IndexError:
                break

    except HttpError:
        global quota_reached
        if not quota_reached:
            quota_reached = True

    if not found:
        return found, np.nan
    else:
        return found, link


def find_wiki(channel_name, query):
    found = False
    pattern = r'https:\/\/\w{2}.wikipedia\.org\/wiki\/.+'

    try:
        wiki_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            try:
                link = wiki_response.get("items")[i].get("formattedUrl")
                if re.search(pattern, link) is not None:
                    # Get Wiki page name from search result
                    title = wiki_response.get("items")[i].get("title")
                    match = re.search(r'.+(?=\s-\sWikipedia)', title)
                    if match is not None:
                        page_name = match.group()

                        # Get similarity between found Wiki page name and channel name
                        # This is to prevent false positives in finding a Wiki page
                        similarity = round(jaro_similarity(channel_name.lower(), page_name.lower()), 2)

                        # If n% similar, consider Wiki page as found
                        if similarity >= 0.80:
                            found = True
                            break
            except IndexError:
                break

    except HttpError:
        global quota_reached
        if not quota_reached:
            quota_reached = True

    if not found:
        return found, np.nan
    else:
        return found, link


def find_website(channel_name, query):
    found = False
    # RegEx to exclude YouTube, LinkedIn, and Wikipedia pages
    pattern = r'https\:\/\/(\w{2}.wikipedia\.org\/wiki\/.+|www\.(youtube\.com.+|linkedin\.com.+))'

    try:
        website_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            try:
                title = website_response.get("items")[i].get("title")
                link = website_response.get("items")[i].get("link")
                if title.lower() in channel_name.lower():
                    if re.search(pattern, link) is None:
                        # The first result among the filtered at this point is MOST LIKELY the official website
                        found = True
                        break
            except IndexError:
                break

    except HttpError:
        global quota_reached
        if not quota_reached:
            quota_reached = True

    if not found:
        return found, np.nan
    else:
        return found, link


def find_fb(channel_name, query):
    found = False
    pattern = r'^https\:\/\/(www\.)?facebook\.com\/.+\/'

    try:
        fb_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            try:
                link = fb_response.get("items")[i].get("formattedUrl")
                if re.search(pattern, link) is not None:
                    title = fb_response.get("items")[i].get("title")
                    similarity = round(jaro_similarity(channel_name.lower(), title.lower()), 2)

                    if similarity >= 0.80:
                        found = True
                        break
            except IndexError:
                break

    except HttpError:
        global quota_reached
        if not quota_reached:
            quota_reached = True

    if not found:
        return found, np.nan
    else:
        return found, link


def find_twitter(channel_name, query):
    found = False
    pattern = r'https\:\/\/(twitter|x)\.com\/.+'

    try:
        twitter_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            try:
                link = twitter_response.get("items")[i].get("formattedUrl")
                if re.search(pattern, link) is not None:
                    title = twitter_response.get("items")[i].get("title")
                    # Remove filler text after actual name of profile
                    title = re.sub(r'\s\(@.+', "", title)
                    similarity = round(jaro_similarity(channel_name.lower(), title.lower()), 2)

                    if similarity >= 0.80:
                        found = True
                        break
            except IndexError:
                break

    except HttpError:
        global quota_reached
        if not quota_reached:
            quota_reached = True

    if not found:
        return found, np.nan
    else:
        return found, link


def find_instagram(channel_name, query):
    found = False
    pattern = r'https:\/\/(www\.)?instagram\.com\/.+'

    try:
        instagram_response = google_resource.list(
            q=query,
            cx=cseKey
        ).execute()

        for i in range(0, 10):
            try:
                link = instagram_response.get("items")[i].get("formattedUrl")
                if re.search(pattern, link) is not None:
                    title = instagram_response.get("items")[i].get("title")
                    # Remove filler text after actual name of profile
                    title = re.sub(r'\s\(@.+', "", title)
                    similarity = round(jaro_similarity(channel_name.lower(), title.lower()), 2)

                    if similarity >= 0.80:
                        found = True
                        break
            except IndexError:
                break

    except HttpError:
        global quota_reached
        if not quota_reached:
            quota_reached = True

    if not found:
        return found, np.nan
    else:
        return found, link


def find_sources_via_google(sc, sl, unchecked_exists):
    global quota_reached

    sc = sc.fillna('')
    sl = sl.fillna('')

    if unchecked_exists[0]:
        queries = unchecked_exists[1]
    else:
        queries = pd.DataFrame(columns=["pos", "channel_name", "source"])
        for i in range(sc.shape[0]):
            for column in sc.columns[2:]:
                if not sc.iloc[i][column]:
                    channel_name = sc.iloc[i]["channel_name"]
                    data = {"pos": [i], "channel_name": [channel_name], "source": [column]}
                    row = pd.DataFrame.from_dict(data)
                    queries = pd.concat([queries, row], axis=0, ignore_index=True)

    print(f"Trying to look for {queries.shape[0]} missing sources via Google...")

    pbar = tqdm(total=queries.shape[0])
    pbar.set_description("Finding sources on Google...")
    i = 0
    ended_on = 0

    for i in range(queries.shape[0]):
        if quota_reached:
            break
        else:
            pos = queries.iloc[i]["pos"]
            channel_name = queries.iloc[i]["channel_name"]
            source = queries.iloc[i]["source"]
            query = str(channel_name + " " + source)
            # print(f"[{i}] {query}")
            found, link = (False, np.nan)

            # '''
            if source == "LinkedIn":
                found, link = find_linkedIn(channel_name, query)
            elif source == "Wiki":
                found, link = find_wiki(channel_name, query)
            elif source == "Website":
                found, link = find_website(channel_name, query)
            elif source == "Twitter":
                found, link = find_twitter(channel_name, query)
            elif source == "Facebook":
                found, link = find_fb(channel_name, query)
            elif source == "Instagram":
                found, link = find_instagram(channel_name, query)
            # '''

            time.sleep(1)

            if quota_reached:
                # print(f"{found}, {link}")
                print(f"CSE quota met at index [{i}], query [{query}]")
                ended_on = i
                break
            else:
                '''
                Even when quota is met, script still passes through here for some reason.
                Assumption is that the quota_reached edit from the find_XXXXX functions doesn't
                push through.
                
                Band-aid solution is to check for the status of the variable twice, as seen below.
                '''
                # print(f"{found}: {link}")

                time.sleep(1)

                if quota_reached:
                    # print(f"{found}, {link}")
                    print(f"CSE quota met at index [{i}], query [{query}]")
                    ended_on = i
                    break
                else:
                    sc.at[pos, source] = found
                    sl.at[pos, source] = link
                    pbar.update(1)

    pbar.close()

    if i == queries.shape[0] - 1:
        print("All queries processed")
    else:
        queries = queries.iloc[ended_on:]
        unchecked = queries.shape[0]
        print(f"Queries left: {unchecked}")
        print("Saving unchecked sources as unchecked.csv...")
        queries.to_csv("unchecked.csv")

    print("Saving changes to checklist and links...")
    sc.to_csv("source_check.csv")
    sl.to_csv("source_links.csv")


def clean_links():
    checklist = pd.read_csv("source_check.csv", index_col=0)
    links = pd.read_csv("source_links.csv", index_col=0)
    df = links[links.columns[2:]]

    for i in range(df.shape[0]):
        for column in df.columns:
            if checklist.iloc[i][column]:
                link = df.iloc[i][column]

                # Add https:// to links
                if re.search(r'^https:\/\/', link) is None:
                    link = 'https://' + link

                # Remove . at the end of links to avoid Bad Request error
                link = re.sub(r'(?<=\w)\.$', '', link)

                # Change http to https
                link = re.sub(r'^http:\/\/', 'https://', link)

                # Remove false positive matches (usually Facebook, Twitter, or Instagram links)
                if column == "Website":
                    if re.search(r'(https:\/\/www\.)?(facebook|twitter|instagram)\.com\/(\w|\w[-_/])+',
                                 link) is not None:
                        checklist.at[i, column] = False
                        links.at[i, column] = np.nan

                # Update link
                links.at[i, column] = link

    links.to_csv("source_links.csv")


if __name__ == '__main__':
    folder = input("Folder name: ")
    path = os.getcwd() + "/datasets/" + folder
    os.chdir(path)

    print("Reading source checklist...")
    sc = pd.read_csv("source_check.csv", index_col=0)

    print("Reading source links...")
    sl = pd.read_csv("source_links.csv", index_col=0)

    try:
        unchecked_exists = (True, pd.read_csv("unchecked.csv", index_col=0))
        print("Getting remaining queries...")
        os.remove("unchecked.csv")
    except FileNotFoundError:
        unchecked_exists = (False, np.nan)

    find_sources_via_google(sc, sl, unchecked_exists)
    clean_links()

    os.chdir("..")
    os.chdir("..")


