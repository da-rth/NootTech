from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.conf.urls import url
from .views import ListUsers, ErrorVideoView, SettingsView, ListFilesView , CreateUserView

# user API requests
# TODO: api/create-user - POST user info (email, username, password, colour) and CREATE new user with it
# TODO: api/file        - POST a uploader id and generated_filename (of a file) and respond with the file's info
# TODO: apo/reports     - GET list of reports; POST
# TODO: api/favourites  - GET list of Favourites (files); POST create new Favourite; DELETE file from Favourites
# TODO: api/report      - POST a report of offending user id, file id, reportee id, title, reason
# TODO: validation for api/settings/ POST request

# isAdminUser API requests
# TODO: api/ban         - POST the id user to ban, admin id, title, reason. Set active status to False, delete all files
# TODO: api/warn        - POST the id user to warn, admin id, title, reason. Increment user.warnings by 1. If > 3, BAN!!


"""
COMPLETE APIs
# Authentication
- api/token/auth
- api/token/refresh
- api/token/verify

# Other
-api/files/ - Display Files belonging to a user
- api/error-videos/ - GET a list of error videos
- api/settings/ - GET an authenticated user's settings and POST changes to settings (if request.user is authenticated)
"""

urlpatterns = format_suffix_patterns([
    url(r'^token/auth', obtain_jwt_token),
    url(r'^token/refresh', refresh_jwt_token),
    url(r'^token/verify', verify_jwt_token),
    url(r'^list-users', ListUsers.as_view(), name='TestView'),
    url(r'^error-videos', ErrorVideoView.as_view(), name='get_error_videos'),
    url(r'^settings', SettingsView.as_view(), name='get_post_settings'),
    url(r'^files', ListFilesView.as_view(), name='list-files'),
    url(r'^create-user', CreateUserView.as_view(), name='list-files'),

])

