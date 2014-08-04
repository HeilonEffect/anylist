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
    url(r'^(?P<url>.*)register/$', register),
    url(r'^(?P<url>.*)logout/$', log_out),

    url(r'^profile/$', profile),
    url(r'^profile/list/(?P<category>\w+)/(?P<status>\w+)$', MyList.as_view()),

    url(r'^creator/add$', AddCreator.as_view()),
    url(r'^creator/(?P<pk>\d+)-\w+$', CreatorView.as_view()),
    url(r'^hero/(?P<pk>\d+)-\w+/$', HeroView.as_view()),
    url(r'^(?P<category>\w+)/add/$', add_product),
    url(r'^(?P<category>\w+)/$', product_list),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/$', ProductDetail.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/edit$', product_edit),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/series/$', serie_view),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/heroes/$', HeroesListView.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-(?P<name>\w+)/heroes/add$', AddHero.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/creators/$', CreatorsListView.as_view()),
    url(r'^(?P<category>\w+)/(?P<pk>\d+)-\w+/creators/add$', AddCreator.as_view()),
    url(r'^(?P<category>\w+)/filter/.+/?$', product_list),

    # API
    url(r'^api-token-auth/$', 'rest_framework.authtoken.views.obtain_auth_token'),
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
