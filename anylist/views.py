# -*- encoding: utf-8 -*-
import json
import re

from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView

from apps.models import *
from apps.forms import AddForm


class BasePageMixin(object):
	''' Содержит одинаковые для всех классов приложения операции '''
	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		context['header'] = self.header
		context['genres'] = Genre.objects.all()
		context['raiting'] = Raiting.objects.all()
		context['nav_groups'] = ThematicGroup.objects.all()
		return context


class DetailPageMixin(object):
	def get_context_data(self, **kwargs):
		context = super(DetailPageMixin, self).get_context_data(**kwargs)
		context['nav_groups'] = ThematicGroup.objects.all()
		return context


class ListPageMixin(object):
	def get_context_data(self, **kwargs):
		context = super(ListPageMixin, self).get_context_data(**kwargs)
		context['genre_groups'] = []
		context['nav_groups'] = ThematicGroup.objects.all()
		context['raiting'] = Raiting.objects.all()
		context['header'] = self.header
		
		# вычисляем, сколько раз встретился каждый жанр
		# на данной странице (фича аля яндекс.маркет)
		num_genres = {}
		for genre in Genre.objects.all():
			num_genres[genre.name] = 0
		
		for item in self.model.objects.all():
			genres = item.genres.all()
			for genre in genres:
				num_genres[genre.name] += 1
		
		# число жанров будет пересчитываться,
		# ибо содержимое страницы непостоянно в реальном времени
		# здесь мы добавляем
		for group in self.genre_groups:
			p = GenreGroup.objects.get(name=group)

			g = []
			for item in p.genres:
				g.append({'name': item, 'count': num_genres[item.name]})
			d = {'name': p.name, 'genres': g}
			context['genre_groups'].append(d)
		
		for item in context['raiting']:
			item.count = 0
			for val in self.model.objects.all():
				if val.old_limit == item:
					item.count += 1
		return context


class MainPage(BasePageMixin, ListView):
	model = ThematicGroup
	template_name = 'index.html'
	header = 'Welcome'

#------- views for anime ---------
class AnimeListView(ListPageMixin, ListView):
	template_name = 'list.html'
	model = Anime
	header = 'Список аниме'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Anime School', 'Standart', 'Anime Porn']


class AddAnime(BasePageMixin, CreateView):
	model = Anime
	form_class = AddForm
	template_name = 'forms/add_form.html'
	header = 'Добавление продукта'
	success_url = '/anime'


class AnimeDetail(DetailPageMixin, DetailView):
	template_name = 'detail.html'
	model = Anime

#----------views for manga------------
class MangaListView(ListPageMixin, ListView):
	template_name = 'list.html'
	model = Manga
	header = 'Список манги'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Anime School', 'Standart', 'Anime Porn']
#TODO - сделать миграцию