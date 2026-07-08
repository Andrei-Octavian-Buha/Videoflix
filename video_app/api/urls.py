# video_app/urls.py
from django.urls import path
from .views import stream_index_m3u8, stream_segment_ts, list_videos

urlpatterns = [
    path('video/', list_videos, name='video-list'),
    path('video/<int:video_id>/<str:resolution>/index.m3u8', stream_index_m3u8, name='hls-index'),
    path('video/<int:video_id>/<str:resolution>/<str:segment>', stream_segment_ts, name='hls-segment'),
]