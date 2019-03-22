from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField
from django.db import models
from django.utils import timezone
from mimetypes import MimeTypes
from moviepy.editor import VideoFileClip, AudioFileClip
from . import utils
import PIL.Image
import threading

"""
File:   models.py
Date:   13/02/2019
Last Updated: 16/02/2019
Author: 2086380A
"""

mime = MimeTypes()


class User(AbstractUser):
    """
    This User model extends the base django Auth User model and adds additional fields direcantly related to a user:

    - COLOUR : A user's hex-colour they choose when registering for an account. This colour is used for CSS styling.
    - UPLOAD_KEY : A user's private (randomly generated) upload key. Used for securely uploading content off-site (cURL)
    - WARNINGS : A user can be warned by an administrator 3 types before being permanently banned for ToS abuse.
    """
    colour = models.CharField(max_length=7, default="#00CCCC")
    upload_key = models.CharField(max_length=26, default=utils.get_upload_key())
    warnings = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class ErrorVideo(models.Model):
    """
    This model stores information about an error video that will be played whenevever
    the user visits /404 or encounters a PageNotFound error.

    - URL : YouTube video url to be embedded on error page.
    - TITLE : The title of the video
    """
    class Meta:
        verbose_name_plural = 'Error Videos'

    url = models.URLField(unique=True, blank=True)
    title = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.title


class Warned(models.Model):
    """
    This model stores information about all users that have been WARNED by an administrator.

    - WARNED_USER : Foreign key pointing to the User who has been warned
    - WARNED_BY : Foreign key pointing to the administrator that has banned the user.
    - DATE : Automatically obtained whenever this model is saved
    - REASON : A text-field expplaining the reason for why a user was banned (maybe can be emailed to user)

    All anned users will be logged.
    """
    class Meta:
        verbose_name_plural = 'Warned Users'
    
    warned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warned_user_set')
    warned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warned_by_admin_set')
    date = models.DateTimeField(default=timezone.now)
    reason = models.TextField(blank=False)

    def __str__(self):
        return f"Warned: {self.warned_user.username} by Administrator: {self.warned_by.username}"

class BannedUser(models.Model):
    """
    This model stores information about all users that have been banned by an administrator.

    - BANNED_USER : One to one relationship with a User (user can only be banned once)
    - BANNED_BY : Foreign key pointing to the administrator that has banned the user.
    - DATE : Automatically obtained whenever this model is saved
    - REASON : A text-field expplaining the reason for why a user was banned (maybe can be emailed to user)

    All banned users will be logged.
    """
    class Meta:
        verbose_name_plural = 'Banned Users'

    banned_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='banned_user_set')
    banned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banned_by_admin_set')
    date = models.DateTimeField(default=timezone.now)
    reason = models.TextField(blank=False)

    def __str__(self):
        return f"Banned: {self.banned_user.username} by Administrator: {self.banned_by.username}"


class File(models.Model):
    """
    This model stores general information about ANY file uploaded by a user. It also stores user-specific info such as:

    - IP : The IP address of the location where the file was uploaded
    - IS_PRIVATE : The privacy status of the file uploaded by the user.
    As well as general info listed below
    All banned users will be logged.
    """
    class Meta:
        verbose_name_plural = 'All Files'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    icon = models.CharField(blank=True, max_length=32)
    is_private = models.BooleanField(default=False)
    """Virus Scan is blank=True as not all files will be scanned with VirusTotal, only text and applications."""
    virus_scan = models.OneToOneField('VirusTotalScan', on_delete=models.CASCADE, null=True, blank=True)
    generated_filename = models.CharField(max_length=16, unique=True, default=utils.get_id_gen)
    """Linux supports filenames that are less than 256 chars in length."""
    original_filename = models.CharField(max_length=255, blank=True)

    file_content = models.FileField(
        upload_to=utils.file_path,
        unique=True
    )
    """
    Thumbnail automatically generated using easy-thumbnails and easy-thumbnails-ffmpeg python nodules.
    This field is blank/null=True as not all files will have a thumbnail, only images and videos.
    """
    file_thumbnail = ThumbnailerImageField(
        upload_to=utils.thumb_path,
        null=True,
        blank=True,
        resize_source=dict(
            size=(200, 113),
            sharpen=True,
            crop=True,
            quality=70
        )
    )
    file_ext = models.CharField(max_length=24, blank=True)
    file_mime_type = models.CharField(max_length=64, default="application/octet-stream")
    file_size_bytes = models.BigIntegerField(default=0)
    file_size_str = models.CharField(max_length=12, default="0 Bytes")
    """
    Below are one-to-one relationships between a file sub-type.
    These fields are left blank on file upload and established after the file sub-type is saved.
    """
    file_image = models.OneToOneField('Image', on_delete=models.CASCADE, blank=True, null=True)
    file_video = models.OneToOneField('Video', on_delete=models.CASCADE, null=True, blank=True)
    file_audio = models.OneToOneField('Audio', on_delete=models.CASCADE, null=True, blank=True)
    file_text = models.OneToOneField('Text', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        
        self.file_mime_type = mime.guess_type(self.file_content.name)[0]
        self.original_filename = self.file_content.name.split("/")[-1].replace(self.generated_filename+'_', '')
        self.file_ext = utils.get_ext(self.file_content.name)
        self.file_size_bytes = self.file_content.size
        self.file_size_str = utils.get_filesize_str(self.file_content.size)
        
        # see https://github.com/denBot/WAD2-Group-Project/issues/35#issuecomment-472485161
        if self.file_mime_type is None:
            self.file_mime_type = 'application/octet-stream'

        self.icon = utils.get_fontawesome(self.file_mime_type, self.file_ext)
        # Hangs just here for pdf

        super(File, self).save(*args, **kwargs) 

    def __str__(self):
        orig = self.original_filename[:36]+"..." if len(str(self.original_filename)) > 36 else self.original_filename
        return f'{self.generated_filename} - {orig}'


class ReportedFile(models.Model):
    """
    This model holds information on reports submitted by authenticated/anonymous users.

    REPORTED_USER : Points to the user who's file has been reported
    REPORTED_BY : Points to the user who reported the file (may be anonymous, hence blank=True)
    REPORTED_FILE : Points to the reported file in question
    DATE : Automatically obdainted on model.save()
    REASON_TITLE : A short-string where user can select options (Copyright Infringement, Privacy Abuse etc...)
    REASON_BODY : A large-strong textfield where user can write detailed message about why they are reporting file.
    """
    class Meta:
        verbose_name_plural = 'Reported Files'

    def __str__(self):
        return f'File: {self.reported_file.generated_filename}{self.reported_file.file_ext} ' \
               f'Reported by: {self.reported_by.username}'
    
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_by_set', blank=True)
    reported_file = models.ForeignKey(File, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    reason_title = models.CharField(max_length=128)
    reason_body = models.TextField()


class FavouritedFile(models.Model):
    """
    This model holds all files that have been favourited by users.

    USER : Points to user that can add/delete a file favourite
    FILE : Points to file that has been favourtied
    DATE : Automatically ontained on model.save()
    """
    class Meta:
        verbose_name_plural = 'Favourites'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):

        orig = self.file.original_filename[:36]+"..." \
            if len(str(self.file.original_filename)) > 36 \
            else self.file.original_filename

        return f'{self.user.username} | {self.file.generated_filename} - {orig}'


class Image(models.Model):
    """
    This model is a sub-file type Image and holds detailed information related the image that has been uploaded.

    FILE_POINTER : Points to the File that has been uploaded
    RESOLUTION : Image resolution (e.g. 600x400)
    MODE : Image mode (ADOBE etc...)
    INFO : Additional image info obtained from PIL
    IS_WEB_SAFE : A boolean checking if the image can be embedded via HTML (is jpg, png, etc...)
    """
    class Meta:
        verbose_name_plural = 'Images'

    file_pointer = models.ForeignKey(File, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=64, null=True, blank=True)
    mode = models.CharField(null=True, max_length=32)
    info = models.TextField(null=True, blank=True)
    is_web_safe = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if "svg" not in self.file_pointer.file_mime_type:
            img = PIL.Image.open(self.file_pointer.file_content.path)
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

        self.is_web_safe = utils.is_websafe(self.file_pointer.file_ext)

        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.file_pointer.generated_filename}{self.file_pointer.file_ext} - ' \
               f'uploaded by {self.file_pointer.user.username}'


class Video(models.Model):
    """
    This model is a sub-file type Video and holds detailed information related the video that has been uploaded.

    FILE_POINTER : Points to the File that has been uploaded
    RESOLUTION : Video resolution (e.g. 600x400)
    DURATION : The duration of the video in seconds (int)
    FPS : The frames per second of the video
    IS_WEB_SAFE : A boolean checking if the video can be embedded via HTML (is mp4, webm, ogv etc...)
    """
    class Meta:
        verbose_name_plural = 'Videos'

    file_pointer = models.ForeignKey(File, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=64, null=True, blank=True)
    duration = models.IntegerField(default=0)
    fps = models.IntegerField(default=30)
    is_web_safe = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        video_clip = VideoFileClip(self.file_pointer.file_content.path)
        self.duration = video_clip.duration
        self.resolution = f'{video_clip.w}x{video_clip.h}'
        self.fps = video_clip.fps
        self.is_web_safe = utils.is_websafe(self.file_pointer.file_ext)
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.file_pointer.generated_filename}{self.file_pointer.file_ext} - ' \
               f'uploaded by {self.file_pointer.user.username}'


class Audio(models.Model):
    """
    This model is a sub-file type Audio and holds detailed information related the audio that has been uploaded.

    FILE_POINTER : Points to the File that has been uploaded
    DURATION : The duration of the audio in seconds (int)
    SAMPLE_RATE : The sample rate of the audio in mhz
    IS_WEB_SAFE : A boolean checking if the video can be embedded via HTML (is mp3, ogg, flac...)
    """
    class Meta:
        verbose_name_plural = 'Audio'

    file_pointer = models.ForeignKey(File, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    sample_rate = models.IntegerField(default=0)
    is_web_safe = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        audio_clip = AudioFileClip(self.file_pointer.file_content.path)
        self.duration = audio_clip.duration
        self.sample_rate = audio_clip.fps
        self.is_web_safe = utils.is_websafe(self.file_pointer.file_ext)
        super(Audio, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.file_pointer.generated_filename}{self.file_pointer.file_ext} -' \
               f' uploaded by {self.file_pointer.user.username}'


class Text(models.Model):
    """
    This model is a sub-file type Text and holds detailed information related the text that has been uploaded.

    FILE_POINTER : Points to the File that has been uploaded
    CHARACTERS : The number of characters in the file
    LINES : The number of lines in the file
    SYNTAX_HIGHLIGHTING : Checks if the file has a syntax supported by HLJS (highlight.js)
    """
    class Meta:
        verbose_name_plural = 'Text'

    file_pointer = models.ForeignKey(File, on_delete=models.CASCADE)
    characters = models.IntegerField(default=0)
    lines = models.IntegerField(default=0)
    syntax_highlighting = models.CharField(blank=True, max_length=32)

    def save(self, *args, **kwargs):
        self.characters, self.lines = utils.get_chars_lines(self.file_pointer.file_content.path)
        self.syntax_highlighting = utils.get_syntax_highlighting(
            self.file_pointer.file_ext,
            self.file_pointer.file_mime_type
        )
        super(Text, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.file_pointer.generated_filename}{self.file_pointer.file_ext} - ' \
               f'uploaded by {self.file_pointer.user.username}'


class VirusTotalScan(models.Model):
    """
    This model holds all virustotal information of files/applications that have been scanned by the VirusTotal API
    As this API is limited to 4 scans per minute... we way need to change it in the future or move to the PRIVATE api
    Preferably, we will also implement server-side ClamAD virus scanning for file upload validation.

    FILE_POINTER : Points to the File that has been uploaded
    MD5 : The MD5 of the scanned file
    PERMALINK : The PERMALINK to virustotal scan results
    """
    class Meta:
        verbose_name_plural = 'VirusTotal Scans'

    file_pointer = models.ForeignKey(File, on_delete=models.CASCADE)
    md5 = models.CharField(max_length=128)
    permalink = models.URLField()

    def __str__(self):
        return f'Virus report for: {self.file_pointer.generated_filename}{self.file_pointer.file_ext}'

def get_virus_info(file_id):

    f = File.objects.get(id=file_id)
    # If file is text or other... (not image, video, audio) send request to virustotal
    virus_data = utils.scan_file(f.file_content.path)
    
    # If we get a response code of 200, all is ok... put results into VirusTotalScan model
    if virus_data.get("response_code", None) == 200:
        VirusTotalScan.objects.create(
            file_pointer=f,
            md5=virus_data["results"]["md5"],
            permalink=virus_data["results"]["permalink"]
        ).save()

@receiver(post_save, sender=File)
def create_file_subtype(sender, instance, created, **kwargs):
    """
    This function gets called after the File model is saved.
    If the file mimetype is an image, video, audio or text, we will try and gather ADDITIONAL info on that file.
    This info will be saved in a Image, Video, Audio or Text model, along with a pointer to the original file.

    :param sender: - Not used... required parameter.
    :param instance: - The file instance
    :param kwargs: - Not used... required parameter.
    :return: null
    """
    # Break recursion by changing value of instance.proceed after saving a file subtype
    if created:

        mimetype = instance.file_mime_type

        # Create a sub-file model based on the mimetype of the file that has just been saved.

        if mimetype.startswith("image"):
            Image.objects.create(file_pointer=instance).save()

        if mimetype.startswith("video"):
            Video.objects.create(file_pointer=instance).save()

        if mimetype.startswith("audio"):
            Audio.objects.create(file_pointer=instance).save()

        if mimetype.startswith("text"):
            Text.objects.create(file_pointer=instance).save()
        
        if mimetype.startswith("text") or mimetype.startswith("application"):
            t = threading.Thread(target=get_virus_info, args=(instance.id,))
            t.start()

# Below code prevents File post_save receiver from executing
@receiver(post_save, sender=VirusTotalScan)
def create_file_virus_scan(sender, instance, **kwargs):
    f = File.objects.filter(id=instance.file_pointer.id).first()
    f.virus_scan = instance
    f.save()


"""
The below functions are called whenever an Image, Video, Audio or Text model is saved.

- Get the file that matches the id of the file referenced to in the `file_pointer` field of the sub-file model.
- Set file_*** to the sender instance creating a one to one relationship between the original file 
  ... and it's additional info stored as a sub-model.

:param sender: - Not used... required parameter.
:param instance: - The image/video/audio/text instance
:param kwargs: - Not used... required parameter.
:return: null
"""


@receiver(post_save, sender=Image)
def create_file_image_subtype(sender, instance, **kwargs):
    f = File.objects.filter(id=instance.file_pointer.id).first()
    f.file_image = instance
    f.save()


@receiver(post_save, sender=Video)
def create_file_video_subtype(sender, instance, **kwargs):
    f = File.objects.filter(id=instance.file_pointer.id).first()
    f.file_video = instance
    f.save()


@receiver(post_save, sender=Audio)
def create_file_audio_subtype(sender, instance, **kwargs):
    f = File.objects.filter(id=instance.file_pointer.id).first()
    f.file_audio = instance
    f.save()


@receiver(post_save, sender=Text)
def create_file_text_subtype(sender, instance, **kwargs):
    f = File.objects.filter(id=instance.file_pointer.id).first()
    f.file_text = instance
    f.save()


"""
The below functions are called whenever:
- a new file is reported
- a user is warned
- a user creates an account
- a user is banned.

On these events, an email is sent out either to the user or an administrator depending on the context of the email.
"""
@receiver(post_save, sender=User)
def create_user_acc(sender, instance, created, **kwargs):
    if created:
        title = 'Woohoo! Your super cool NootTech account has been created!'

        msg_html = render_to_string('email/new_user.html', {
            'username': instance.username,
            'upload_key': instance.upload_key,
        })
        
        if settings.EMAIL_ENABLED:
            send_mail(
                title,
                '',
                'no-reply@noot.tech',
                [instance.email],
                html_message=msg_html,
            )

@receiver(post_save, sender=ReportedFile)
def new_report_submitted(sender, instance, created, **kwargs):
    if created:
        title = f"New file report: {instance.reported_file.generated_filename} by {instance.reported_file.user.username}"
        
        msg_html = render_to_string('email/new_report.html', {
            'username': instance.reported_file.user.username,
            'instance' : instance,
            'admin': True
        })
        
        if settings.EMAIL_ENABLED:
            send_mail(
                title,
                '',
                'no-reply@noot.tech',
                ['contact@noot.tech'],
                html_message=msg_html,
            )

@receiver(post_save, sender=Warned)
def notify_warned_user(sender, instance, created, **kwargs):
    if created:
        title = 'You have recieved a warning from an administrator.'

        msg_html = render_to_string('email/user_warned.html', {
            "username": instance.warned_user.username,
            "instance": instance
        })

        if settings.EMAIL_ENABLED:
            send_mail(
                title,
                '',
                'no-reply@noot.tech',
                [instance.warned_user.email],
                html_message=msg_html,
            )

@receiver(post_save, sender=BannedUser)
def notify_banned_user(sender, instance, created, **kwargs):
    if created:
        title = "Your account has been banned... here's why."

        msg_html = render_to_string('email/user_banned.html', {
            "username": instance.banned_user.username,
            "instance": instance
        })

        if settings.EMAIL_ENABLED:
            send_mail(
                title,
                '',
                'no-reply@noot.tech',
                [instance.banned_user.email],
                html_message=msg_html,
            )