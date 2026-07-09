from rest_framework import serializers
from video_app.models import Video

class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model, designed to provide a lightweight summary 
    of video information, including the thumbnail image URL for client-side display.
    """
    thumbnail_url = serializers.ImageField(source='thumbnail',read_only=True)
    class Meta:
        model = Video
        fields = fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']