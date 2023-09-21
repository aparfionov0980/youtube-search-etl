select v.id, v.etag, v.title, v.channel_id, v.published_at, v.duration, c.subscriber_count
from youtube_video as v
left join youtube_channel as c
on v.channel_id = c.id
where c.subscriber_count > 1000