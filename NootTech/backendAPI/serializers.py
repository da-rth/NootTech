from rest_framework import serializers
from collections import OrderedDict
from .models import User, ErrorVideo, File, FavouritedFile, ReportedFile, Image, Video, Audio, Text
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from . import validators


class ListUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'colour')


class ImageFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class VideoFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'


class AudioFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Audio
        fields = '__all__'


class TextFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Text
        fields = '__all__'


class ListFilesSerializer(serializers.ModelSerializer):

    uploader_id = serializers.CharField(source='user.id')
    uploader = serializers.CharField(source='user.username')
    file_image_info = ImageFileSerializer(source='file_image')
    file_video_info = VideoFileSerializer(source='file_video')
    file_audio_info = AudioFileSerializer(source='file_audio')
    file_text_info = TextFileSerializer(source='file_text')

    class Meta:
        model = File
        fields = '__all__'

    def to_representation(self, instance):
        # Omit null fields : https://stackoverflow.com/a/45569581
        result = super(ListFilesSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class FavouriteFiles(serializers.ModelSerializer):
    '''
    Serializer for favourite files
    '''
    generated_filename = serializers.CharField(source='file.generated_filename')
    original_filename = serializers.CharField(source='file.original_filename')
    file_url = serializers.CharField(source='file.file_content')
    uploader = serializers.CharField(source='file.user.username')
    icon = serializers.CharField(source='file.icon')
    thumbnail = serializers.CharField(source='file.thumbnail')

    class Meta:
        model = FavouritedFile
        fields = ('id', 'generated_filename', 'original_filename', 'icon', 'thumbnail', 'file_url', 'uploader')


class DeleteFavourite(serializers.ModelSerializer):
    '''
    API for deleting Files
    '''
    class Meta:
        model = FavouritedFile
        fields = ('file','user')


class CreateUserSerializer(serializers.ModelSerializer):

    email = serializers.CharField(validators =[validators.validate_email],write_only= True )
    username = serializers.CharField(validators =[validators.validate_username],write_only=True)
    password = serializers.CharField(style = {'input_type': 'password'}, write_only=True)
    colour = serializers.CharField(validators =[validators.validate_colour],write_only=True)

    class Meta:
        model = User
        fields = ('username','email','colour','password')

    def create(self, validated_data):
        password = validated_data['password']

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            colour=validated_data['colour'],
        )

        try:
            validate_password(password=validated_data['password'], user=user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        user.set_password(password)
        user.save()
        return validated_data


class ErrorVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorVideo
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    gen_upload_key = serializers.BooleanField(default=False)
    email = serializers.CharField(validators =[validators.validate_email],allow_null=True)
    colour = serializers.CharField(validators =[validators.validate_colour],write_only=True)

    class Meta:
        model = User
        fields = ('colour', 'email', 'warnings', 'upload_key', 'gen_upload_key')


class ReportList(serializers.ModelSerializer):
    reported_user_name = serializers.CharField(source="reported_user.username")
    reported_by_name = serializers.CharField(source="reported_by.username")
    file_gen_name = serializers.CharField(source="reported_file.generated_filename")
    file_orig_name = serializers.CharField(source="reported_file.original_filename")
    file_url = serializers.CharField(source="reported_file.file_content")
    class Mete:
        model = ReportedFile
        fields = '__all__'


class ReportAdd(serializers.ModelSerializer):
    class Mete:
        model = ReportedFile
        fields = '__all__'



