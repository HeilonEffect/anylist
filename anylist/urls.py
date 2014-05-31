from django.conf.urls import patterns, include, url
from anylist.views import *

from django.contrib import admin

import anylist.settings as settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', MainPage.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^anime/add/?$', AddAnime.as_view()),
    url(r'anime/add/\d', AddAnime.as_view()),
    url(r'^anime/?$', AnimeListView.as_view()),
    url(r'^anime/(?P<pk>[\d]+)-\w+/?$', AnimeDetail.as_view()),
    url(r'^anime/(?P<pk>[\d]+)-\w+/series', AnimeSeriesView.as_view()),
    url(r'^anime/series/add$', anime_series),
    url(r'^anime/season/add$', add_season),


    url(r'^anime/filter/(.+)/?', AnimeChoiceView.as_view()),
    url(r'^manga/?$', MangaListView.as_view()),
    url(r'^manga/add/?$', AddManga.as_view()),
    url(r'^manga/(?P<pk>[\d]+)-\w+', MangaDetailView.as_view()),
    url(r'^manga/filter/(.+)/?', MangaChoiceView.as_view()),
)
