from .utils import get_upload_key, upload_authentication_failure, get_ip, get_id_gen, get_ext
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from . import serializers
from .models import *
import traceback
import logging
log = logging.getLogger(__name__)

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
        return File.objects.filter(user=self.request.user).order_by('-date')


class GetSetSettingsAPIView(generics.ListCreateAPIView):
    """
    Returns a list of settings on GET request for an AUTHENTICATED user
    Updates specific settings sent over via POST request for an AUTENTICATED user
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

class WarningListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.WarningList

    def get_queryset(self):
        return Warned.objects.filter(warned_user=self.request.user)


class DeleteFileAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

class ToggleFilePrivacyAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PrivacyFile

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

    def update(self, request, pk):
        try:
            file = File.objects.get(user=self.request.user, id=pk)
            file.is_private = not file.is_private
            file.save()
            log.info(f"[FILE-PRIVACY] : USER: {self.request.user.username} TOGGLED PRIVACY FOR FILE WITH ID {pk}")
            return Response({'is_private': file.is_private}, status=status.HTTP_200_OK)
        except File.DoesNotExist:
            log.warn(f"[FILE-PRIVACY] : USER: {self.request.user.username} TRIED TO TOGGLE PRIVACY FOR NON EXISTING FILE WITH ID {pk}")
            return Response({'detail':f'The file with id {pk} uploaded by {self.request.user.username} could not be found.'},
                            status=status.HTTP_404_NOT_FOUND
            )


class SubdomainViewSet(viewsets.ViewSet):

    permission_classes = (AllowAny,)

    def field(self, request, username, gen_name):

        user = User.objects.filter(username=username).first()
        file = File.objects.filter(user=user, generated_filename=gen_name).first()
        serializer = serializers.PublicFileSerializer(file)
        data = serializer.data
        if user and file:
            file.views += 1
            file.save()
            return Response({'file': data if not file.is_private else None, 'colour': user.colour}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'The file with gen id {gen_name} belonging to {username} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


class BanAPIView(generics.CreateAPIView):

    permission_classes = (IsAdminUser,)
    serializer_class = serializers.BanAdd
    queryset = BannedUser.objects.all()

    def create(self, request, *args, **kwargs):

        reason = request.POST.get('reason', "Not given by admin")
        ban_uid = request.POST.get('warned_user', None)
        ban_user = User.objects.get(id=ban_uid)

        if ban_user:

            if ban_user.is_staff:
                log.warn(f"[BAN-USER] : USER: {request.user.username} TRIED TO BAN STAFF MEMBER {ban_user.username}.")
                return Response({'detail':'You cannot ban another staff member.'}, status=status.HTTP_400_BAD_REQUEST)
            
            ban_user.is_active = False
            files = File.objects.filter(user=ban_user)
            files.delete()
            ban_user.save()

            banned_user = BannedUser(
                banned_by=self.request.user,
                banned_user=ban_user,
                reason=reason
            )
            banned_user.save()            
            log.info(f"[BAN-USER] : USER: {ban_user.username} BANNED BY: {self.request.user.username}")
            return Response({'banned': True}, status=status.HTTP_201_CREATED)
        else:
            log.warn(f"[BAN-USER] : FAILED TO BAN USER WITH ID: {ban_uid}, REQUESTED BY: {self.request.user.username}")
            return Response({'detail':'The user you tried to ban does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


class WarnAPIView(generics.CreateAPIView):

    permission_classes = (IsAdminUser,)
    serializer_class = serializers.WarningAdd
    queryset = Warned.objects.all()

    def create(self, request, *args, **kwargs):
        
        autoban = False
        reason = request.POST.get('reason', "Not given by administrator.")

        warned_uid = request.POST.get('warned_user', None)
        warned_user = User.objects.get(id=warned_uid)

        if warned_user:
            
            if warned_user.is_staff:
                log.warn(f"[WARN-USER] : USER: {request.user.username} TRIED TO WARN STAFF MEMBER {warned_user.username}.")
                return Response({'detail': 'You cannot warn another staff member.'}, status=status.HTTP_403_FORBIDDEN)

            warned_user.warnings += 1
            
            warning = Warned(
                warned_by=self.request.user,
                warned_user=warned_user,
                reason=reason if reason != None else "Reason not given by admin."
            )
            warning.save()

            if warned_user.warnings > 3:
                autoban = True
                warned_user.is_active = False
                files = File.objects.filter(user=warned_user)
                files.delete()
                ban = BannedUser(
                    banned_by=request.user,
                    banned_user=warned_user,
                    reason="You have exceeded 3 warnings by an administrator and have been auto-banned."
                )
                log.info(f"[WARN-USER] : USER: {warned_user.username} AUTO-BANNED DUE TO EXCEEDING 3 WARNINGS.")
                ban.save()
            warned_user.save()
            
            log.info(f"[WARN-USER] : USER: {warned_user.username} WARNED BY: {self.request.user.username}")
            return Response({'warned': True, 'autoban': autoban, 'warnings': warned_user.warnings}, status=status.HTTP_201_CREATED)
        else:
            log.warn(f"[WARN-USER] : FAILED TO WARN USER WITH ID: {warned_uid}, REQUESTED BY: {self.request.user.username}")
            return Response({'detail': 'The user you tried to warn does not exist.'}, status=status.HTTP_404_NOT_FOUND)


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
                log.warn(f"[FILE-UPLOAD] : BANNED USER: {upload_user.username} ATTEMPTED TO UPLOAD FILE.")
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

                log.info(f"[FILE-UPLOAD] : USER: {upload_user.username} UPLOADED FILE WITH ID: {uploaded_file.id} FROM IP: {uploaded_file.ip}")
                
                if settings.SUBDOMAIN:
                    uploaded_files.append(f"{htp}://{username}.{settings.DOMAIN_NAME}/{uploaded_file.generated_filename}")
                else:
                    uploaded_files.append(f"{htp}://{settings.DOMAIN_NAME}/u/{username}/{uploaded_file.generated_filename}")

            except Exception as e:
                
                log.warn(f"[FILE-UPLOAD] : USER: {upload_user.username} FAILED TO UPLOADED FILE WITH ID: {user_file} FROM IP: {uploaded_file.ip}")
                print(f"Upload for {user_file} failed")
                traceback.print_exc()
                uploaded_files.append(f"Failed to upload: {user_file}\n")

        return HttpResponse("\n".join(uploaded_files))

    def get(self, request):
        return redirect('/')
