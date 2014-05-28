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

from apps.models import *
from apps.forms import AddForm, AddMangaForm


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
		return context


# TODO
class AddWizard(SessionWizardView):
	def done(self, form_list, **kwargs):
		return render_to_response('done.html', {
			'form_data': [form.cleaned_data for form in form_list],
		})


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

		q = []
		if qs.get('old_limit'):
			q = Q(old_limit__name=qs['old_limit'][0])
			if len(qs['old_limit']) > 1:
				for i in range(1, len(qs['old_limit'])):
					q = q.__or__(Q(old_limit__name=qs['old_limit'][i]))

		if q:
			self.queryset = self.model.objects.filter(q)
		else:
			self.queryset = self.model.objects

		if qs.get('genres'):
			self.queryset = self.queryset.filter(genres__name=qs['genres'][0])
			if len(qs['genres']) > 1:
				for i in range(1, len(qs['genres'])):
					self.queryset = self.queryset.filter(
						genres__name=qs['genres'][i]
					)
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


class AnimeSeriesView(ListView):
	template_name = 'components/series.html'


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

