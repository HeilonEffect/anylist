from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin

import anylist.settings as settings

from anylist.views import *
# from myapp.views import *


admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', start_page),
    url(r'^$', MainPage.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<url>.*)register/$', register),
    url(r'^(?P<url>.*)login/$', auth),
    url(r'^(?P<url>.*)logout/$', log_out),
    url(r'^search$', search),

    url(r'^profile/$', profile),
    url(r'^mylist/series/add$', add_list_serie),
    url(r'^mylist/series/del$', del_list_serie),
    url(r'^profile/list/(?P<category>\w+)/(?P<status>\w+)$', MyList.as_view()),

    url(r'^creator/add$', AddCreator.as_view()),
    url(r'^creator/(?P<pk>\d+)-\w+$', CreatorView.as_view()),
    url(r'^hero/(?P<pk>\d+)-\w+/$', HeroView.as_view()),
    url(r'^(?P<category>\w+)/add/$', AddProduct.as_view()),
# WTF ?!?
#    url(r'^\w+/(?P<pk>\d+)-\w+/remove_from_list$', remove_from_list),
#    url(r'^\w+/(?P<pk>\d+)-\w+/series/remove_from_list$', remove_from_list),
    url(r'^(?P<category>\w+)/$', ProductionList.as_view()),
    url(r'^\w+/(?P<pk>\d+)-\w+/status$', status_update),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/$', ProductDetail.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/edit$', ProductionEdit.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/series/$', SerieView.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/series/add$', add_serie),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/heroes/$', HeroesListView.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-(?P<name>\w+)/heroes/add$', AddHero.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/creators/$', CreatorsListView.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/creators/add$', AddCreator.as_view()),
    url(r'^(?P<category>\w+)/filter/(?P<args>(.+))/?$', ProductionChoiceView.as_view()),
    url(r'^\w+/series/edit$', edit_serie),

    # API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('myapp.urls')),
)


if settings.DEBUG:

    if settings.MEDIA_ROOT:

        urlpatterns += static(settings.MEDIA_URL,

            document_root=settings.MEDIA_ROOT)

# Эта строка опциональна и будет добавлять url'ы только при DEBUG = True

urlpatterns += staticfiles_urlpatterns()

handler404 = 'anylist.views.error404'
handler500 = 'anylist.views.error404'
