# video_app/urls.py
from django.urls import path
from .views import stream_index_m3u8, stream_segment_ts

urlpatterns = [
    # Route for retrieving the master index playlist map
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', stream_index_m3u8, name='hls-index'),
    
    # Route for retrieving individual streaming .ts video chunks
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', stream_segment_ts, name='hls-segment'),
]