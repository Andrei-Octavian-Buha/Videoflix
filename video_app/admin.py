from django.contrib import admin
from .models import Video
# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Configures the administrative interface for the Video model, 
    providing list views, filtering, and search capabilities for 
    efficient video management.
    """
    list_display = ('id', 'title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')