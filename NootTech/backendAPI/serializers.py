from rest_framework import serializers
from collections import OrderedDict
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from . import validators

class UserSerializer(serializers.ModelSerializer):
    """
    This serializer allows for four fields to be posted; username, email, colour and password
    All of these fields will then go through validation
    If successful, the create() method will automatically be called.
    It will then proceed to validate the password and create the user - validation errors return BadRequest responses
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'warnings')


class CreateUserSerializer(serializers.ModelSerializer):
    """
    This serializer allows for four fields to be posted; username, email, colour and password
    All of these fields will then go through validation
    If successful, the create() method will automatically be called.
    It will then proceed to validate the password and create the user - validation errors return BadRequest responses
    """
    email = serializers.CharField(validators =[validators.validate_email],write_only= True )
    username = serializers.CharField(validators =[validators.validate_username],write_only=True)
    password = serializers.CharField(style = {'input_type': 'password'}, write_only=True)
    colour = serializers.CharField(validators =[validators.validate_colour],write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'colour', 'password')

    def create(self, validated_data):

        user = User(username=validated_data['username'], email=validated_data['email'], colour=validated_data['colour'])

        try:
            # Try to validate password and create account
            validate_password(password=validated_data['password'], user=user)

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        # If successful, set password and save user (created! woohoo!)
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class VirusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirusTotalScan
        fields = '__all__'

class DeleteAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for allowing user to delete an account, provided confirmation_password
    """
    confirmation_password = serializers.CharField(style = {'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('confirmation_password',)

class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for allowing user to change their password. Input types are set to password.
    """
    old_password = serializers.CharField(style = {'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(style = {'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('old_password', 'new_password')

class AddFavSerializer(serializers.ModelSerializer):
    """
    A serialiser for adding favourited files.
    """
    class Meta:
        model = FavouritedFile
        fields = '__all__'

class ImageFileSerializer(serializers.ModelSerializer):
    """
    Serializer used for File Sub-type : Image
    Exclusdes the file-pointer and id fields from being serialized
    """
    class Meta:
        model = Image
        exclude = ('file_pointer', 'id')


class VideoFileSerializer(serializers.ModelSerializer):
    """
    Serializer used for File Sub-type : Video
    Exclusdes the file-pointer and id fields from being serialized
    """
    class Meta:
        model = Video
        exclude = ('file_pointer', 'id')


class AudioFileSerializer(serializers.ModelSerializer):
    """
    Serializer used for File Sub-type : Audio
    Exclusdes the file-pointer and id fields from being serialized
    """
    class Meta:
        model = Audio
        exclude = ('file_pointer', 'id')


class TextFileSerializer(serializers.ModelSerializer):
    """
    Serializer used for File Sub-type : Text
    Exclusdes the file-pointer and id fields from being serialized
    """
    class Meta:
        model = Text
        exclude = ('file_pointer', 'id')


class ListFilesSerializer(serializers.ModelSerializer):
    """
    This serializer serializes a File Object, merging it with any additional file information relevant to the file.
    Additional info is gathered by the 4 serializers below. If no info is found for that sub-type of file, then its null

    The method to_representation() simply skips any keys/values
    where the value is null, preventing them from being serialized.
    I (Daniel) found out how to do this from: https://stackoverflow.com/a/45569581
    """
    file_image_info = ImageFileSerializer(source='file_image')
    file_video_info = VideoFileSerializer(source='file_video')
    file_audio_info = AudioFileSerializer(source='file_audio')
    file_text_info = TextFileSerializer(source='file_text')
    virus_info = VirusSerializer(source='virus_scan')
    user = UserSerializer()

    class Meta:
        model = File
        exclude = ('file_image', 'file_video', 'file_audio', 'file_text', 'virus_scan')

    def to_representation(self, instance):
        result = super(ListFilesSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class UpdateFileSerializer(serializers.ModelSerializer):
    """
    Used when updating information of a file, or deleting a file.
    """
    gen_new_id = serializers.BooleanField(default=False)
    toggle_private = serializers.BooleanField(default=False)
    delete = serializers.BooleanField(default=False)
    
    class Meta:
        model = File
        fields = ('gen_new_id', 'toggle_private', 'delete', 'original_filename')
    
class PublicFileSerializer(serializers.ModelSerializer):
    """
    Used by sharelink page for obtaining public info about a file.
    """
    file_image_info = ImageFileSerializer(source='file_image')
    file_video_info = VideoFileSerializer(source='file_video')
    file_audio_info = AudioFileSerializer(source='file_audio')
    file_text_info = TextFileSerializer(source='file_text')
    virus_info = VirusSerializer(source='virus_scan')

    class Meta:
        model = File
        exclude = ('file_image', 'file_video','file_audio', 'file_text', 'virus_scan', 'ip')

    def to_representation(self, instance):
        result = super(PublicFileSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class SerializeFavouritesList(serializers.ModelSerializer):
    """
    This serializer takes a file (favourited by a user) and returns a small amount of the file's attributes
    Such as its original filename, gen name, thumbnail, icon, extension and (fontawesome) icon
    """
    icon = serializers.CharField(source='file.icon', read_only=True)
    username = serializers.CharField(source='file.user.username', read_only=True)
    ext = serializers.CharField(source='file.file_ext', read_only=True)
    gen =serializers.CharField(source='file.generated_filename', read_only=True)
    original = serializers.CharField(source='file.original_filename', read_only=True)
    thumbnail = serializers.CharField(source='file.file_thumbnail', read_only=True)

    class Meta:
        model = FavouritedFile
        fields = ('id', 'original', 'ext', 'icon', 'gen', 'username', 'thumbnail')


class SerializeFavourite(serializers.ModelSerializer):
    """
    This serializer serilizes the FavouritedFile mode, for adding a new favourite.
    """
    class Meta:
        model = FavouritedFile
        fields = '__all__'



class ErrorVideoSerializer(serializers.ModelSerializer):
    """
    Basic serializer for turning ErorVideo model queryset into JSON
    Note: __all__ simply includes two fields: url and title
    """
    class Meta:
        model = ErrorVideo
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    """
    This serializer is used to convert colour, email, warnings and upload_key of the currently authenticated user
    The aforementioned fields can also be set through a POST request
    """
    gen_upload_key = serializers.BooleanField(default=False, allow_null=True, write_only=True, required=False)
    email = serializers.CharField(validators =[validators.validate_email], allow_null=True, required=False)
    colour = serializers.CharField(validators =[validators.validate_colour], allow_null=True, required=False)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('colour', 'email', 'warnings', 'upload_key', 'gen_upload_key', 'is_superuser')


class ReportList(serializers.ModelSerializer):
    """
    Serializer for a list of reports (viewed by admin), additional info on report is provided.
    Additional info is obtained using the serializers.CharField parameter "source" as shown below:
    """
    reported_user_name = serializers.CharField(source="reported_user.username", read_only=True)
    reported_by_name = serializers.CharField(source="reported_by.username", read_only=True)
    reported_file = ListFilesSerializer()

    class Meta:
        model = ReportedFile
        fields = '__all__'


class ReportAdd(serializers.ModelSerializer):
    """
    Basic serializer for reporting a user
    As the date is automatically obtained, it is added to the excluded fields list
    """
    class Meta:
        model = ReportedFile
        exclude = ('date',)


class WarningList(serializers.ModelSerializer):
    """
    Serializer for a list of warnings recieved by a user from an admin.
    """
    warned_user_name = serializers.CharField(source="warned_user.username", read_only=True)
    warned_by_name = serializers.CharField(source="warned_by.username", read_only=True)

    class Meta:
        model = Warned
        exclude = ('warned_user', 'warned_by')

class WarningAdd(serializers.ModelSerializer):
    """
    Basic serializer for warning a user
    """
    class Meta:
        model = Warned
        exclude = ('date', 'warned_by')

class BanAdd(serializers.ModelSerializer):
    """
    Basic serializer for warning a user
    """
    class Meta:
        model = BannedUser
        exclude = ('date', 'banned_by')
