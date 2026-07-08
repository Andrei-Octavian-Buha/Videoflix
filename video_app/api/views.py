import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from video_app.models import Video
from .serializers import VideoListSerializer


def get_hls_file_path(video_id, resolution, filename):
    return os.path.join(
        settings.MEDIA_ROOT, 'videos', str(video_id), resolution, filename
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_videos(request):
    """Returns a list of all available videos sorted by newest first."""
    videos = Video.objects.all().order_by('-created_at')
    serializer = VideoListSerializer(videos, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_index_m3u8(request, video_id, resolution):
    file_path = get_hls_file_path(video_id, resolution, 'index.m3u8')
    if not os.path.exists(file_path):
        raise Http404("Playlist not found.")
    return FileResponse(open(file_path, 'rb'), content_type='application/vnd.apple.mpegurl')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_segment_ts(request, video_id, resolution, segment):
    """Returns the binary MPEG transport stream (.ts) video segment."""
    file_path = get_hls_file_path(video_id, resolution, segment)
    if not os.path.exists(file_path):
        raise Http404("Video segment not found.")
    return FileResponse(open(file_path, 'rb'), content_type='video/MP2T')