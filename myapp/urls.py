from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns('myapp.views',
	url(r'user', User.as_view()),
	url(r'categories/$', CategoriesList.as_view()),
	url(r'products$', ProductList.as_view()),
	url(r'products/id:(?P<pk>\d+)$', ProductDetail.as_view()),
	url(r'products/category:(?P<name>\w+)/$', ProductList.as_view()),
	url(r'products/category:(?P<name>\w+)/filter/(?P<args>.+)/$', ProductList.as_view()),
	url(r'raitings/$', RaitingList.as_view()),
	url(r'genres/category:(?P<name>\w+)$', GenreGroupList.as_view()),
)