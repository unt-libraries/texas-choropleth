from django.conf.urls import patterns, include, url

from cartograms.views import cartogram_csv_template
from core import views


urlpatterns = patterns('',
    url(r'^$', views.GalleryView.as_view(), name="gallery"),
    url(r'^about/$', views.AboutView.as_view(), name="about"),
    url(r'^help/$', views.HelpView.as_view(), name="help"),
    url(r'^cartogram-template/(?P<pk>[0-9]+)/$', cartogram_csv_template, name="csv-template"),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),
    # url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^reset/', include('password_reset.urls')),
    url(r'^reset/recover', views.RecoverInvalid.as_view(), name='password_reset_recover'),
    url(r'^api/', include('core.api.urls', namespace="api")),
)
