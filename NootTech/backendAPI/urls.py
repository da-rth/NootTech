from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.conf.urls import url
from .views import *

urlpatterns = format_suffix_patterns([
    # POST login credentials {username, password} in /api/token/auth. Returns a JWT which gets saved to local user storage for authenticated API requests. Returns JWT token.
    url(r'^token/auth', obtain_jwt_token),
    
    # POST with no body data but JWT {token} in header for authorisation. Returns a new 'refreshed' JWT token with new expiry date. Returns new token(s).
    url(r'^token/refresh', refresh_jwt_token),
    
    # POST with no body data but JWT {token} in header for authorisation. Verifies if the current token is expired or still valid. Returns validity status. 
    url(r'^token/verify', verify_jwt_token),
    
    # POST account credentials {username, email, password, colour}. If credentials are validated, return successful status. Frontend then posts to /api/token/auth to log user in.
    url(r'^create-user', CreateUserAPIView.as_view(), name='CreateUser'),

     # POST with {password_confirmation}. If credentials are validated, return successful status and delete account and all files.
    url(r'^delete-account', DeleteAccountAPIView.as_view(), name='DeleteUser'),
    
    # POST account credentials {old_password, new_password}. If credentials are validated, return change user password to new_password.
    url(r'^change-password', ChangePasswordAPIView.as_view(), name='ChangeUserPassword'),
    
    # GET to get JSON object representing user settings of currently authenticated user. If not authenticated, forbidden. Or POST new settings along with JWT In header to authenticate. Update settings. 
    url(r'^settings', GetSetSettingsAPIView.as_view(), name='GetSetSettings'),
    
    # POST file upload information {username, upload_key, content[]="path/to/file(S)"}. If user is verified, process file upload and respond with file URL. Else, respond with helpful error message explaining upload failure.
    url(r'^upload', UploadView.as_view(), name='Upload'),

    # GET list of files uploaded by currently authenticated user (through verifying JWT Header). If no files, return empty array. If not verified, respond with forbidden.
    url(r'^files', ListFilesAPIView.as_view(), name='ListFiles'),

    # POST to below url where <pk> is the ID of the file to be renamed. If file exists, delete it and respond with success. Else, respond with 404.
    url(r'^file/(?P<pk>\d+)', UpdateFileAPIView.as_view(), name='RenameFile'),

    # GET a list of all files favourited by the currently authenticated user (again, verified through JWT token in header). If no favourites, return empty array. If not authenticated, respond with forbidden.
    url(r'^favourites', ListFavouritesAPIView.as_view(), name='ListFavourites'),

    # POST to below url where <pk> is the ID of the file to be added as a favourite. If file exists, mark it as a favourite. Else, respond with 404 not found.
    url(r'^favourite/add/(?P<pk>\d+)', AddFavouriteAPIView.as_view(), name='AddFavourite'),
    
    # POST to below url where <pk> is the ID of the file to be deleted from list of favourites. If file exists and is favourited by user, remove it from favourites. Else, respond with 404 not found.
    url(r'^favourite/delete/(?P<pk>\d+)', DeleteFavouriteAPIView.as_view(), name='DeleteFavourite'),
    
    # POST report information {reportee_user, reported_file, report_reason, report_body} and process report accordingly. Respond with success if all keys (reported_file, reportee_user etc...) exist.
    url(r'^report-file', ReportAddAPIView.as_view(), name='ReportAdd'),

    # GET a list of reports as an array (AdminOnly - verified by JWT). If no reports are present, return empty array. If not authorized, respond with unauthorised.
    url(r'^reports', ReportListAPIView.as_view(), name='ReportList'),
    
    # POST information regarding banning a user {user_id, reason} (AdminOnly - verified by JWT), process ban and respond with success and message. If not authorized, respond with unauthorised.
    url(r'^ban', BanAPIView.as_view(), name='Ban'),

    # GET a list of warnings belonging to the currently authenticated user. If not authenticated, respond with bad request.
    url(r'^warnings', WarningListAPIView.as_view(), name='WarningList'),
    
    # POST a warning (AdminOnly), {user_id, reason}, process the warning. If user has too many warnings, they will be autobanned. Respond with success info (such as if auto-banned). If not admin, respond with unauthorized.
    url(r'^warn', WarnAPIView.as_view(), name='Warn'),

    # GET data for a share link, given a username and gen_name for a file. If the file exists, respond with file information. Else, respond with bad request.
    url(r'^sharelink/(?P<username>\w+)/(?P<gen_name>\w+)', SubdomainViewSet.as_view({'get': 'field', }), name='Sub'),
    
    # GET a list of error videos - no authentication required.
    url(r'^error-videos', ErrorVideoAPIView.as_view(), name='ErrorVideos'),
])

