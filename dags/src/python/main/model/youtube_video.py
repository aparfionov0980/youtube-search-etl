import json

class YouTubeVideo:
    def __init__(self, id, etag, title, description, channelId, publishedAt, duration) -> None:
        self.id = id
        self.etag = etag
        self.title = title
        self.description = description
        self.channelId = channelId
        self.publishedAt = publishedAt
        self.duration = duration


    def __str__(self) -> str:
        return "YouTube(id = {id}, etag = {etag}, title = {title}, channelId = {channelId})"\
            .format(id = self.id, etag = self.etag, title = self.title, channelId = self.channelId)
    

    def toJSON(self) -> dict:
        return json.dumps(self, default = lambda o: o.__dict__, sort_keys = True, indent = 4)
    

    def toTuple(self) -> tuple:
        return (self.id, self.etag, self.title, self.channelId)


    def toTupleString(self) -> str:
        return (
            """('{id}', '{etag}', '{title}', '{description}',
              '{channelId}', '{publishedAt}', '{duration}')""".format(
                id = self.id,
                etag = self.etag,
                title = self.title,
                description = self.description,
                channelId = self.channelId,
                publishedAt = self.publishedAt,
                duration = self.duration
            )
        )

    @staticmethod
    def fromJSON(_string) -> object:
        YouTubeVideo_json = json.loads(_string)
        return YouTubeVideo(**YouTubeVideo_json)
    
