from src.python.main.model.youtube_video import YouTubeVideo
from src.python.main.model.youtube_channel import YouTubeChannel

def parse_youtube_search_result(response):
    videos: list[YouTubeVideo] = []
    
    items = response["items"]
    for i in items:
        videos.append(
            YouTubeVideo(
                id = i["id"]["videoId"], etag = i["etag"], title=i["snippet"]["title"],
                description=None,  
                channelId = i["snippet"]["channelId"],
                publishedAt=None,
                duration=None
            )
        )

    return videos


def parse_youtube_video_info(response):
    videos: list[YouTubeVideo] = []
    
    items = response["items"]
    for i in items:
        description = str(i["snippet"]["description"])\
            .replace('\n', "\\n")\
            .replace("\n\r", "\\n\\r")\
            .replace('\t', "\\t")\
            .replace("'", "''")\
        
        title = str(i["snippet"]["title"])\
            .replace("'", "''")

        videos.append(
            YouTubeVideo(
                id = i["id"], etag = i["etag"], 
                title=title,
                description=description,
                channelId=i["snippet"]["channelId"],
                publishedAt=i["snippet"]["publishedAt"],
                duration=i["contentDetails"]["duration"]
            )
        )

    return videos


def parse_youtube_channel_info(response):
    channels: list[YouTubeChannel] = []
    
    items = response["items"]
    for i in items:
        channels.append(
            YouTubeChannel(
                id = i["id"], etag = i["etag"], title=i["snippet"]["title"],
                  subscriberCount = i["statistics"]["subscriberCount"]
            )
        )

    return channels
