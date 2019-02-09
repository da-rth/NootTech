from django.conf.urls import url
from .views import ListUsers

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = format_suffix_patterns([
    url(r'^token/auth', obtain_jwt_token),
    url(r'^token/refresh', refresh_jwt_token),
    url(r'^token/verify', verify_jwt_token),
    url(r'^list-users', ListUsers.as_view(), name='TestView'),
])