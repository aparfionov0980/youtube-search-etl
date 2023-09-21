class VideoSearchQuery:
    def __init__(self, videoId, query) -> None:
        self.videoId = videoId
        self.query = query


    def toTupleString(self) -> str:
        return(
            """('{videoId}','{query}')""".format(
                videoId = self.videoId,
                query = self.query                
            )
        )