
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example DAG demonstrating the usage of the TaskFlow API to execute Python functions natively and within a
virtual environment.
"""
from __future__ import annotations

import logging
import sys
import tempfile
import time
from pprint import pprint

import googleapiclient.discovery
import googleapiclient.errors

import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.operators.postgres import PostgresOperator 

from src.python.main.model.youtube_video import YouTubeVideo
from src.python.main.model.youtube_channel import YouTubeChannel
from src.python.main.model.video_search_query import VideoSearchQuery
from src.python.main.youtube_parser import parse_youtube_search_result
from src.python.main.youtube_parser import parse_youtube_channel_info
from src.python.main.youtube_parser import parse_youtube_video_info


log = logging.getLogger(__name__)


YOUTUBE_API_KEY_SECRET = 
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


YOUTUBE_SEARCH_QUERY = "power query"
YOUTUBE_VIDEOS_MAX_RESULTS = 1000


with DAG(
    dag_id = "power_query_youtube_search",
    schedule = None,
    start_date = pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup = False,
    tags = ["power_query"],
) as dag:
    @task(task_id="extract_videos_by_query_task")
    def extract_videos_by_query():
        # Call Youtube API for Video by Query
        youtube = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, developerKey=YOUTUBE_API_KEY_SECRET
        )

        request = youtube.search().list(
            part="snippet",
            maxResults = YOUTUBE_VIDEOS_MAX_RESULTS,
            type = "video",
            q = YOUTUBE_SEARCH_QUERY
        )

        response = request.execute()

        # Parse Results
        videos: list[YouTubeVideo] = parse_youtube_search_result(response)

        #Serialize and return videos
        videos = list(
            map(lambda v: v.toJSON(), videos)
        )

        return videos


    @task(task_id = "prepare_video_query_data_task")
    def prepare_video_query_data(videos: dict):
        videoSearchQueries: list[VideoSearchQuery] = list(
            map(lambda v: VideoSearchQuery(YouTubeVideo.fromJSON(v).id, YOUTUBE_SEARCH_QUERY), videos)
        )

        videoSearchQueries_str = str()
        for vsq in videoSearchQueries[:-1]:
            videoSearchQueries_str += (vsq.toTupleString() + ",")

        videoSearchQueries_str += videoSearchQueries[-1].toTupleString()
        return videoSearchQueries_str


    @task(task_id="extract_videos_full_info_task")
    def extract_videos_full_info(videos: dict):
        # Call Youtube API for Video Info
        videos: list[YouTubeVideo] = list(
            map(lambda v: YouTubeVideo.fromJSON(v), videos)
        )

        videos_ids = str()
        for v in videos:
            videos_ids += "{},".format(v.id)

        youtube = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, developerKey=YOUTUBE_API_KEY_SECRET
        )

        request = youtube.videos().list(
            part="snippet,contentDetails",
            id=videos_ids
        )

        response = request.execute()

        # Parse Results
        videos: list[YouTubeVideo] = parse_youtube_video_info(response)

        # Parse Results
        videos_str = str("")
        for v in videos[:-1]:
            videos_str += (v.toTupleString() + ",")
        videos_str += videos[-1].toTupleString()

        # Return Videos
        return videos_str

    
    @task(task_id="get_distinct_channels")
    def get_distinct_channels(videos: dict):
        # Extract distinct channels
        videos: list[YouTubeVideo] = list(
            map(lambda v: YouTubeVideo.fromJSON(v), videos)
        )

        channels_set = set()
        for v in videos:
            channels_set.add(v.channelId)

        # Return channels
        return channels_set


    @task(task_id="extract_channels_info_task")
    def extract_channels_info(channels: list):
        # Call Youtube API for Channel Info
        channel_ids = str()
        for c in channels:
            channel_ids += "{},".format(c)

        youtube = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, developerKey=YOUTUBE_API_KEY_SECRET
        )

        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_ids
        )

        response = request.execute()

        # Parse Results
        channels: list[YouTubeChannel] = parse_youtube_channel_info(response)

        # Return Videos
        channels_str = str("")
        for v in channels[:-1]:
            channels_str += (v.toTupleString() + ",")
        channels_str += channels[-1].toTupleString()

        return channels_str


    load_query_video_in_storage_task = PostgresOperator(
        task_id = "load_query_video_in_storage_task",
        postgres_conn_id = "storage",
        sql = "src/sql/dml/merge_query_video_table.sql"
    )


    load_videos_in_storage_task = PostgresOperator(
        task_id = "load_videos_in_storage_task",
        postgres_conn_id = "storage",
        sql = "src/sql/dml/merge_youtube_video_table.sql"
    )


    load_channels_in_storage_task = PostgresOperator(
        task_id = "load_channels_in_storage_task",
        postgres_conn_id = "storage",
        sql = "src/sql/dml/merge_youtube_channel_table.sql"
    )


    extracted_videos = extract_videos_by_query()

    prepare_video_query_data_task = prepare_video_query_data(extracted_videos)
    prepare_video_query_data_task >> load_query_video_in_storage_task

    extract_videos_full_info_task = extract_videos_full_info(extracted_videos)
    extract_videos_full_info_task >> load_videos_in_storage_task

    distinct_channels = get_distinct_channels(extracted_videos)
    extract_channels_info_task = extract_channels_info(distinct_channels)
    extract_channels_info_task >> load_channels_in_storage_task



# TEST
if __name__ == "__main__":
    dag.test()