from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import viewsets, routers

import anylist.settings as settings
from anylist.views import *
from apps.models import *


class ProductViewSet(viewsets.ModelViewSet):
    model = Production
    fields = ('title',)


router = routers.DefaultRouter()
router.register(r'productions', ProductViewSet)

admin.autodiscover()

urlpatterns = patterns('',
#    url(r'^', include(router.urls)),
 #   url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', MainPage.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<url>.+)/register$', register),
    url(r'^(?P<url>.+)/login$', auth),
    url(r'^(?P<url>.+)/logout$', log_out),

    url(r'^profile/$', profile),
    url(r'^mylist/add$', add_list),
    url(r'^mylist/series/add$', add_list_serie),
    url(r'^profile/list/(?P<category>\w+)/(?P<status>\w+)$', UserList.as_view()),

    url(r'^anime/add/$', AddAnime.as_view()),
    url(r'^anime/add/1$', add_anime),
    url(r'^anime/$', AnimeListView.as_view()),
    url(r'^anime/(?P<pk>[\d]+)-(?P<name>\w+)$', AnimeDetail.as_view()),
    url(r'^anime/(?P<pk>[\d]+)-(?P<name>\w+)/edit$', AnimeEdit.as_view()),
    url(r'^anime/(?P<pk>[\d]+)-\w+/series', AnimeSeriesView.as_view()),
    url(r'^anime/series/add$', add_serie),
    url(r'^anime/series/edit$', edit_serie),

    url(r'^anime/filter/(.+)/?', AnimeChoiceView.as_view()),
    url(r'^manga/$', MangaListView.as_view()),
    url(r'^manga/add/?$', AddManga.as_view()),
    url(r'manga/add/1$', add_manga),
    url(r'^manga/(?P<pk>[\d]+)-\w+/?$', MangaDetailView.as_view()),
    url(r'^manga/(?P<pk>[\d]+)-\w+/series$', MangaSeriesView.as_view()),
    url(r'^manga/filter/(.+)/?', MangaChoiceView.as_view()),
    url(r'^manga/series/add$', add_manga_serie),
    url(r'^manga/volume/add$', add_manga_vol),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

if settings.DEBUG:

    if settings.MEDIA_ROOT:

        urlpatterns += static(settings.MEDIA_URL,

            document_root=settings.MEDIA_ROOT)

# Эта строка опциональна и будет добавлять url'ы только при DEBUG = True

urlpatterns += staticfiles_urlpatterns()

