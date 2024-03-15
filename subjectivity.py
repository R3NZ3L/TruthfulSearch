import pandas as pd
import regex as re
from textblob import TextBlob
import os


def get_and_clean_transcripts(df):
    drop_indices = df[["video_id", "video_transcript"]].loc[df["video_transcript"] == 'nan'].index
    df.drop(drop_indices, inplace=True)

    # Regular Expressions
    patterns = []
    replacements = []

    # [0] Removing occurances of \xa0 and \n
    patterns.append('(\\xa0|\\n)')
    replacements.append(' ')

    # [1] Removing text enclosed in brackets
    patterns.append('\[(\w|\s)+\]')
    replacements.append('')

    # [2] Replacing stray '000's to 'thousand'
    patterns.append('(?<=\s)000(?=\s)')
    replacements.append('thousand')

    # [3, 4] Mistranscriptions of the word 'COVID'
    patterns.append('(?<=\s)(C|c)o(ve(r)?t|id)(?=\s)')
    patterns.append('(C|c)overed(?=\s(vacc|infe))')
    replacements.append('COVID')
    replacements.append('COVID')

    # [5] Mistranscriptions of the word 'COVID-19'
    patterns.append('(?<=\s)(C|c)(oveted|o9|o\s19)(?=\s)')
    replacements.append('COVID19')

    # [6] Replacing '%' with the word 'percent'
    patterns.append('(?<=\d)\%')
    replacements.append(' percent')

    # [7] Removing 'Speaker %d:' occurances
    patterns.append('Speaker\s\d\:')
    replacements.append('')

    # [8] Removing '[\xa0__\xa0]'
    patterns.append('\[\\xa0\_\_\\xa0\]')
    replacements.append('')

    # [9] Removing >> occurances
    patterns.append('\>\>(\>+)?')
    replacements.append('')

    # [10] Removing 'Reporter:' occurances
    patterns.append('Reporter\:')
    replacements.append('')

    # [11] Removing weird +@ occurances
    patterns.append('\+\@')
    replacements.append('')

    # [12] Removing stray - occurances
    patterns.append('(?<=\s)\-(\-+)?(?=\s)')
    replacements.append('')

    # [13] Removing text within parentheses
    patterns.append('\((\w|\s)+\)')
    replacements.append('')

    # [14] Combining stray instances of '19' with the word 'covid' if it exists next to it
    patterns.append('(covid|COVID)(\s|-)?19')
    replacements.append('COVID19')

    transcripts = df["video_transcript"].tolist()
    cleaned = []

    for transcript in transcripts:
        result = re.sub(patterns[0], replacements[0], str(transcript))

        for i in range(1, len(patterns)):
            result = re.sub(patterns[i], replacements[i], result)

        cleaned.append(result)

    transcripts_df = pd.DataFrame(
        {
            'video_id': df["video_id"].tolist(),
            'video_title': df["video_title"].tolist(),
            'video_transcript': cleaned
        }
    )

    return transcripts_df


def get_subjectivity(df):
    ss = []
    for entry in df["video_transcript"]:
        testimonial = TextBlob(entry)
        score = testimonial.sentiment.subjectivity
        if score == 0.0:
            ss.append(-1)
        elif score > 0:
            ss.append(testimonial.sentiment.subjectivity)

    ss = pd.Series(ss, name="subjectivity")
    df = pd.concat([df, ss], axis=1)

    return df


def subjectivity(videos):
    print("Computing for video transcript subjectivity...")
    df = get_subjectivity(get_and_clean_transcripts(videos))
    print("Saving subjectivity scores in subjectivity_scores.csv")
    df.to_csv("subjectivity_scores.csv")


if __name__ == "__main__":
    filename = input("Filename (w/o .csv): ")
    path = os.getcwd() + "/datasets/" + filename
    os.chdir(path)

    video_df = pd.read_csv("videos.csv", index_col=0)

    subjectivity(video_df)

    os.chdir("..")
    os.chdir("..")
    print("Back @ " + os.getcwd())

