from django.conf.urls import url
from .views import DatasetManagementView, DatasetDetailView

urlpatterns = [
    url(r'^datasets/$', DatasetManagementView.as_view()),
    url(r'^datasets/(?P<pk>[0-9]+)/$', DatasetDetailView.as_view()),
    # url(r'^datasets/(?P<pk>[0-9]+)/edit/$', ),
]
