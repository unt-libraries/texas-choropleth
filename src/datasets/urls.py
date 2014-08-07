from django.conf.urls import url
from .views import DatasetManagement, DatasetDetail, DatasetCreate

urlpatterns = [
    url(r'^$', DatasetManagement.as_view(), name='dataset-management'),
    url(r'^(?P<pk>[0-9]+)/$', DatasetDetail.as_view(), name='dataset-detail'),
    url(r'^new/$', DatasetCreate.as_view(), name='dataset-create'),
    # url(r'^datasets/(?P<pk>[0-9]+)/edit/$', ),
]
