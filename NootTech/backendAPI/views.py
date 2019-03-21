from .utils import get_upload_key, upload_authentication_failure, get_ip, get_id_gen, get_ext
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from . import serializers
from .models import *
import traceback
import logging
from datetime import datetime
log = logging.getLogger(__name__)

htp = "https" if settings.HTTPS else "http"

from django.views.generic import View
from django.shortcuts import render
from django.conf import settings




class IndexView(View):
    
    def get(self, request, *args):

        """
        This view renders the Vue.JS javascript - which loads the main website application.
        However, it also checks if the current URL is a sharelink. If so, it will add a QueryDict 'file' to the context
        Which is used by index.html template to generate some fancy html meta information - allowing for URL embeds on platforms such as Discord, Twitter etc...
        """

        context = dict()
        context["debug"] = settings.DEBUG
        context["subdomain"] = False
        # Check if URL is a dubdomaon or a sharelink (has /u/ in url)
        subdomain = request.META['HTTP_HOST'].replace((settings.DOMAIN_NAME), "")[:-1]
        sharelink = '/u/' in request.build_absolute_uri()
        url = request.build_absolute_uri()
        
        context["url"] = ('https://' if settings.HTTPS else 'http://') + settings.DOMAIN_NAME+settings.MEDIA_URL
        
        try:
            # If the current URL is a sharelink for an existing file, add file info to context dict
            if subdomain:
                username = url.split("//")[0].split(".")[0]
                genid = url.split("/")[-1]
                u = User.objects.get(username=username)
                f = File.objects.get(generated_filename=genid, user=u)
                context["file"] = f
            
            elif sharelink:
                username = url.split("/u/")[1].split("/")[0]
                genid = url.split("/")[-1]
                u = User.objects.get(username=username)
                f = File.objects.get(generated_filename=genid, user=u)
                context["file"] = f
        except (User.DoesNotExist, File.DoesNotExist) as e:
            # If file or user doesn't exist, just ignore.
            pass
        
        return render(request, 'index.html', context=context)


class ErrorVideoAPIView(generics.ListAPIView):
    """
    Returns a list of videos used (randomly) at website 404 page.
    The video is automatically played when the user visits or gets redirected to /404
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.ErrorVideoSerializer
    queryset = ErrorVideo.objects.all()

class DeleteAccountAPIView(generics.CreateAPIView):
    """
    View for /api/delete-account
    Requires a confirmation_password to be POSTed to view in order to confirm account deletion
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DeleteAccountSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        u = User.objects.get(id=self.request.user.id)
        password = request.data.get('confirmation_password', None)

        if password:
            # If confirmation password matches user's current password, proceed with account deletion
            current_password = request.user.password
            match = check_password(password, current_password)
            if match:
                user = User.objects.get(id=request.user.id)
                files = File.objects.filter(user=user)
                files.delete()
                user.delete()

                log.info(f"[ACCOUNT-DELETED] : USER: {user.username} DELETED ACCOUNT.")

                return Response({'detail': 'Account successfully deleted'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Account could not be deleted. Is password confirmation correct?'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Password confirmation is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        u.save()

class ChangePasswordAPIView(generics.CreateAPIView):
    """
    View for /api/change-password
    Changes the user's password, given the old_password and new_password
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):

        u = User.objects.get(id=self.request.user.id)
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)

        # If old and new passwords were recieved in POST request...
        if old_password and new_password:

            current_password = request.user.password
            match = check_password(old_password, current_password)
            # If old_password matches current user's password, proceed with password change
            if match:
                try: 
                    validate_password(new_password)
                    user = User.objects.get(id=request.user.id)
                    user.set_password(new_password)
                    user.save()
                    log.info(f"[PASSWORD-CHANGED] : USER: {user.username} CHANGED THEIR PASSWORD.")
                    return Response({'detail': 'Password successfully changed'}, status=status.HTTP_200_OK)
                except ValidationError as e:
                    return Response({'detail': e.messages}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'The old password was not correct.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'old_password and new_password is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        u.save()



class ListFilesAPIView(generics.ListAPIView):
    """
    Returns a list of files belonging to an Authenticated user, ordered by most recently uploaded.
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

    def create(self, request, *args, **kwargs):
        # Override the perform_create method to UPDATE a user instead of CREATE one.
        # Get the object for the current authenticated user (logged in)
        u = User.objects.get(id=self.request.user.id)

        # If the variables colour, email or upload_key have been recieved via POST request
        # Update user object with these values...
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = dict()

        if serializer.validated_data.get('colour'):
            # if "colour" exists and isn't an empty string
            u.colour = serializer.validated_data.get('colour')
            response["colour"] = u.colour
        
        if serializer.validated_data.get('email'):
            # If "email" exists and isn't an empty string
            u.email = serializer.validated_data.get('email')
            response["email"] = u.email
        
        if serializer.validated_data.get('gen_upload_key'):
            # If "upload_key" exists and is set to True
            u.upload_key = get_upload_key()
            response["upload_key"] = u.upload_key
        if response:
            u.save()
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid parameters. Try `colour`, `email`, etc...'}, status=status.HTTP_400_BAD_REQUEST)


class CreateUserAPIView(generics.ListCreateAPIView):
    '''
        This API will Take in  POST request of user informations and create a new User.
    '''
    permission_classes = (AllowAny,)
    serializer_class = serializers.CreateUserSerializer
    queryset = User.objects.all()


class ListFavouritesAPIView(generics.ListCreateAPIView):
    '''
        This API Will POST the files favourite by a user, Create new favourites, delete already favourite files
        Needs tweeking, need model to be created
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SerializeFavouritesList

    def get_queryset(self):
        return FavouritedFile.objects.filter(user=self.request.user).order_by('-date')

class UpdateFileAPIView(generics.UpdateAPIView):
    '''
        This API will update a file, such as deleting the file, toggling it as private, generating a new file_id or renaming it.
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateFileSerializer

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)
    
    def update(self, request, pk):
        try:
            # Check if file exists
            file = File.objects.get(user=self.request.user, id=pk)
            response = dict()

            # Get request information
            toggle_private = request.data.get("toggle_private", None)
            gen_new_id = request.data.get("gen_new_id", None)
            original_filename = request.data.get("original_filename", None)
            delete = request.data.get("delete", None)
            
            # If any of the above fields are provided... execute their action
            if delete:
                file.delete()
                log.info(f"[FILE-DELETED] : USER: {self.request.user.username} DELETED FILE WITH ID {pk}")
                return Response({'detail': "File successfully deleted!"}, status=status.HTTP_200_OK)
            
            if toggle_private:
                file.is_private = not file.is_private
                log.info(f"[FILE-PRIVACY] : USER: {self.request.user.username} TOGGLED PRIVACY FOR FILE WITH ID {pk}")
                response["is_private"] = file.is_private
            
            if gen_new_id:
                file.generated_filename = utils.get_id_gen()
                log.info(f"[FILE-GEN-NAME] : USER: {self.request.user.username} GENERATED NEW UNIQUE ID FOR FILE WITH ID {pk}")
                response["generated_filename"] = file.generated_filename
            
            if original_filename:
                old = file.original_filename
                file.original_filename = original_filename
                log.info(f"[FILENAME-CHANGE] : USER: {self.request.user.username} CHANGED FILENAME FROM `{old}` TO `{original_filename}` FOR FILE WITH ID: {pk}")
                response["original_filename"] = original_filename
            
            # If ANY action was executed, save the file
            if response:
                file.save() # ignored for deleted files
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'detail': f'The file with id {pk} uploaded by {self.request.user.username} could not be updated with provided information.'}, status=status.HTTP_400_BAD_REQUEST)

        except File.DoesNotExist:
            return Response({'detail':f'The file with id {pk} uploaded by {self.request.user.username} could not be found.'}, status=status.HTTP_404_NOT_FOUND)


class AddFavouriteAPIView(generics.CreateAPIView):
    '''
    This API adds a file to a user's list of favourites, given the FILE ID as a parameter.
    This creates a new FavouritedFile object which is saved to the database.
    User must be authenticated.
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AddFavSerializer

    def get_queryset(self):
        return FavouritedFile.objects.filter(user=self.request.user)
    
    def create(self, request, pk):
        try:
            # Check if file exists
            f = File.objects.get(id=pk)

            # Check if user has already favourited file
            try:
                fav_exists = FavouritedFile.objects.get(file=f, user=request.user)
            except FavouritedFile.DoesNotExist:
                fav_exists = False
            
            if fav_exists:
                return Response({'detail': 'Favourite already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            fav = FavouritedFile(
                user=request.user,
                file=f
            )

            fav.save()
            return Response({'detail': 'Favourite successfully added.'}, status=status.HTTP_200_OK)
        except File.DoesNotExist:
            return Response({'detail': 'Could not add favourite for file. File may not exist or may already be favourited.'}, status=status.HTTP_404_NOT_FOUND)

class DeleteFavouriteAPIView(generics.DestroyAPIView):
    '''
    This API deletes a favourite from a user's list of favourites, given the FAVOURITE_ID.
    User must be authenticated.
    '''
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return FavouritedFile.objects.filter(user=self.request.user)


class ReportListAPIView(generics.ListAPIView):
    '''
    This API lists all reports submitted by users.
    It is accessable for Administrators only
    '''
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.ReportList
    queryset = ReportedFile.objects.all()


class ReportAddAPIView(generics.CreateAPIView):
    '''
    This API allows users to submit a new file report.
    '''
    permission_classes = (AllowAny,)
    serializer_class = serializers.ReportAdd
    queryset = ReportedFile.objects.all()

class WarningListAPIView(generics.ListAPIView):
    '''
    This API allows authenticated users to view a list of all their warnings.
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.WarningList

    def get_queryset(self):
        return Warned.objects.filter(warned_user=self.request.user)

class SubdomainViewSet(viewsets.ViewSet):
    '''
    This API returns file information for a sharelink, given a username and generated filename.
    Anyone can view sharelinks, hence this is AllowAny.
    '''
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
    '''
        Allows an administrator to ban a user. Banned user will recieve an email notifying them.
    '''
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.BanAdd
    queryset = BannedUser.objects.all()

    def create(self, request, *args, **kwargs):

        reason = request.data.get('reason', "Not given by admin")
        ban_uid = request.data.get('warned_user', None)
        ban_user = User.objects.get(id=ban_uid)

        if ban_user:
            # Checks if user is staff/admin
            if ban_user.is_staff or ban_user.is_superuser:
                log.warn(f"[BAN-USER] : USER: {request.user.username} TRIED TO BAN STAFF MEMBER {ban_user.username}.")
                return Response({'detail':'You cannot ban another staff member.'}, status=status.HTTP_400_BAD_REQUEST)
            
            ban_user.is_active = False
            # File deletion at discretion of administrator through admin panel.
            #files = File.objects.filter(user=ban_user)
            #files.delete()
            ban_user.save()
            # Ban the user
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
    '''
        Allows an administrator to warn a user. Banned user will recieve an email notifying them.
    '''
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.WarningAdd
    queryset = Warned.objects.all()

    def create(self, request, *args, **kwargs):
        
        autoban = False
        reason = request.data.get('reason', "Not given by administrator.")
        warned_uid = request.data.get('warned_user', None)
        warned_user = User.objects.get(id=warned_uid)

        if warned_user:
            
            if warned_user.is_staff or warned_user.is_superuser:
                log.warn(f"[WARN-USER] : USER: {request.user.username} TRIED TO WARN STAFF MEMBER {warned_user.username}.")
                return Response({'detail': 'You cannot warn another staff member.'}, status=status.HTTP_403_FORBIDDEN)
            # Warn the user and create a new warning reference.
            warned_user.warnings += 1
            
            warning = Warned(
                warned_by=User.objects.get(id=self.request.user.id),
                warned_user=warned_user,
                reason=reason if reason != None else "Reason not given by admin."
            )
            warning.save()

            # Auto-ban the user if their warnings are above 3.
            if warned_user.warnings > 3:
                autoban = True
                warned_user.is_active = False
                # File deletion at discretion of administrator through admin panel.
                #files = File.objects.filter(user=warned_user)
                #files.delete()
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
    '''
    Allows users to upload files both on and off-site using an Upload Key as means of proving authentication.
    A user must provide username, upload_key , is_private and content fields, where content points to a file or list of files.
    
    CSRF_EXEMPT required to ensure users not currently on website are able to sent requests to /api/upload
    '''
    @csrf_exempt
    def post(self, request):

        uploaded_files = []

        if request.user.is_authenticated:
            upload_user = User.objects.get(id=request.user.id)
            username = upload_user.username
        else:
            # Check if user hasn't provided enough fields for upload
            invalid_field_message = upload_authentication_failure(request, User)
            if invalid_field_message:
                return invalid_field_message
            
            # Identify the User
            username = request.POST["username"]
            upload_user = get_object_or_404(User, username=username, upload_key=request.POST["upload_key"])

            # Stop user from uploading if they are banned.
            if not upload_user.is_active:
                log.warn(f"[FILE-UPLOAD] : BANNED USER: {upload_user.username} ATTEMPTED TO UPLOAD FILE.")
                return HttpResponse(f"Your account is no longer active.\n"
                                    f"If you think this is a mistake, "
                                    f"please visit: {htp}://{settings.DOMAIN_NAME}/contact")
        
        # Set private status of file if provided.
        is_private = request.POST.get("is_private", False) == "true"
        ip = get_ip(request)

        for user_file in request.FILES.getlist('content'):

            try:
                # Get ext and genrate a unique file id
                ext = get_ext(user_file.name)
                id_gen = get_id_gen()

                # Check if file is an image or video, if so then also generate a thumbnail image.
                exts = [".gif", ".jpg", ".jpeg", ".png", ".mp4", ".webm", ".ogv", ".ico", ".apng", ".bmp"]

                uploaded_file = File(
                    user=upload_user,
                    generated_filename=id_gen,
                    ip=ip,
                    file_content=user_file,
                    file_thumbnail=user_file if ext in exts else None,
                    is_private=is_private
                )
                
                uploaded_file.save()

                # Log the user upload
                log.info(f"[FILE-UPLOAD] : USER: {upload_user.username} UPLOADED FILE WITH ID: {uploaded_file.id} FROM IP: {uploaded_file.ip}")
                
                # Return correctly formatted sharelink depending if settings.SUBDOMAIN is enabled.
                if settings.SUBDOMAIN:
                    uploaded_files.append(f"{htp}://{username}.{settings.DOMAIN_NAME}/{uploaded_file.generated_filename}")
                else:
                    uploaded_files.append(f"{htp}://{settings.DOMAIN_NAME}/u/{username}/{uploaded_file.generated_filename}")

            except Exception as e:
                # If upload fails, log information.
                log.warn(f"[FILE-UPLOAD] : USER: {upload_user.username} FAILED TO UPLOADED FILE WITH ID: {user_file} FROM IP: {uploaded_file.ip}")
                traceback.print_exc()

                print(f"Upload for {user_file} failed")
                # Add message to list of uploads or simply return with bad request 400
                if len(uploaded_files) == 0:
                    return HttpResponse("Failed to upload file - issue saving it to server.", status=400)
                else:
                    uploaded_files.append(f"Failed to upload: {user_file}\n")

        return HttpResponse("\n".join(uploaded_files), status=200)

    def get(self, request):
        return redirect('/')
