from django.conf.urls import patterns, include, url
from anylist.views import index

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index),
    url(r'^admin/', include(admin.site.urls)),
)
