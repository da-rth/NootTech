from .utils import get_upload_key, upload_authentication_failure, get_ip, get_id_gen, get_ext
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, viewsets
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from . import serializers
from .models import *
import traceback

htp = "https" if settings.HTTPS else "http"

# Get List of user uploads


class ErrorVideoAPIView(generics.ListAPIView):
    """
    Returns a list of videos used (randomly) at website 404 page.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.ErrorVideoSerializer
    queryset = ErrorVideo.objects.all()


class ListFilesAPIView(generics.ListAPIView):
    """
    Returns a list of files belonging to an Authenticated user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ListFilesSerializer

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)


class GetSetSettingsAPIView(generics.ListCreateAPIView):
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
        if serializer.validated_data.get('gen_upload_key'):
            # If "upload_key" exists and is set to True
            u.upload_key = get_upload_key()

        u.save()


class CreateUserAPIView(generics.ListCreateAPIView):
    '''
        This API will Take in  POST request of user informations and create a new User
    '''

    permission_classes = (AllowAny,)
    serializer_class = serializers.CreateUserSerializer
    queryset = User.objects.all()
    '''
        API for creating a user
        Process of checking valid data to be reviewed
        :return:
    '''


class ListFavouritesAPIView(generics.ListCreateAPIView):
    '''
        This API Will POST the files favourite by a user, Create new favourites, delete already favourite files
        Needs tweeking, need model to be created
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SerializeFavouritesList

    def get_queryset(self):
        return FavouritedFile.objects.filter(user=self.request.user)


class AddFavouriteAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SerializeFavourite

    def get_queryset(self):
        return FavouritedFile.objects.filter(user=self.request.user)


class DeleteFavouriteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return FavouritedFile.objects.filter(user=self.request.user)


class ReportListAPIView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.ReportList
    queryset = ReportedFile.objects.all()


class ReportAddAPIView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.ReportAdd
    queryset = ReportedFile.objects.all()


class DeleteFileAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)


class SubdomainViewSet(viewsets.ViewSet):

    permission_classes = (AllowAny,)

    def field(self, request, username, gen_name):

        user = User.objects.filter(username=username).first()
        file = File.objects.filter(user=user, generated_filename=gen_name).first()
        serializer = serializers.ListFilesSerializer(file)
        data = serializer.data
        if user and file:
            file.views += 1
            file.save()
            return Response({'file': data if not file.is_private else None, 'colour': user.colour})
        else:
            return Response({'file': None, 'colour': user.colour if user else None})


class BanViewSet(viewsets.ViewSet):

    permission_classes = (IsAdminUser,)

    def field(self, request, pk):
        user = User.objects.filter(id=pk).first()

        if user:
            user.is_active = False
            files = File.objects.filter(user=user)
            files.delete()
            user.save()

            banned_user = BannedUser(
                banned_by=self.request.user,
                banned_user=user,
                reason="User was very very bad! >:("
            )
            banned_user.save()
            # LOG BAN HERE
            # LOG FILES DELETED HERE
            return Response({'banned': True})
        else:
            return Response({'banned': False})


class WarnViewSet(viewsets.ViewSet):

    permission_classes = (IsAdminUser,)

    def field(self, request, pk):
        # reason = ...
        user = User.objects.filter(id=pk).first()

        if user:

            user.warnings += 1
            autoban = False

            warning = Warnings(
                warned_by=self.request.user,
                warned_user=user,
                reason="User was a little bad..."
            )
            warning.save()

            if user.warnings > 3:
                autoban = True
                user.is_active = False
                files = File.objects.filter(user=user)
                files.delete()
                ban = BannedUser(
                    banned_by=self.request.user,
                    banned_user=user,
                    reason="User was very very bad! >:("
                )
                ban.save()
            user.save()

            # LOG WARNING HERE
            return Response({'warned': True, 'autoban': autoban, 'warnings': user.warnings})
        else:
            return Response({'warned': False, 'autoban': False, 'warnings': None})


@method_decorator(csrf_exempt, name='dispatch')
class UploadView(View):

    @csrf_exempt
    def post(self, request):

        uploaded_files = []

        if request.user.is_authenticated:
            upload_user = User.objects.get(id=request.user.id)
            username = upload_user.username
        else:
            invalid_field_message = upload_authentication_failure(request, User)
            if invalid_field_message:
                return invalid_field_message
            username = request.POST["username"]
            upload_user = get_object_or_404(User, username=username, upload_key=request.POST["upload_key"])

            if not upload_user.is_active:
                return HttpResponse(f"Your account is no longer active.\n"
                                    f"If you think this is a mistake, "
                                    f"please visit: {htp}://{settings.DOMAIN_NAME}/contact")

        for user_file in request.FILES.getlist('content'):
            ip = get_ip(request)

            try:
                ext = get_ext(user_file.name)
                if ext in [".gif", ".jpg", ".jpeg", ".png", ".mp4", ".webm", ".ogv", ".ico", ".apng", ".bmp"]:

                    uploaded_file = File(
                        user=upload_user,
                        generated_filename=get_id_gen(),
                        ip=ip,
                        file_content=user_file,
                        file_thumbnail=user_file
                    )
                else:
                    uploaded_file = File(
                        user=upload_user,
                        generated_filename=get_id_gen(),
                        ip=ip,
                        file_content=user_file
                    )

                uploaded_file.save()

                print(uploaded_file.original_filename, uploaded_file.generated_filename)

                if settings.SUBDOMAIN:
                    uploaded_files.append(f"{htp}://{username}.{settings.DOMAIN_NAME}/{uploaded_file.generated_filename}")
                else:
                    uploaded_files.append(f"{htp}://{settings.DOMAIN_NAME}/u/{username}/{uploaded_file.generated_filename}")

            except Exception as e:

                print(f"Upload for {user_file} failed")
                traceback.print_exc()
                uploaded_files.append(f"Failed to upload: {user_file}\n")

        return HttpResponse(" \n".join(uploaded_files))

    def get(self, request):
        return redirect('/')
