from django.conf.urls import patterns, include, url
from anylist.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', MainPage.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^anime/add/?$', AddAnime.as_view()),
    url(r'anime/add/\d', AddAnime.as_view()),
    url(r'^anime$', AnimeListView.as_view()),
    url(r'^anime/(?P<pk>[\d]+)-\w+', AnimeDetail.as_view()),
    url(r'^manga$', MangaListView.as_view()),
)
