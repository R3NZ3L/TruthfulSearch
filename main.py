# Google API Python Client by Google (n.d.)
# https://github.com/googleapis/google-api-python-client
# To install, run the following: pip install google-api-python-client
from googleapiclient.discovery import build

# Youtube Transcript API by Jonas Depoix (2018)
# https://github.com/jdepoix/youtube-transcript-api
# To install, run the following: pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi

# Put your personal API key here
apiKey = '#####'

# Youtube API object
youtube = build('youtube', 'v3', developerKey=apiKey)

if __name__ == '__main__':
    searchQuery = input("Search query: ")

    request = youtube.search().list(
        part="snippet",
        q=searchQuery,
        type="video",
        maxResults=50,
        order="relevance"
    )

    response = request.execute()

    '''
    Response Keys: 
    dict_keys(['kind', 'etag', 'nextPageToken', 'regionCode', 'pageInfo', 'items'])
    
    Search Results (items) Keys: 
    dict_keys(['kind', 'etag', 'id', 'snippet'])
    
    Metadata (snippet) Keys: 
    dict_keys(['publishedAt', 'channelId', 'title', 'description', 'thumbnails', 'channelTitle', 'liveBroadcastContent', 'publishTime']) 
    '''

    searchResults = response.get("items")

    print("--------------")
    print("")

    for i in range(0, 3):
        video = searchResults[i]
        metadata = video.get("snippet")

        print("[" + str(i + 1) + "]")
        print("Video ID: " + str(video.get("id").get("videoId")))
        print("Title: " + str(metadata.get("title")))
        print("Channel: " + str(metadata.get("channelTitle")))
        print("Transcript: " + str(YouTubeTranscriptApi.get_transcript(video.get("id").get("videoId"))))
        print("")


