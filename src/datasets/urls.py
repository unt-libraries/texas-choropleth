from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^$',login_required(views.DatasetManagement.as_view()), name='dataset-management'),
    url(r'^(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view(), name='dataset-detail'),
    url(r'^new/$', login_required(views.DatasetCreate.as_view()), name='dataset-create'),
    url(r'^(?P<pk>[0-9]+)/update/$', login_required(views.DatasetUpdate.as_view()), name='dataset-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', login_required(views.DatasetDelete.as_view()), name='dataset-delete'),
    url(r'^(?P<pk>[0-9]+)/export/$', login_required(views.export_dataset), name='dataset-export'),
]
