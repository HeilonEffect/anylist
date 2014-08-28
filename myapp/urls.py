from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns('myapp.views',
    url(r'profile$', UserStatistic.as_view()),
    url(r'categories/$', CategoriesList.as_view()), # test

    url(r'products$', ProductList.as_view()),
    url(r'products/id:(?P<pk>\d+)$', ProductDetail.as_view()),
    url(r'products/id:(?P<pk>\d+)/creators$', ProductCreator.as_view()),
    url(r'products/category:(?P<name>\w+)/$', ProductList.as_view()),
    url(r'products/category:(?P<name>\w+)/filter/(?P<args>.+)/$', ProductList.as_view()),

    url(r'seasons$', SeasonsView.as_view()),
    url(r'series$', SeriesView.as_view()),
    url(r'series/id:(?P<id>\d+)$', SingleSerieView.as_view()),
    url(r'raitings/$', RaitingList.as_view()),
    url(r'genres$', GenreGroupList.as_view()),
    url(r'userlist$', UserListView.as_view()),
    url(r'userlist/product:(?P<id>\d+)$', UserListUpdate.as_view()),
    url(r'serielist$', SerieListView.as_view()),
    url(r'serielist/serie:(?P<id>\d+)$', SingleSerieListView.as_view()),
    url(r'serielist/product:(?P<pk>\d+)/count$', SeriesCount.as_view()),

    url(r'search$', SearchView.as_view()),
    url(r'search_creator$', SearchCreatorView.as_view()),
    url(r'search_hero$', SearchHeroView.as_view()),

    url(r'creators$', CreatorView.as_view()),
    url(r'creators/id:(?P<pk>\d+)$', CreatorDetailView.as_view()),

    url(r'heroes$', HeroView.as_view()),
    url(r'heroes/id:(?P<pk>\d+)$', HeroDetailView.as_view()),

    url(r'employs$', EmployView.as_view()),
)