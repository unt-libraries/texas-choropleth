from django.conf.urls import patterns, include, url

from core import views as core_views
from cartograms.views import cartogram_csv_template


urlpatterns = patterns('',
    url(r'^$', core_views.GalleryView.as_view(), name="gallery"),
    url(r'^help/$', core_views.HelpView.as_view(), name="help"),
    url(r'^cartogram-template/(?P<pk>[0-9]+)/$', cartogram_csv_template, name="csv-template"),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),
    url(r'^register/$', core_views.RegisterView.as_view(), name='register'),
    url(r'^reset/', include('password_reset.urls')),
)
