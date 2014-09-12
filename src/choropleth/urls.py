from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from choropleths.views import GalleryView
from cartograms.views import cartogram_csv_template

urlpatterns = patterns('',
    url(r'^$', GalleryView.as_view(), name="gallery"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^datasets/', include('datasets.urls', namespace="datasets")),
    url(r'^choropleths/', include('choropleths.urls', namespace="choropleths")),
    url(r'^cartogram-template/(?P<pk>[0-9]+)/$', cartogram_csv_template, name="csv-template"),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)

# Serve Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
