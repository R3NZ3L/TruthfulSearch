import pandas as pd
import numpy as np
from math import sqrt
import os


def prepare_scores(output):
    if output == "vs":
        sb_df = pd.read_csv("source_backlinks.csv", index_col=0)
        sc_df = pd.read_csv("source_check.csv", index_col=0)

        comp_dict = {
            "channel_id": {}, "profiles": {}, "p_desc": {}, "external_sites": {}, "e_desc": {},
            "LinkedIn": {}, "li_desc": {}, "Wiki": {}, "wi_desc": {},
            "Website": {}, "we_desc": {},
            "Twitter": {}, "tw_desc": {},
            "Facebook": {}, "fb_desc": {},
            "Instagram": {}, "insta_desc": {}
        }

        for i in range(sc_df.shape[0]):
            comp_dict["channel_id"][i] = sc_df.iloc[i]["channel_id"]

            # // Sources //
            linkedIn = sc_df.iloc[i]["LinkedIn"]
            wiki = sc_df.iloc[i]["Wiki"]
            website = sc_df.iloc[i]["Website"]
            twitter = sc_df.iloc[i]["Twitter"]
            facebook = sc_df.iloc[i]["Facebook"]
            instagram = sc_df.iloc[i]["Instagram"]

            # Profiles
            if linkedIn and twitter and (facebook or instagram):
                comp_dict["profiles"][i] = 20 / 20
                comp_dict["p_desc"][i] = "Has existing LinkedIn, Twitter/X, AND Facebook OR Instagram profiles"
            elif (linkedIn or twitter) or (facebook and instagram):
                comp_dict["profiles"][i] = 15 / 20
                comp_dict["p_desc"][i] = "ONLY has existing Twitter/X AND Facebook OR Instagram profiles"
            elif (not linkedIn) and (not twitter) and (facebook or instagram):
                comp_dict["profiles"][i] = 5 / 20
                comp_dict["p_desc"][i] = "ONLY has existing Facebook OR Instagram profiles"
            elif (not linkedIn) and (not twitter) and not (facebook or instagram):
                comp_dict["profiles"][i] = 0 / 20
                comp_dict["p_desc"][i] = "Has no existing profiles"

            # External Sites
            if wiki and website:
                comp_dict["external_sites"][i] = 20 / 20
                comp_dict["e_desc"][i] = "Has existing official Wikipedia page AND website"
            elif website and not wiki:
                comp_dict["external_sites"][i] = 15 / 20
                comp_dict["e_desc"][i] = "Has existing official website BUT no Wikipedia page"
            elif not website and wiki:
                comp_dict["external_sites"][i] = 5 / 20
                comp_dict["e_desc"][i] = "Has existing official Wikipedia page BUT no website"
            elif not wiki and not website:
                comp_dict["external_sites"][i] = 0 / 20
                comp_dict["e_desc"][i] = "Has no existing external sites"

            # // Backlinks //
            sb_linkedIn = int(sb_df.iloc[i]["LinkedIn"])
            sb_wiki = int(sb_df.iloc[i]["Wiki"])
            sb_website = int(sb_df.iloc[i]["Website"])
            sb_twitter = int(sb_df.iloc[i]["Twitter"])
            sb_facebook = int(sb_df.iloc[i]["Facebook"])
            sb_instagram = int(sb_df.iloc[i]["Instagram"])

            # LinkedIn
            if sb_linkedIn >= 100:
                comp_dict["LinkedIn"][i] = 20 / 20
                comp_dict["li_desc"][i] = "Referenced by at least 100 webpages"
            elif 100 > sb_linkedIn >= 40:
                comp_dict["LinkedIn"][i] = 15 / 20
                comp_dict["li_desc"][i] = "Referenced by at least 40 but less than 100 webpages"
            elif 40 > sb_linkedIn >= 10:
                comp_dict["LinkedIn"][i] = 5 / 20
                comp_dict["li_desc"][i] = "Referenced by at least 10 but less than 40 webpages"
            elif sb_linkedIn < 10:
                comp_dict["LinkedIn"][i] = 0 / 20
                comp_dict["li_desc"][i] = "Referenced by less than 10 webpages"

            # Wiki
            if sb_wiki >= 100:
                comp_dict["Wiki"][i] = 20 / 20
                comp_dict["wi_desc"][i] = "Referenced by at least 100 webpages"
            elif 100 > sb_wiki >= 40:
                comp_dict["Wiki"][i] = 15 / 20
                comp_dict["wi_desc"][i] = "Referenced by at least 40 but less than 100 webpages"
            elif 40 > sb_wiki >= 10:
                comp_dict["Wiki"][i] = 5 / 20
                comp_dict["wi_desc"][i] = "Referenced by at least 10 but less than 40 webpages"
            elif sb_wiki < 10:
                comp_dict["Wiki"][i] = 0 / 20
                comp_dict["wi_desc"][i] = "Referenced by less than 10 webpages"
            
            # Website
            if sb_website >= 100:
                comp_dict["Website"][i] = 20 / 20
                comp_dict["we_desc"][i] = "Referenced by at least 100 webpages"
            elif 100 > sb_website >= 40:
                comp_dict["Website"][i] = 15 / 20
                comp_dict["we_desc"][i] = "Referenced by at least 40 but less than 100 webpages"
            elif 40 > sb_website >= 10:
                comp_dict["Website"][i] = 5 / 20
                comp_dict["we_desc"][i] = "Referenced by at least 10 but less than 40 webpages"
            elif sb_website < 10:
                comp_dict["Website"][i] = 0 / 20
                comp_dict["we_desc"][i] = "Referenced by less than 10 webpages"

            # Twitter
            if sb_twitter >= 100:
                comp_dict["Twitter"][i] = 20 / 20
                comp_dict["tw_desc"][i] = "Referenced by at least 100 webpages"
            elif 100 > sb_twitter >= 40:
                comp_dict["Twitter"][i] = 15 / 20
                comp_dict["tw_desc"][i] = "Referenced by at least 40 but less than 100 webpages"
            elif 40 > sb_twitter >= 10:
                comp_dict["Twitter"][i] = 5 / 20
                comp_dict["tw_desc"][i] = "Referenced by at least 10 but less than 40 webpages"
            elif sb_twitter < 10:
                comp_dict["Twitter"][i] = 0 / 20
                comp_dict["tw_desc"][i] = "Referenced by less than 10 webpages"

            # Facebook
            if sb_facebook >= 100:
                comp_dict["Facebook"][i] = 20 / 20
                comp_dict["fb_desc"][i] = "Referenced by at least 100 webpages"
            elif 100 > sb_facebook >= 40:
                comp_dict["Facebook"][i] = 15 / 20
                comp_dict["fb_desc"][i] = "Referenced by at least 40 but less than 100 webpages"
            elif 40 > sb_facebook >= 10:
                comp_dict["Facebook"][i] = 5 / 20
                comp_dict["fb_desc"][i] = "Referenced by at least 10 but less than 40 webpages"
            elif sb_facebook < 10:
                comp_dict["Facebook"][i] = 0 / 20
                comp_dict["fb_desc"][i] = "Referenced by less than 10 webpages"

            # Instagram
            if sb_instagram >= 100:
                comp_dict["Instagram"][i] = 20 / 20
                comp_dict["insta_desc"][i] = "Referenced by at least 100 webpages"
            elif 100 > sb_instagram >= 40:
                comp_dict["Instagram"][i] = 15 / 20
                comp_dict["insta_desc"][i] = "Referenced by at least 40 but less than 100 webpages"
            elif 40 > sb_instagram >= 10:
                comp_dict["Instagram"][i] = 5 / 20
                comp_dict["insta_desc"][i] = "Referenced by at least 10 but less than 40 webpages"
            elif sb_instagram < 10:
                comp_dict["Instagram"][i] = 0 / 20
                comp_dict["insta_desc"][i] = "Referenced by less than 10 webpages"


    elif output == "rank":
        videos = pd.read_csv("videos.csv", index_col=0)
        vs_df = pd.read_csv("verifiability_scores.csv", index_col=0)
        vb_df = pd.read_csv("video_backlinks.csv", index_col=0)
        ss_df = pd.read_csv("subjectivity_scores.csv", index_col=0)

        comp_dict = {
            "video_id": {}, "vs": {}, "backlinks": {},
            "subjectivity": {}
        }

        for i in range(videos.shape[0]):
            comp_dict["video_id"][i] = videos.iloc[i]["video_id"]

            comp_dict["vs"][i] = vs_df.loc[
                vs_df["channel_id"] == videos.iloc[i]["channel_id"]
            ]["vs"].iloc[0]

            backlinks = vb_df["backlinks"].iloc[i]

            if backlinks >= 100:
                comp_dict["backlinks"][i] = 20 / 20
            elif 100 > backlinks >= 50:
                comp_dict["backlinks"][i] = 15 / 20
            elif 50 > backlinks >= 25:
                comp_dict["backlinks"][i] = 5 / 20
            elif backlinks < 25:
                comp_dict["backlinks"][i] = 0 / 20

            sub_score = ss_df.iloc[i]["subjectivity"]

            if sub_score == -1.0 or sub_score >= 0.60:
                comp_dict["subjectivity"][i] = 0 / 20
            elif 0.60 > sub_score >= 0.50:
                comp_dict["subjectivity"][i] = 5 / 20
            elif 0.50 > sub_score >= 0.30:
                comp_dict["subjectivity"][i] = 15 / 20
            elif sub_score < 0.30:
                comp_dict["subjectivity"][i] = 20 / 20


    comp_df = pd.DataFrame.from_dict(comp_dict)

    if output == "vs":
        print("Saving raw scores as vs_raw_scores.csv...")
        comp_df.to_csv("vs_raw_scores.csv")

    return comp_df


def topsis(scores, output):
    if output == "vs":
        weights = {
            "profiles": 0.20,
            "external_sites": 0.30,
            "Wiki": 0.10,
            "Website": 0.15,
            "LinkedIn": 0.10,
            "Twitter": 0.05,
            "Facebook": 0.05,
            "Instagram": 0.05
        }

    elif output == "rank":
        weights = {
            "vs": 0.80,
            "backlinks": 0.10,
            "subjectivity": 0.10
        }

    wndm = {}

    for column in weights.keys():
        temp_list = []
        x = 0
        # print(column)
        for i in range(0, scores.shape[0]):
            num = scores.iloc[i][column] ** 2
            x += num
            # print(f"num: {num}, index: [{i}]")
        # print(f"x: {x}")
        denominator = sqrt(float(x))

        # Normalize scores
        for i in range(0, scores.shape[0]):
            if denominator == 0:
                norm_score = 0.0
            else:
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
        result = dist_from_worst[i] / (dist_from_best[i] + dist_from_worst[i])
        performance_ranks.append(result)

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
        rank_df = scores[["video_id", "rank"]].sort_values("rank", ascending=False).reset_index().drop("index", axis=1)
        print("Saving ranks as ranks.csv...")
        rank_df.to_csv("ranks.csv")
        print("Ranking complete.")


if __name__ == "__main__":
    folder = input("Folder name: ")
    path = os.getcwd() + "/datasets/" + folder
    os.chdir(path)

    topsis(prepare_scores(output="vs"), output="vs")
    topsis(prepare_scores(output="rank"), output="rank")

