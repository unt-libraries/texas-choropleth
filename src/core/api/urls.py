from django.conf.urls import url, include


urlpatterns = [
    url(r'^choropleths/', include('choropleths.api.urls', namespace="choropleths")),
    url(r'^datasets/', include('datasets.api.urls', namespace="datasets")),
]
