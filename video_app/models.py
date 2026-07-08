from django.db import models
from django.db import transaction

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


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            from .tasks import convert_video_to_hls
            transaction.on_commit(lambda: convert_video_to_hls.delay(self.id))
    def __str__(self):
        return self.title