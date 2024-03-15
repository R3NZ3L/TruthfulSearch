import pandas as pd
import numpy as np
from math import sqrt
import os


def prepare_scores(output):
    if output == "vs":
        sb_df = pd.read_csv("source_backlinks.csv", index_col=0)
        sc_df = pd.read_csv("source_check.csv", index_col=0)

        comp_dict = {
            "channel_id": {}, "profiles": {}, "external_sites": {},
            "LinkedIn": {}, "Wiki": {}, "Website": {}, "Twitter": {}, "Facebook": {}
        }

        for i in range(sc_df.shape[0]):
            comp_dict["channel_id"][i] = sc_df.iloc[i]["channel_id"]

            # // Sources //
            linkedIn = sc_df.iloc[i]["LinkedIn"]
            wiki = sc_df.iloc[i]["Wiki"]
            website = sc_df.iloc[i]["Website"]
            twitter = sc_df.iloc[i]["Twitter"]
            facebook = sc_df.iloc[i]["Facebook"]

            # Profiles
            if linkedIn and (facebook or twitter):
                comp_dict["profiles"][i] = 20 / 20
            elif linkedIn or (facebook and twitter):
                comp_dict["profiles"][i] = 10 / 20
            elif (not linkedIn) and (facebook or twitter):
                comp_dict["profiles"][i] = 5 / 20
            elif (not linkedIn) and (not facebook) and (not twitter):
                comp_dict["profiles"][i] = 0 / 20

            # External Sites
            if wiki and website:
                comp_dict["external_sites"][i] = 20 / 20
            elif wiki and not website:
                comp_dict["external_sites"][i] = 10 / 20
            elif not wiki and website:
                comp_dict["external_sites"][i] = 5 / 20
            elif not wiki and not website:
                comp_dict["external_sites"][i] = 0 / 20

            # // Backlinks //
            sb_linkedIn = int(sb_df.iloc[i]["LinkedIn"])
            sb_wiki = int(sb_df.iloc[i]["Wiki"])
            sb_website = int(sb_df.iloc[i]["Website"])
            sb_twitter = int(sb_df.iloc[i]["Twitter"])
            sb_facebook = int(sb_df.iloc[i]["Facebook"])

            # LinkedIn
            if sb_linkedIn >= 100:
                comp_dict["LinkedIn"][i] = 20 / 20
            elif 100 > sb_linkedIn >= 50:
                comp_dict["LinkedIn"][i] = 10 / 20
            elif 50 > sb_linkedIn >= 25:
                comp_dict["LinkedIn"][i] = 5 / 20
            elif sb_linkedIn < 25:
                comp_dict["LinkedIn"][i] = 0 / 20

            # Wiki
            if sb_wiki >= 3000:
                comp_dict["Wiki"][i] = 20 / 20
            elif 3000 > sb_wiki >= 1500:
                comp_dict["Wiki"][i] = 10 / 20
            elif 1500 > sb_wiki >= 500:
                comp_dict["Wiki"][i] = 5 / 20
            elif sb_wiki < 500:
                comp_dict["Wiki"][i] = 0 / 20

            # Website
            if sb_website >= 3000:
                comp_dict["Website"][i] = 20 / 20
            elif 3000 > sb_website >= 1500:
                comp_dict["Website"][i] = 10 / 20
            elif 1500 > sb_website >= 500:
                comp_dict["Website"][i] = 5 / 20
            elif sb_website < 500:
                comp_dict["Website"][i] = 0 / 20

            # Twitter
            if sb_twitter >= 100:
                comp_dict["Twitter"][i] = 20 / 20
            elif 100 > sb_twitter >= 50:
                comp_dict["Twitter"][i] = 10 / 20
            elif 50 > sb_twitter >= 25:
                comp_dict["Twitter"][i] = 5 / 20
            elif sb_twitter < 25:
                comp_dict["Twitter"][i] = 0 / 20

            # Facebook
            if sb_facebook >= 100:
                comp_dict["Facebook"][i] = 20 / 20
            elif 100 > sb_facebook >= 50:
                comp_dict["Facebook"][i] = 10 / 20
            elif 50 > sb_facebook >= 25:
                comp_dict["Facebook"][i] = 5 / 20
            elif sb_facebook < 25:
                comp_dict["Facebook"][i] = 0 / 20
    elif output == "rank":
        comp_dict = {
            "video_id": {}, "vs": {}, "backlinks": {},
            "subjectivity": {}
        }

        

    comp_df = pd.DataFrame.from_dict(comp_dict)

    return comp_df


def topsis(scores, output):
    if output == "vs":
        weights = {
            "profiles": 0.15,
            "external_sites": 0.15,
            "LinkedIn": 0.25,
            "Wiki": 0.25,
            "Website": 0.10,
            "Twitter": 0.05,
            "Facebook": 0.05
        }

    elif output == "rank":
        weights = {
            "vs": 0.70,
            "backlinks": 0.25,
            "subjectivity": 0.05
        }

    wndm = {}

    for column in weights.keys():
        temp_list = []
        x = 0
        for i in range(0, scores.shape[0]):
            num = scores.iloc[i][column] ** 2
            x += num
        denominator = sqrt(x)

        if denominator == 0:
            continue

        # Normalize scores
        for i in range(0, scores.shape[0]):
            norm_score = scores.iloc[i][column] / denominator
            temp_list.append(norm_score)

        # Apply weight
        for i in range(0, len(temp_list)):
            temp_list[i] *= weights.get(column)

        wndm.update({column: temp_list})

    wndm_df = pd.DataFrame.from_dict(wndm)
    ideal_best = wndm_df.max()
    ideal_worst = wndm_df.min()

    dist_from_best = []
    dist_from_worst = []

    # Euclidean distance from ideal best
    for i in range(0, wndm_df.shape[0]):
        temp_num = 0
        for column in wndm_df.columns:
            temp_num += (wndm_df.iloc[i][column] - ideal_best[column]) ** 2
        dist_from_best.append(sqrt(temp_num))

    # Euclidean distance from ideal worst
    for i in range(0, wndm_df.shape[0]):
        temp_num = 0
        for column in wndm_df.columns:
            temp_num += (wndm_df.iloc[i][column] - ideal_worst[column]) ** 2
        dist_from_worst.append(sqrt(temp_num))

    performance_ranks = []
    for i in range(0, wndm_df.shape[0]):
        performance_ranks.append(dist_from_worst[i] / (dist_from_best[i] + dist_from_worst[i]))

    performance_ranks = pd.Series(np.array(performance_ranks))

    if output == "vs":
        scores["vs"] = performance_ranks
        vs_df = scores[["channel_id", "vs"]].sort_values("vs", ascending=False).reset_index().drop("index", axis=1)

        category = []

        for i in range(vs_df.shape[0]):
            score = vs_df.iloc[i]["vs"]

            if score >= 0.70:
                category.append("Very Verifiable")
            elif 0.70 > score >= 0.50:
                category.append("Verifiable")
            elif 0.50 > score >= 0.25:
                category.append("Somewhat Verifiable")
            elif 0.25 > score > 0.0:
                category.append("Not so Verifiable")
            elif score == 0.0:
                category.append("Cannot be verified")

        category = pd.Series(category, name="category")
        categorized_df = pd.concat([vs_df, category], axis=1)

        print("Saving scores as verifiability_scores.csv...")
        categorized_df.to_csv("verifiability_scores.csv")
        print("Scoring complete.")

    elif output == "rank":
        scores["rank"] = performance_ranks
        rank_df = scores[["channel_id", "rank"]].sort_values("rank", ascending=False).reset_index().drop("index", axis=1)
        print("Saving ranks as ranks.csv...")
        rank_df.to_csv("ranks.csv")
        print("Ranking complete.")


if __name__ == "__main__":
    filename = input("Filename (w/o .csv): ")
    path = os.getcwd() + "/datasets/" + filename
    os.chdir(path)

    # topsis(prepare_scores(output="vs"), output="vs")
    topsis(prepare_scores(output="rank"), output="rank")

