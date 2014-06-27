from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns

import anylist.settings as settings
from anylist.views import *
from apps.models import *
from apps.views import *


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', MainPage.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<url>.*)register$', register),
    url(r'^(?P<url>.*)login/$', auth),
    url(r'^(?P<url>.*)logout/$', log_out),
    url(r'^search$', search),

    url(r'^profile/$', profile),
    url(r'^mylist/series/add$', add_list_serie),
    url(r'^mylist/series/del$', del_list_serie),
    url(r'^profile/list/(?P<category>\w+)/(?P<status>\w+)$', UserList.as_view()),

    url(r'^(?P<category>\w+)/add$', AddProduct.as_view()),
    url(r'^\w+/(?P<pk>\d+)-\w+/remove_from_list$', remove_from_list),
    url(r'^\w+/(?P<pk>\d+)-\w+/series/remove_from_list$', remove_from_list),
    url(r'^\w+/(?P<pk>\d+)-\w+/status$', status_update),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/$', ProductDetail.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/edit$', ProductionEdit.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/series/$', production_series_view),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/series/list$', seasons_view),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/series/add$', add_serie),
    url(r'^(?P<category>\w+)/$', ProductionList.as_view()),
    url(r'^(?P<category>\w+)/filter/(?P<args>(.+))/?$', ProductionChoiceView.as_view()),
    url(r'^\w+/series/edit$', edit_serie),
    url(r'^add_to_list$', add_list),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

urlpatterns += patterns('apps.views',
    url(r'^api/products$', ProductList.as_view(), name='product-list'),
    url(r'^api/status$', StatusList.as_view()),
    url(r'^api/genres$', GenreView.as_view()),
    url(r'^api/product:(?P<pk>\d+)/season:(?P<number>\d+)$', SeriesView.as_view(), name='series-list'),
    url(r'^api/product:(?P<pk>\d+)/seasons$', SeriesView.as_view(), name='seasons-list'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

if settings.DEBUG:

    if settings.MEDIA_ROOT:

        urlpatterns += static(settings.MEDIA_URL,

            document_root=settings.MEDIA_ROOT)

# Эта строка опциональна и будет добавлять url'ы только при DEBUG = True

urlpatterns += staticfiles_urlpatterns()
