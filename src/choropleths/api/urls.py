from django.conf.urls import url

from choropleths.api import views


urlpatterns = [
    url(r'^$', views.ChoroplethAPI.as_view({'get':'list', 'post': 'create'}), name='list-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.ChoroplethAPI.as_view({'get':'retrieve', 'put': 'update', 'delete': 'destroy'}), name='retrieve-update'),
    url(r'^palettes/(?P<pk>[0-9]+)/$', views.PaletteAPIView.as_view(), name='palette'),
]

