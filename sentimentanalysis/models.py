from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import regex as re
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import stanza
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

"""
# get comments from a specific video using Youtube API
apiKey = 'AIzaSyCIplXpNgYZ2IS44ZYyEi-hXRu1gzl9I58'
youtube = build('youtube', 'v3', developerKey=apiKey)
videoId="4qnwdTr7LM0"

comment_request = youtube.commentThreads().list(
                part=['snippet'],
                videoId=videoId,
                maxResults=20,
                order='relevance',
                textFormat="plainText"
            )
"""

list_of_comments = ['Prayers for the world', 'What Should Israel Do Next in Light of Their Declaration of War?\n\nFirst, we should reflect deeply upon the painful divide that has festered among us, causing the devastating toll of hundreds of lives lost and thousands wounded. We need to yearn for a major change and wholeheartedly unite as one. Only the bonds of unity can shield us from future tragedy and elevate our nation from the abyss of despair.\n\nWe cannot afford to nurse bitterness or delay action, waiting for the war\'s end to ponder our fractured state. Now is the time for introspection. We need to pinpoint the reasons behind our present circumstances and act accordingly.\n\nOur quest for understanding needs to extend to our lives’ very source: the upper force of love, bestowal and connection that acts on us beyond our current level of awareness, which perceives through an egoistic and divisive lens. It is no matter of religion, but a realization that reality’s governing force is singular, and we accordingly need to stand united before it as one.\n\nPrecisely in our trying times, we are in need for an expansion of consciousness to let the upper force of love and bestowal into our lives. We need to raise the pain and anguish that erupts in so many people in such times to the upper force, and wish for it to mend our torn relations, and draw us closer together. We must seek to hold each other close to our hearts, not solely in times of war, but as an enduring duty.\n\nWe are a nation established not on a biological foundation, but on a spiritual-ideological one: "Love your neighbor as yourself." That is, we were people from all around ancient Babylon who felt a problem with living our lives solely according to competitive-materialistic ideals and sought for a higher truth to our existence, which we revealed as a higher force of love, bestowal and connection that united us above our divisive drives. That is why we cannot remain divided without suffering from our separation.\n\nOur mission to unite above our divisions is constant, because divisive egoistic desires constantly surface within us, driving us apart. Therefore, much like a diligent student who finds new homework awaiting them each day, we should not accumulate any more overdue assignments that end up exploding in our faces, pressuring us into critical situations such as the one we now find before us. Instead, we should hurry up and correct our hearts to favor unity “as one man with one heart” above our divisions.', 'They are still getting what they want by not letting them back home', 'I don’t believe in war, but I do believe in giving people what they ask for', 'I Wouldnt Expect Any Cease Fire', '1048 will be the generation that won’t pass away until it sees the coming of the Son of Man', 'Praise the lord dont let the devil try and take yall stay safe guys🙏', 'This war just got bigger.', 'I thought the captain was supposed to stay with the sinking ship?  Look at the coward run. Should not have had a family', 'Imagine if every single death in gaza got this much attention', 'Zechariah 11: 1 Open your doors, Lebanon, and fire will consume your cedars. 2 Wail, cypress tree, for the cedar has fallen while the stately trees are destroyed. Wail, oak trees of Bashan, for the old growth forest has been cut down. 3 Hear the wailing of the shepherds, for the magnificence of the forest[c] is ruined! Hear the roar of the lions, for the Jordan’s arrogance is ruined!', 'If they sew the wind they will reap the whirlwind.', 'Lebanon has the right to defend itself! Palestinians do too!', 'Sad', 'Prayers for Israel , America and Ukrainians.   Thank you God Almighty. Possessor of heaven and earth. The just God.  The righteous and loving God', 'Praise Jesus christ and he will show what he can do he will bring his land back', 'Restraint the International organizations say, and yet Israel has restrained and continues to restrain itself ever since Hamas started this war.', "Israel has a right to defend it's children.", 'Lebanon government will also face the consequences for granting Hezbollah space to strike Israel from Lebanon']

"""
# Vader 
def sentiment_scores(sentence):

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
     
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
 
    print("Sentence Overall Rated As", end = " ")
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        print("Positive")
 
    elif sentiment_dict['compound'] <= - 0.05 :
        print("Negative")
 
    else :
        print("Neutral")

"""

"""
# Roberta Transformer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
labels = ['Negative', 'Neutral', 'Positive']

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

for comments in dasdasd:
    comment_words = []
    comments = comments.replace("\n", " ")
    comments = comments.replace("\xa0", " ")
    comments = comments.replace("?", " ")
    comments = comments.replace(":", " ")
    comments = comments.replace(";", " ")
    comments = comments.replace(";", " ")
    comments = re.sub(r"\s+", ' ', comments) 
    print(comments)
    for word in comments.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        
        elif word.startswith('http'):
            word = "http"
        comment_words.append(word)

    comment_procs = " ".join(comment_words)

    encoded = tokenizer(comment_procs, return_tensors='pt', max_length=512, truncation=True, padding=True)
    print(encoded)
    output = model(**encoded)

    scores = output[0][0].detach().numpy()

    scores = softmax(scores)

    for i in range(len(scores)):

        l = labels[i]
        s = scores[i]
        print(l, s)
"""

"""
# TextBlob
for comment in list_of_comments:
    testimonial = TextBlob(comment)
    print(comment)
    if (testimonial.sentiment.polarity > 0):
        print("positive", testimonial.sentiment.subjectivity)
    elif (testimonial.sentiment.polarity < 0):
        print("negative", testimonial.sentiment.subjectivity)
    else:
        print("neutral", testimonial.sentiment.subjectivity)
"""

"""
# Stanza
# stanza.download('en')       # This downloads the English models for the neural pipeline
nlp = stanza.Pipeline('en', processors='tokenize,sentiment', tokenize_no_ssplit=True)

for comment in list_of_comments:
    doc = nlp(comment.replace("\n", " "))
    print(comment)
    #doc.sentences[0].print_dependencies()
    for i, sentence in enumerate(doc.sentences):
        print("%d -> %d" % (i, sentence.sentiment))


list_of_comments = []
try:
    video_comments = comment_request.execute()
except:
    print("No comment for this video")
else:   
    for comment in video_comments.get("items"): 
        current_comment = comment.get("snippet").get("topLevelComment").get("snippet").get("textDisplay")
        #print(current_comment)

        #print(current_comment + "\ntesting vader sentiment analysis scores:")
        #print(sentiment_scores(current_comment))
        list_of_comments.append(current_comment)

print(list_of_comments)

"""


