from django.conf.urls import url, include
from django.contrib import admin
from .views import IndexView, AboutView, ToSView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='Index'),
    url(r'^about$', AboutView.as_view(), name='About'),
    url(r'^ToS$', ToSView.as_view(), name='ToS'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('backendAPI.urls')),
]
