select v.id, v.etag, vsq.query, v.title, v.channel_id, v.published_at, v.duration
from video_search_query as vsq
left join youtube_video as v
    on v.id = vsq.youtube_video_id
where vsq.query = 'power bi'