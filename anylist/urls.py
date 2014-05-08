from django.conf.urls import patterns, include, url
from anylist.views import index, CatalogView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', CatalogView.as_view()),
    url(r'^anime$', CatalogView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
