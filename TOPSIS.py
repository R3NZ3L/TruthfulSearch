import pandas as pd
import numpy as np
from math import sqrt


def prepare_scores(sc_df, sb_df):
    comp_dict = {"channel_id": {}, "profiles": {}, "external_sites": {}}

    for i in range(sc_df.shape[0]):
        comp_dict["channel_id"][i] = sc_df.iloc[i]["channel_id"]

        linkedIn = sc_df.iloc[i]["LinkedIn"]
        wiki = sc_df.iloc[i]["Wiki"]
        website = sc_df.iloc[i]["Website"]
        twitter = sc_df.iloc[i]["Twitter"]
        facebook = sc_df.iloc[i]["Facebook"]

        # Profiles
        if linkedIn and (facebook or twitter):
            comp_dict["profiles"][i] = 20
        elif (not linkedIn) and facebook and twitter:
            comp_dict["profiles"][i] = 10
        elif (not linkedIn) and (facebook or twitter):
            comp_dict["profiles"][i] = 5
        elif (not linkedIn) and (not facebook) and (not twitter):
            comp_dict["profiles"][i] = 0

        # External Sites
        if wiki and website:
            comp_dict["external_sites"][i] = 20
        elif wiki and not website:
            comp_dict["external_sites"][i] = 10
        elif not wiki and website:
            comp_dict["external_sites"][i] = 5
        elif not wiki and not website:
            comp_dict["external_sites"][i] = 0


    comp_df = pd.DataFrame.from_dict(comp_dict)
    comp_df = pd.concat([comp_df, sb_df[["LinkedIn", "Wiki", "Website", "Twitter", "Facebook"]]], axis=1)

    return comp_df


def topsis(scores):
    weights = {
        "profiles": 0.10,
        "external_sites": 0.10,
        "LinkedIn": 0.25,
        "Wiki": 0.25,
        "Website": 0.10,
        "Twitter": 0.10,
        "Facebook": 0.10
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

    performance_rank = []
    for i in range(0, wndm_df.shape[0]):
        performance_rank.append(dist_from_worst[i] / (dist_from_best[i] + dist_from_worst[i]))

    performance_rank = pd.Series(np.array(performance_rank))

    scores["vs"] = performance_rank

    vs_df = scores[["channel_id", "vs"]].sort_values("vs", ascending=False).reset_index().drop("index", axis=1)
    print("Saving as scores as verifiability_scores.csv...")
    vs_df.to_csv("verifiability_scores.csv")

    print("Channel verifiability scored.")
