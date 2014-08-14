from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ChoroplethList.as_view(), name='choropleth-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ChoroplethDetail.as_view(), name='choropleth-detail'),
    url(r'^create/(?P<pk>[0-9]+)/$', views.ChoroplethCreate.as_view(), name='choropleth-create'),
    url(r'^(?P<pk>[0-9]+)/view/$', views.ChoroplethView.as_view(), name='choropleth-view'),
    url(r'^api/(?P<pk>[0-9]+)/$', views.ChoroplethAPIView.as_view(), name='api-view'),
    url(r'^api/$', views.ChoroplethAPI.as_view({'get':'list', 'post': 'create', }), name='api-create'),
    url(r'^api/palettes/(?P<pk>[0-9]+)/$', views.PaletteAPIView.as_view(), name='palette-api'),
]
