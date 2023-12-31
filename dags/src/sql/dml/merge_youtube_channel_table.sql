MERGE INTO YOUTUBE_CHANNEL AS T
USING (
    VALUES {{ ti.xcom_pull(task_ids="extract_channels_info_task") }}
) AS S(ID, ETAG, TITLE, SUBSCRIBER_COUNT)
ON T.ID = S.ID
WHEN MATCHED THEN
    UPDATE SET ETAG = S.ETAG, TITLE = S.TITLE, SUBSCRIBER_COUNT = S.SUBSCRIBER_COUNT
WHEN NOT MATCHED THEN
    INSERT (ID, ETAG, TITLE, SUBSCRIBER_COUNT) VALUES (S.ID, S.ETAG, S.TITLE, S.SUBSCRIBER_COUNT)