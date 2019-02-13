from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.hashers import check_password
from .models import ErrorVideo, User ,File
from .utils import get_upload_key
from . import serializers


# Get List of user uploads
class ListUsers(generics.ListAPIView):
    """
    Returns a list of users with basic information (check ListUsersSerializer to see what info is sent in response)
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.ListUsersSerializer
    ordering = ('-id',)

    def get_queryset(self):
        return User.objects.all()


class ErrorVideoView(generics.ListAPIView):
    """
    Returns a list of videos used (randomly) at website 404 page.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.ErrorVideoSerializer

    def get_queryset(self):
        return ErrorVideo.objects.all()


class ListFilesView(generics.ListAPIView):
    """
    Returns a list of files belonging to an Authenticated user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ListFilesSerializer

    def get_queryset(self):
        return File.objects.filter(user = self.request.user,is_deleted = False)



class SettingsView(generics.ListCreateAPIView):
    """
    Returns a list of settings on GET request for an AUTHENTICATED user
    Updates specific settings sent over via POST request for an AUTENTICATED user
    TODO: Validate the email address and colour chosen by the user. Is the colour a hex? Is the email real?
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SettingsSerializer

    def get_queryset(self):
        # This API returns only the settings for the currently logged in user.
        # So a member cannot get other members settings (upload key, etc...).
        return User.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        # Override the perform_create method to UPDATE a user instead of CREATE one.
        # Get the object for the current authenticated user (logged in)
        u = User.objects.get(id=self.request.user.id)

        # If the variables colour, email or upload_key have been recieved via POST request
        # Update user object with these values...
        if serializer.validated_data.get('colour'):
            # if "colour" exists and isn't an empty string
            u.colour = serializer.validated_data.get('colour')
        if serializer.validated_data.get('email'):
            # If "email" exists and isn't an empty string
            u.email = serializer.validated_data.get('email')
        if serializer.validated_data.get('gen_upload_key') == True:
            # If "upload_key" exists and is set to True
            u.upload_key = get_upload_key()

        u.save()



