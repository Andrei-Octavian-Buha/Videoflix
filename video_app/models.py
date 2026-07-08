from django.db import models

# Create your models here.
class Video(models.Model):
    CHATEGORY_COICES = [
        ('General','General'),
        ('Drama','Drama'),
        ('Romance', 'Romance'),
        ('Action', 'Action'),
        ('Comedy','Comedy'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CHATEGORY_COICES, default='General')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    raw_video_file = models.FileField(upload_to='videos/raw/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title