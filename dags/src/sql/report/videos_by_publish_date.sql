select v.id, v.etag, v.title, v.channel_id, v.published_at, v.duration
from youtube_video as v
where v.published_at < timestamp '2023-01-01'