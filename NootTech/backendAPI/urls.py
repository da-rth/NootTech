from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.conf.urls import url
from .views import *

# TODO : api/make-private/<id> - sets file.is_private = True
# TODO : api/make-public/<id> - sets file.is_private = False
# TODO : api/warnings - so that user can view list of warnings

# TODO REVAMP : api/warning so that admin must POST a "reason" for warning
# TODO REVAMP : api/ban so that admin must POST a "reason" for warning

# TODO : Clean up code, add comments to views.py

urlpatterns = format_suffix_patterns([
    url(r'^token/auth', obtain_jwt_token),
    url(r'^token/refresh', refresh_jwt_token),
    url(r'^token/verify', verify_jwt_token),
    url(r'^create-user', CreateUserAPIView.as_view(), name='CreateUser'),

    url(r'^settings', GetSetSettingsAPIView.as_view(), name='GetSetSettings'),
    url(r'^upload', UploadView.as_view(), name='Upload'),
    url(r'^files', ListFilesAPIView.as_view(), name='ListFiles'),
    url(r'^file/delete/(?P<pk>\d+)', DeleteFileAPIView.as_view(), name='DeleteFile'),

    url(r'^favourites', ListFavouritesAPIView.as_view(), name='ListFavourites'),
    url(r'^favourite/add/(?P<pk>\d+)', AddFavouriteAPIView.as_view(), name='AddFavourite'),
    url(r'^favourite/delete/(?P<pk>\d+)', DeleteFavouriteAPIView.as_view(), name='DeleteFavourite'),

    url(r'^report-file', ReportAddAPIView.as_view(), name='ReportAdd'),
    url(r'^reports', ReportListAPIView.as_view(), name='ReportList'),

    url(r'^ban/(?P<pk>\w+)', BanViewSet.as_view({'get': 'field', }), name='Ban'),
    url(r'^warn/(?P<pk>\w+)', WarnViewSet.as_view({'get': 'field', }), name='Warn'),

    url(r'^users/(?P<username>\w+)/(?P<gen_name>\w+)', SubdomainViewSet.as_view({'get': 'field', }), name='Sub'),
    url(r'^error-videos', ErrorVideoAPIView.as_view(), name='ErrorVideos'),
])

