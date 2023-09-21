select v.id, v.etag, v.title, c.title, v.published_at, v.duration
from youtube_video as v
left join youtube_channel as c
    on v.channel_id = c.id
where c.title = 'Microsoft Power BI'