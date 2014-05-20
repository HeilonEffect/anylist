from django.conf.urls import patterns, include, url
from anylist.views import MainPage, AddAnime, save_anime

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', MainPage.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^anime/add/?$', AddAnime.as_view()),
    url(r'^anime/add/genre/?$', save_anime),
    url(r'anime/add/\d', AddAnime.as_view()),
)
