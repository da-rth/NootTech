from .utils import get_upload_key, get_file_path, get_thumb_path
from django.contrib.auth.models import AbstractUser
from easy_thumbnails.fields import ThumbnailerImageField
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    colour = models.CharField(max_length=7, default="#00CCCC")
    upload_key = models.CharField(max_length=26, default=get_upload_key())
    auto_delete_after = models.IntegerField(null=True)
    warnings = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class BannedUser(models.Model):

    class Meta:
        verbose_name_plural = 'Banned Users'

    banned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banned_user_set')
    banned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banned_by_set')
    date = models.DateTimeField(default=timezone.now)
    reason = models.TextField(blank=False)


class URL(models.Model):

    class Meta:
        verbose_name_plural = 'URLs'

    url = models.URLField()
    clicks = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    embed_supported = models.BooleanField(default=False)
    embed_type = models.CharField(max_length=32, blank=True)


class File(models.Model):

    class Meta:
        verbose_name_plural = 'All Files'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    ip = models.GenericIPAddressField()
    icon = models.CharField(default="fas fa-file", max_length=32)

    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_web_safe = models.BooleanField(default=False)

    generated_filename = models.CharField(max_length=16, blank=True, unique=True, null=True)
    original_filename = models.CharField(max_length=256)

    file_path = models.FileField(upload_to=get_file_path, null=True, blank=True, unique=True)
    file_ext = models.CharField(max_length=24, default=None)
    file_mime_type = models.CharField(max_length=64, default="text/plain")
    file_size_bytes = models.BigIntegerField(default=0)
    file_size_str = models.CharField(max_length=12, default="0 Bytes")
    file_type = models.CharField(max_length=6, default="Other")  # Image, Video, Audio, Text, Other

    def as_dict(self):
        return {
            "id": self.id,
            "uploader": str(self.user),
            "date": str(self.date).split('.')[0],
            "views": self.views,
            "name": {
                "original": self.original_filename,
                "generated": self.generated_filename
            },
            "file": {
                "file_path": str(self.file_path),
                "size": self.file_size_str,
                "size_bytes": self.file_size_bytes,
                "mime_type": self.file_mime_type,
                "extension": self.file_ext
            },
        }

    def __str__(self):
        orig = self.original_filename[:36]+"..." if len(str(self.original_filename)) > 36 else self.original_filename
        return f'{self.generated_filename} - {orig}'


class ReportedFile(models.Model):

    class Meta:
        verbose_name_plural = 'Reported Files'

    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user_set')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_by_set')
    reported_file = models.ForeignKey(File, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    reason_title = models.CharField(max_length=128)
    reason_body = models.TextField()


class Image(models.Model):

    class Meta:
        verbose_name_plural = 'Images'

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=64, null=True, blank=True)
    bit_colour = models.IntegerField(default=0)
    thumbnail = ThumbnailerImageField(
        upload_to=get_thumb_path,
        blank=True,
        null=True,
        resize_source=dict(size=(200, 113), sharpen=True, crop=True, quality=70)
    )


class Video(models.Model):

    class Meta:
        verbose_name_plural = 'Videos'

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=64, null=True, blank=True)
    duration = models.IntegerField(default=0)
    bit_rate = models.IntegerField(default=0)
    thumbnail = ThumbnailerImageField(
        upload_to=get_thumb_path,
        blank=True,
        null=True,
        resize_source=dict(size=(200, 113), sharpen=True, crop=True, quality=70)
    )


class Audio(models.Model):

    class Meta:
        verbose_name_plural = 'Audio'

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    sample_rate = models.IntegerField(default=0)


class Text(models.Model):

    class Meta:
        verbose_name_plural = 'Text'

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    characters = models.IntegerField(default=0)
    syntax_highlighting = models.IntegerField(blank=True)


class ErrorVideo(models.Model):

    class Meta:
        verbose_name_plural = 'Error Videos'

    url = models.URLField(unique=True, blank=True)
    name = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name

