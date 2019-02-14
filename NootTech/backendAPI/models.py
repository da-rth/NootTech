from .utils import get_upload_key, get_id_gen, get_ext, get_filesize_str, get_fontawesome, get_syntax_highlighting, get_chars_lines, is_websafe
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField
from django.db import models
from django.utils import timezone
from mimetypes import MimeTypes
from moviepy.editor import VideoFileClip, AudioFileClip
import PIL.Image
mime = MimeTypes()

"""
File:   models.py
Date:   13/02/2019
Author: 2086380A
"""


def thumb_path(instance, filename):
    return 'Thumbnails/{0}/{1}__{2}'.format(instance.user.id, instance.generated_filename, instance.original_filename)


def file_path(instance, filename):
    return 'Uploads/{0}/{1}__{2}'.format(instance.user.id, instance.generated_filename, instance.original_filename)


class User(AbstractUser):

    colour = models.CharField(max_length=7, default="#00CCCC")
    upload_key = models.CharField(max_length=26, default=get_upload_key())
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


class File(models.Model):

    class Meta:
        verbose_name_plural = 'All Files'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    icon = models.CharField(blank=True, max_length=32)

    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    generated_filename = models.CharField(max_length=16, default=get_id_gen(), unique=True)
    original_filename = models.CharField(blank=True, max_length=300)

    file_content = models.FileField(upload_to=file_path, null=True, blank=True, unique=True)
    file_ext = models.CharField(max_length=24, blank=True)
    file_mime_type = models.CharField(max_length=64, default="text/plain")
    file_size_bytes = models.BigIntegerField(default=0)
    file_size_str = models.CharField(max_length=12, default="0 Bytes")
    thumbnail = ThumbnailerImageField(
        upload_to=thumb_path,
        null=True, blank=True,
        resize_source=dict(size=(200, 113), sharpen=True, crop=True, quality=70)
    )

    def save(self, *args, **kwargs):
        self.original_filename = self.file_content.name
        self.file_ext = get_ext(self.file_content.name)
        self.file_size_bytes = self.file_content.size
        self.file_size_str = get_filesize_str(self.file_content.size)
        self.file_mime_type = mime.guess_type(self.file_content.name)[0]
        self.icon = get_fontawesome(self.file_mime_type, self.file_ext)
        super(File, self).save(*args, **kwargs)

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
                "file_path": str(self.file_content),
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

    def __str__(self):
        return f'File: {self.reported_file.generated_filename}{self.reported_file.file_ext} Reported by: {self.reported_by.username}'

    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_user_set')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_by_set')
    reported_file = models.ForeignKey(File, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    reason_title = models.CharField(max_length=128)
    reason_body = models.TextField()


class FavouritedFile(models.Model):

    class Meta:
        verbose_name_plural = 'Favourites'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        orig = self.file.original_filename[:36]+"..." if len(str(self.file.original_filename)) > 36 else self.file.original_filename
        return f'{self.user.username} | {self.file.generated_filename} - {orig}'


class Image(models.Model):

    class Meta:
        verbose_name_plural = 'Images'

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=64, null=True, blank=True)
    mode = models.CharField(null=True, max_length=32)
    info = models.TextField(null=True, blank=True)
    is_web_safe = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if "svg" not in self.file.file_mime_type:
            img = PIL.Image.open(self.file.file_content.path)
            info = ""
            for k, v in img.info.items():
                if "exif" not in k and len(str(v)) < 128:
                    info += f"{k}: {v}<br/>"
            self.resolution = f'{img.width}x{img.height}'
            self.mode = img.mode
            self.info = info
            img.close()
        else:
            self.resolution = "Independent"
            self.info = None
            self.mode = None

        self.is_web_safe = is_websafe(self.file.file_ext)

        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.file.generated_filename}{self.file.file_ext} - uploaded by {self.file.user.username}'


class Video(models.Model):

    class Meta:
        verbose_name_plural = 'Videos'

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=64, null=True, blank=True)
    duration = models.IntegerField(default=0)
    fps = models.IntegerField(default=30)
    is_web_safe = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        video_clip = VideoFileClip(self.file.file_content.path)
        self.duration = video_clip.duration
        self.resolution = f'{video_clip.w}x{video_clip.h}'
        self.fps = video_clip.fps
        self.is_web_safe = is_websafe(self.file.file_ext)
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.file.generated_filename}{self.file.file_ext} - uploaded by {self.file.user.username}'


class Audio(models.Model):

    class Meta:
        verbose_name_plural = 'Audio'

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    sample_rate = models.IntegerField(default=0)
    is_web_safe = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        audio_clip = AudioFileClip(self.file.file_content.path)
        self.duration = audio_clip.duration
        self.sample_rate = audio_clip.fps
        self.is_web_safe = is_websafe(self.file.file_ext)
        super(Audio, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.file.generated_filename}{self.file.file_ext} - uploaded by {self.file.user.username}'


class Text(models.Model):

    class Meta:
        verbose_name_plural = 'Text'

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    characters = models.IntegerField(default=0)
    lines = models.IntegerField(default=0)
    syntax_highlighting = models.CharField(blank=True, max_length=32)

    def save(self, *args, **kwargs):
        self.characters, self.lines = get_chars_lines(self.file.file_content.path)
        self.syntax_highlighting = get_syntax_highlighting(self.file.file_ext, self.file.file_mime_type)
        super(Text, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.file.generated_filename}{self.file.file_ext} - uploaded by {self.file.user.username}'


@receiver(post_save, sender=File)
def create_file_subtype(sender, instance, **kwargs):
    ft = None
    if instance.file_mime_type.lower().startswith("image"):
        ft = Image.objects.create(file=instance)
    elif instance.file_mime_type.lower().startswith("video"):
        ft = Video.objects.create(file=instance)
    elif instance.file_mime_type.lower().startswith("audio"):
        ft = Audio.objects.create(file=instance)
    elif instance.file_mime_type.lower().startswith("text"):
        ft = Text.objects.create(file=instance)
    if ft:
        ft.save()


class ErrorVideo(models.Model):

    class Meta:
        verbose_name_plural = 'Error Videos'

    url = models.URLField(unique=True, blank=True)
    title = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.title

