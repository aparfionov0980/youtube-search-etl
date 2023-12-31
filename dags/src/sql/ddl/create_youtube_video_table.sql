CREATE TABLE IF NOT EXISTS YOUTUBE_VIDEO (
    ID VARCHAR(11) NOT NULL,
    ETAG VARCHAR(27),
    DESCRIPTION TEXT,
    TITLE TEXT,
    CHANNEL_ID VARCHAR(24),
    PUBLISHED_AT TIMESTAMP,
    DURATION VARCHAR(20),
    PRIMARY KEY ( ID )
);