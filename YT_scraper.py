# Google API Python Client by Google (n.d.)
# https://github.com/googleapis/google-api-python-client
# To install, run the following: pip install google-api-python-client
from googleapiclient.discovery import build

# Youtube Transcript API by Jonas Depoix (2018)
# https://github.com/jdepoix/youtube-transcript-api
# To install, run the following: pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi

# Put your personal API key here
apiKey = 'AIzaSyCIplXpNgYZ2IS44ZYyEi-hXRu1gzl9I58'

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

    for i in range(0, 1):
        video = searchResults[i]
        metadata = video.get("snippet")

        print("------------------------------------------------------------------------------")
        print("[" + str(i + 1) + "]")
        print("Video ID: " + video.get("id").get("videoId"))
        print("Title: " + str(metadata.get("title")))
        print("Channel: " + str(metadata.get("channelTitle") + " (" + metadata.get("channelId") + ")"))
        # print("Description: " + str(metadata.get("description")))

        request = youtube.videos().list(
            part=['snippet, statistics'],
            id=video.get("id").get("videoId"),
            maxResults=1
        )

        vid_specs = request.execute()
        print("----------------------------------------\n", vid_specs)
        '''
        Video Specifics Keys:
        dict_keys(['kind', 'etag', 'items', 'pageInfo'])
        '''

        # TODO: Display video date of publication
        print("Video Date of Publication: " + metadata.get("publishedAt")[:10])
        
        # TODO: Display Total Views, Likes, and Comments count of Video
        print("Video View Count: " + vid_specs.get("items")[0].get("statistics").get("viewCount"))
        print("Video Like Count:" + vid_specs.get("items")[0].get("statistics").get("likeCount"))
        print("Video Comment Count: " + vid_specs.get("items")[0].get("statistics").get("commentCount"))

        # TODO: Display video description as raw string
        print("------------------Start of Description------------------")
        print("Description:\n" + vid_specs.get("items")[0].get("snippet").get("description"))
        print("------------------End of Description------------------")

        '''
        try:
            print("Transcript: " + str(YouTubeTranscriptApi.get_transcript(video.get("id").get("videoId"))))
        except:
            print("Transcript unavailable")
        finally:
            print("")
        # '''

        #TODO get channel information
        request = youtube.channels().list(
            part=['snippet','statistics'],
            id= metadata.get("channelId"),
            maxResults=1
        )

        channel_specs =request.execute()

        # TODO: Display Subscriber count of channel
        print("Channel Subscriber count: " + channel_specs.get("items")[0].get("statistics").get("subscriberCount"))
        # TODO: Display total video uploaded of channel
        print("Channel Total video uploaded: " + channel_specs.get("items")[0].get("statistics").get("videoCount"))
        # TODO: Display published date of channel
        print("Channel Date of Publication: " + channel_specs.get("items")[0].get("snippet").get("publishedAt")[:10])

