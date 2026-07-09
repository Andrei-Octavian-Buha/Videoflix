import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from video_app.models import Video
from .serializers import VideoListSerializer


def get_hls_file_path(video_id, resolution, filename):
    """
    Constructs the absolute file system path for a specific HLS asset 
    (playlist or segment) based on the video ID, resolution, and filename.

    Args:
        video_id (int): The ID of the video record.
        resolution (str): The video quality folder (e.g., '480p').
        filename (str): The specific file to retrieve (e.g., 'index.m3u8' or '001.ts').

    Returns:
        str: The full path on the local file system.
    """
    return os.path.join(
        settings.MEDIA_ROOT, 'videos', str(video_id), resolution, filename
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_videos(request):
    """
    Retrieves and serializes a list of all available video objects, 
    ordered by creation date in descending order.

    Args:
        request: The incoming GET request object.

    Returns:
        Response: A DRF Response containing the serialized video list.
    """
    videos = Video.objects.all().order_by('-created_at')
    serializer = VideoListSerializer(videos, many=True, context={'request': request})
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_index_m3u8(request, video_id, resolution):
    """
    Serves the HLS master/variant playlist (.m3u8) file for a given 
    video and resolution.

    Args:
        request: The incoming GET request.
        video_id (int): ID of the video.
        resolution (str): Quality level (e.g., '720p').

    Returns:
        FileResponse: The .m3u8 file with correct MIME type.

    Raises:
        Http404: If the playlist file does not exist on disk.
    """
    file_path = get_hls_file_path(video_id, resolution, 'index.m3u8')
    if not os.path.exists(file_path):
        raise Http404("Playlist not found.")
    return FileResponse(open(file_path, 'rb'), content_type='application/vnd.apple.mpegurl')




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_segment_ts(request, video_id, resolution, segment):
    """
    Serves an individual binary MPEG transport stream (.ts) video segment.

    Args:
        request: The incoming GET request.
        video_id (int): ID of the video.
        resolution (str): Quality level (e.g., '720p').
        segment (str): Filename of the .ts segment.

    Returns:
        FileResponse: The binary video segment with correct MIME type.

    Raises:
        Http404: If the segment file does not exist on disk.
    """
    file_path = get_hls_file_path(video_id, resolution, segment)
    if not os.path.exists(file_path):
        raise Http404("Video segment not found.")
    return FileResponse(open(file_path, 'rb'), content_type='video/MP2T')