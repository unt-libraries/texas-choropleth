from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from core import views as core_views
from choropleths.views import GalleryView
from choropleths.feeds import ChoroplethFeed
from cartograms.views import cartogram_csv_template

urlpatterns = patterns('',
    url(r'^$', GalleryView.as_view(), name="gallery"),
    url(r'^help/$', core_views.HelpView.as_view(), name="help"),
    url(r'^datasets/', include('datasets.urls', namespace="datasets")),
    url(r'^choropleths/', include('choropleths.urls', namespace="choropleths")),
    url(r'^cartogram-template/(?P<pk>[0-9]+)/$', cartogram_csv_template, name="csv-template"),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),
    url(r'^feed/$', ChoroplethFeed()),
    url(r'^register/$', core_views.RegisterView.as_view(), name='register'),
    url(r'^reset/', include('password_reset.urls')),
)

# Serve Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
