from django.conf.urls import patterns, include, url
from anylist.views import MainView, JapView, AnimeView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', MainView.as_view()),
    url(r'^anime$', JapView.as_view()),
    url(r'^Anime/add$', AnimeView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
