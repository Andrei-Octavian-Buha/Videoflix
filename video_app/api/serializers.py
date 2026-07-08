from rest_framework import serializers
from video_app.models import Video

class VideoListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.ImageField(source='thumbnail',read_only=True)
    class Meta:
        model = Video
        fields = fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']