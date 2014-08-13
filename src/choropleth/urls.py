from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from datasets.views import IndexView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'choropleth.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', IndexView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^datasets/', include('datasets.urls', namespace="datasets")),
    url(r'^choropleths/', include('choropleths.urls', namespace="choropleths")),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)
