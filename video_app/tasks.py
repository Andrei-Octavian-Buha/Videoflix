import os
import subprocess
from django.conf import settings
from django_rq import job
from .models import Video

@job('default')
def convert_video_to_hls(video_id):
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return f"Video {video_id} not found"
    
    raw_video_path = video.raw_video_file.path
    resolutions = {
        '480p': {'scale': '854:480', 'bitrate': '800k'},
        '720p': {'scale': '1280:720', 'bitrate': '1500k'},
        '1080p': {'scale': '1920:1080', 'bitrate': '3000k'}
    }
    for res_name, config in resolutions.items():
        processed_dir = os.path.join(settings.MEDIA_ROOT, 'videos',str(video.id), res_name)
        os.makedirs(processed_dir, exist_ok=True)

        output_playlist = os.path.join(processed_dir, 'index.m3u8')
        segment_pattern = os.path.join(processed_dir, '%03d.ts')
        
        cmd = [
            'ffmpeg', '-y',
            '-i', raw_video_path,
            '-vf', f"scale={config['scale']}",
            '-c:v', 'libx264',
            '-b:v', config['bitrate'],
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'hls',
            '-hls_time', '6',
            '-hls_playlist_type', 'event',
            '-hls_segment_filename', segment_pattern,
            output_playlist
        ]

        subprocess.run(cmd, check=True)

    return f"Finished converting video {video.title} to 720p HLS."