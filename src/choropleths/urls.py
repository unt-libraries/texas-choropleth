from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', login_required(views.ChoroplethList.as_view()), name='choropleth-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ChoroplethDetail.as_view(), name='choropleth-detail'),
    url(r'^create/(?P<pk>[0-9]+)/$', login_required(views.ChoroplethCreate.as_view()), name='choropleth-create'),
    url(r'^(?P<pk>[0-9]+)/edit/$', login_required(views.ChoroplethEdit.as_view()), name='choropleth-edit'),
    url(r'^(?P<pk>[0-9]+)/view/$', views.ChoroplethView.as_view(), name='choropleth-view'),
    url(r'^(?P<pk>[0-9]+)/export/$', views.ChoroplethExport.as_view(), name='choropleth-export'),
    url(r'^api/$', views.ChoroplethAPI.as_view({'get':'list', 'post': 'create'}), name='api-create'),
    url(r'^api/(?P<pk>[0-9]+)/$', views.ChoroplethAPI.as_view({'get':'retrieve', 'put': 'update', 'delete': 'destroy'}), name='api-retrieve-update'),
    url(r'^api/palettes/(?P<pk>[0-9]+)/$', views.PaletteAPIView.as_view(), name='palette-api'),
]
