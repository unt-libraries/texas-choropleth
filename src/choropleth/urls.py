from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from core.views import HelpView, RegisterView
from choropleths.views import GalleryView
from choropleths.feeds import ChoroplethFeed
from cartograms.views import cartogram_csv_template

urlpatterns = patterns('',
    url(r'^$', GalleryView.as_view(), name="gallery"),
    url(r'^help/$', HelpView.as_view(), name="help"),
    url(r'^datasets/', include('datasets.urls', namespace="datasets")),
    url(r'^choropleths/', include('choropleths.urls', namespace="choropleths")),
    url(r'^cartogram-template/(?P<pk>[0-9]+)/$', cartogram_csv_template, name="csv-template"),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^feed/$', ChoroplethFeed()),
    # url(r'^register/$', CreateView.as_view(
    #     template_name='registration/register.html',
    #     form_class=UserCreationForm,
    #     success_url='/login'
    #     ), name='register'
    url(r'^register/$', RegisterView.as_view(), name='register'),
)

# Serve Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
