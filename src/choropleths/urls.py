from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from . import feeds


urlpatterns = [
    url(r'^$', login_required(views.ChoroplethList.as_view()), name='choropleth-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ChoroplethDetail.as_view(), name='choropleth-detail'),
    url(r'^create/(?P<pk>[0-9]+)/$', login_required(views.ChoroplethCreate.as_view()), name='choropleth-create'),
    url(r'^(?P<pk>[0-9]+)/edit/$', login_required(views.ChoroplethEdit.as_view()), name='choropleth-edit'),
    url(r'^(?P<pk>[0-9]+)/view/$', views.ChoroplethView.as_view(), name='choropleth-view'),
    url(r'^(?P<pk>[0-9]+)/export/$', views.ChoroplethExport.as_view(), name='choropleth-export'),
    url(r'^feed/$', feeds.ChoroplethFeed()),
]
