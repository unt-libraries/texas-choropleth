from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.DatasetAPIView.as_view(), name='dataset'),
]
