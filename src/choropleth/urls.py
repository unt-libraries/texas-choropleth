from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from choropleths.feeds import ChoroplethFeed


urlpatterns = patterns('',
    url(r'^', include('core.urls')),
    url(r'^datasets/', include('datasets.urls', namespace="datasets")),
    url(r'^choropleths/', include('choropleths.urls', namespace="choropleths")),
)

# Serve Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
