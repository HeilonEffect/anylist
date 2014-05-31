# -*- encoding: utf-8 -*-
import json
import re

from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.cache import cache
from django.db.models import F, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView

from braces.views import FormValidMessageMixin

from apps.models import *
from apps.forms import *


class BasePageMixin(object):
	''' Содержит одинаковые для всех классов приложения операции '''
	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		context['header'] = self.header
		context['genres'] = Genre.objects.all()
		context['raiting'] = Raiting.objects.all()
		context['nav_groups'] = ThematicGroup.objects.all()
		try:
			context['category'] = Category.objects.get(name=self.category)
		except AttributeError as e:
			print('Category is not defined')
		return context


class DetailPageMixin(object):
	def get_context_data(self, **kwargs):
		context = super(DetailPageMixin, self).get_context_data(**kwargs)
		context['nav_groups'] = ThematicGroup.objects.all()
		context['category'] = Category.objects.get(name=self.category)
		context['url'] = self.model.objects.get(
			id=self.kwargs['pk']).get_absolute_url()
		return context


class ChildDetailPageMixin(object):
	def get_queryset(self):
		return self.model.objects.filter(link__id=self.kwargs['pk'])
	
	def get_context_data(self, **kwargs):
		context = super(ChildDetailPageMixin, self).get_context_data(**kwargs)
		context['nav_groups'] = ThematicGroup.objects.all()
		context['category'] = Category.objects.get(name=self.category)
		context['num_season'] = self.get_queryset().count()
		
		context['url'] = self.parent_model.objects.get(
			id=self.kwargs['pk']).get_absolute_url()
		return context


class ListPageMixin(object):
	def get_queryset(self):
		if not self.queryset:
			self.queryset = self.model.objects.all()
			return self.queryset
		else:
			return self.queryset

	def get_context_data(self, **kwargs):
		context = super(ListPageMixin, self).get_context_data(**kwargs)
		context['nav_groups'] = ThematicGroup.objects.all()
		context['raiting'] = Raiting.objects.all()
		context['header'] = self.header
		context['category'] = Category.objects.get(name=self.category)

		context['genre_groups'] = []

		# вычисляем, сколько раз встретился каждый жанр
		# на данной странице (фича аля яндекс.маркет)
		num_genres = {}
		for genre in Genre.objects.all():
			num_genres[genre.name] = 0

		for item in self.queryset:
			genres = item.genres.all()
			for genre in genres:
				num_genres[genre.name] += 1

		# число жанров будет пересчитываться,
		# ибо содержимое страницы непостоянно в реальном времени
		for group in self.genre_groups:
			p = GenreGroup.objects.get(name=group)

			g = []
			for item in p.genres:
				item.__setattr__('count', num_genres[item.name])
				g.append(item)
			d = {'name': p.name, 'genres': g}
			context['genre_groups'].append(d)

		for item in context['raiting']:
			item.count = 0
			for val in self.queryset:
				if val.old_limit == item:
					item.count += 1
		print(context['genre_groups'])
		return context


class BaseChoiceMixin(ListPageMixin):

	def get_queryset(self):
		qs = {}
		tmp = self.args[0].split('/')

		# избавляемся от пустых значений
		tmp = list(filter(lambda item: item, tmp))

		keys = tmp[::2]
		values = [item.split(',') for item in tmp[1::2]]
		qs = dict(zip(keys, values))

		tmp = qs.get('old_limit')
		q = []
		if tmp:
			q, *rest = tmp
			q = Q(old_limit__name=q)
			for item in rest:
				q = q.__or__(Q(old_limit__name=item))

		if isinstance(q, list):
			q = self.model.objects
		else:
			q = self.model.objects.filter(q)
		
		tmp = qs.get('genres')
		if tmp:
			for item in tmp:
				q = q.filter(genres__name=item)
		self.queryset = q

		return self.queryset


class MainPage(BasePageMixin, ListView):
	model = ThematicGroup
	template_name = 'index.html'
	header = 'Welcome'

#------- views for anime ---------
class AnimeListView(ListPageMixin, ListView):
	template_name = 'list.html'
	model = Anime
	header = 'Список аниме'
	category = 'Anime'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Anime School', 'Standart', 'Anime Porn']


class AddAnime(BasePageMixin, CreateView):
	model = Anime
	form_class = AddForm
	template_name = 'forms/add_form.html'
	header = 'Добавление продукта'
	success_url = '/anime'
	category = 'Anime'


class AnimeDetail(DetailPageMixin, DetailView):
	template_name = 'detail.html'
	model = Anime
	category = 'Anime'


class AnimeSeriesView(ChildDetailPageMixin, ListView):
	template_name = 'components/series.html'
	model = AnimeSeason
	category = "Anime"
	parent_model = Anime


def add_season(request):
	form = AddAnimeSeasonsForm(request.POST)
	if form.is_valid():
		form.save()
		return HttpResponse('Ok')


def anime_series(request):
	data = request.POST.copy()
	q = AnimeSeason.objects.filter(link=data['anime'])
	if not q:
		AnimeSeason.objects.create(
			number=1, link=Anime.objects.get(id=data['anime']))
	data['season'] = AnimeSeason.objects.filter(
		link=data['anime']
	).last().id
	print(data)
	form = AddAnimeSeriesForm(data)
	if form.is_valid():
		form.save()
		return HttpResponse()
	return HttpResponse('Invalid Form')


class AnimeChoiceView(BaseChoiceMixin, ListView):
	model = Anime
	template_name = 'list.html'
	header = 'Выборка'
	category = 'Anime'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Anime School', 'Standart', 'Anime Porn']


#----------views for manga------------
class MangaListView(ListPageMixin, ListView):
	template_name = 'list.html'
	model = Manga
	header = 'Список манги'
	category = 'Manga'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Anime School', 'Standart', 'Anime Porn']


class AddManga(BasePageMixin, CreateView):
	model = Manga
	form_class = AddMangaForm
	template_name = 'forms/add_form.html'
	header = 'Добавление манги'
	success_url = '/manga'
	category = 'Manga'


class MangaDetailView(DetailPageMixin, DetailView):
	template_name = 'detail.html'
	model = Manga


class MangaChoiceView(ListPageMixin, BasePageMixin, ListView):
	model = Manga
	template_name = 'list.html'
	header = 'Выборка манги по жанрам'
	category = 'Manga'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Anime School', 'Standart', 'Anime Porn']
