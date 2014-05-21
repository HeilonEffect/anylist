from django.conf.urls import patterns, include, url
from anylist.views import MainPage, AddAnime

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', MainPage.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^anime/add/?$', AddAnime.as_view()),
    url(r'anime/add/\d', AddAnime.as_view()),
    url(r'^select2/', include('select2.urls')),
)
