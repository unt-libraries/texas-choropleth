from django.conf.urls import url
from .views import DatasetManagement, DatasetDetail

urlpatterns = [
    url(r'^datasets/$', DatasetManagement.as_view(), name='dataset-management'),
    url(r'^datasets/(?P<pk>[0-9]+)/$', DatasetDetail.as_view(), name='dataset-detail'),
    # url(r'^datasets/(?P<pk>[0-9]+)/edit/$', ),
]
