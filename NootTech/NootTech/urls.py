from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import sys

sys.path.append(".")

from backendAPI.views import IndexView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('backendAPI.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^(.*?)$', IndexView.as_view(), name='IndexPage'),
]
