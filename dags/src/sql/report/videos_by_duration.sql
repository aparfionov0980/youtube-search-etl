select id, etag, title, channel_id, published_at, duration
from youtube_video
where duration::interval < 'PT30M'::interval and duration::interval > 'PT10M'::interval