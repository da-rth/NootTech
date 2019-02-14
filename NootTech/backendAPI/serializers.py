from rest_framework import serializers
from .models import User, ErrorVideo, File
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class ListUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'colour', 'is_admin')


class ListFilesSerializer(serializers.ModelSerializer):

    uploader_id = serializers.CharField(source='user.id')
    uploader = serializers.CharField(source='user.username')

    class Meta:
        model = File
        fields = '__all__'

class FavouriteFiles(serializers.ModelSerializer):
    '''
    Serializer for favourite files
    '''
    uploader_id = serializers.CharField(source='user.id')
    uploader = serializers.CharField(source='user.username')

    class Meta:
        model = File
        field = '__all__'

class CreateFavouriteFiles(serializers.ModelSerializer):
    '''
    Serializer to create a new favourite file, need counselling on what to do
    '''
    user = serializers.CharField(write_only= True)
    'Not Sure About parentesis content'
    file =serializers.FileField()
    date = serializers.DateField(write_only= True)
    class Meta:
        model = File
        field = ('user','file','date')

    def create(self,new_file):

        file = FavouriteFiles(
        user = new_file['user'],
        file=new_file['file'],
        date=new_file['date'],
        )
        '''
        Validation to write
        :param new_file:
        Informations about the new File
        :return:
        '''

class CreateUserSerializer(serializers.ModelSerializer):

    email = serializers.CharField(write_only= True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    colour = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','email','color','password')

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
    email = serializers.CharField(allow_null=True)

    class Meta:
        model = User
        fields = ('colour', 'email', 'warnings', 'upload_key', 'gen_upload_key')



