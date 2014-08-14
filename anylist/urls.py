from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin

import anylist.settings as settings

from anylist.views import *
# from myapp.views import *


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', main_page),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^(?P<url>.*)register/$', register),

    # API
    url(r'^api-token-auth/$', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('myapp.urls')),

    url(r'^(?P<path>.*)[.]html$', partials),
)


if settings.DEBUG:

    if settings.MEDIA_ROOT:

        urlpatterns += static(settings.MEDIA_URL,

            document_root=settings.MEDIA_ROOT)

# Эта строка опциональна и будет добавлять url'ы только при DEBUG = True

urlpatterns += staticfiles_urlpatterns()
