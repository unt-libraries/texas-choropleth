from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import DatasetManagement, DatasetDetail, DatasetCreate, DatasetAPIView, DatasetUpdate, DatasetDelete, export_dataset

urlpatterns = [
    url(r'^$',login_required(DatasetManagement.as_view()), name='dataset-management'),
    url(r'^(?P<pk>[0-9]+)/$', DatasetDetail.as_view(), name='dataset-detail'),
    url(r'^new/$', login_required(DatasetCreate.as_view()), name='dataset-create'),
    url(r'^(?P<pk>[0-9]+)/update/$', login_required(DatasetUpdate.as_view()), name='dataset-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', login_required(DatasetDelete.as_view()), name='dataset-delete'),
    url(r'^(?P<pk>[0-9]+)/export/$', login_required(export_dataset), name='dataset-export'),
    url(r'^api/(?P<pk>[0-9]+)/$', DatasetAPIView.as_view(), name='dataset-api'),
]
