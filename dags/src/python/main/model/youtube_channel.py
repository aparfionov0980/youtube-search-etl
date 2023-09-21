import json


class YouTubeChannel:
    def __init__(self, id, etag, title, subscriberCount) -> None:
        self.id = id
        self.etag = etag
        self.title = title
        self.subscriberCount = subscriberCount


    def __str__(self) -> str:
        return "YouTube(id = {id}, etag = {etag}, title = {title}, subscriberCount = {subscriberCount})"\
            .format(id = self.id, etag = self.etag, title = self.title, 
                    subscriberCount = self.subscriberCount)
    

    def toJSON(self) -> dict:
        return json.dumps(self, default = lambda o: o.__dict__, sort_keys = True, indent = 4)
    

    def toTupleString(self) -> str:
        return (
            "('{id}','{etag}','{title}',{subscriberCount})".format(
                id = self.id,
                etag = self.etag,
                title = self.title,
                subscriberCount = self.subscriberCount
            )
        )
    

    @staticmethod
    def fromJSON(_string) -> object:
        YouTubeChannel_json = json.loads(_string)
        return YouTubeChannel(**YouTubeChannel_json)