import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

def get_hls_file_path(movie_id, resolution, filename):
    return os.path.join(
        settings.MEDIA_ROOT, 'videos', 'processed',
        f'movie_{movie_id}', resolution, filename
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_index_m3u8(request, movie_id, resolution):
    file_path = get_hls_file_path(movie_id, resolution, 'index.mp3u8')
    if not os.path.exists(file_path):
        raise Http404("Playlist not found.")
    return FileResponse(open(file_path, 'rb'), content_type='application/vnd.apple.mpegurl')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_segment_ts(request, movie_id, resolution, segment):
    """Returns the binary MPEG transport stream (.ts) video segment."""
    file_path = get_hls_file_path(movie_id, resolution, segment)
    if not os.path.exists(file_path):
        raise Http404("Video segment not found.")
    return FileResponse(open(file_path, 'rb'), content_type='video/MP2T')