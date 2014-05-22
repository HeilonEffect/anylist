# -*- encoding: utf-8 -*-
import json
import re

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from apps.models import *
from apps.forms import AddForm


class BasePageMixin(object):
	''' Содержит одинаковые для всех классов приложения операции '''
	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		context['header'] = self.header
		context['genres'] = Genre.objects.all()
		return context


class DetailPageMixin(object):
	def get_context_data(self, **kwargs):
		context = super(DetailPageMixin, self).get_context_data(**kwargs)
		return context


class ListPageMixin(object):
	def get_context_data(self, **kwargs):
		context = super(ListPageMixin, self).get_context_data(**kwargs)
		context['genre_groups'] = []
		for group in self.genre_groups:
			context['genre_groups'].append(GenreGroup.objects.get(name=group))
		return context


class MainPage(BasePageMixin, ListView):
	model = Anime
	template_name = 'list.html'
	header = 'Welcome'

#------- views for anime ---------
class AnimeListView(ListPageMixin, ListView):
	template_name = 'list.html'
	model = Anime
	genre_groups = ['Japanese Male', 'Japanese Female']


class AddAnime(BasePageMixin, CreateView):
	model = Anime
	form_class = AddForm
	template_name = 'forms/add_form.html'
	header = 'Добавление продукта'

	def post(self, request):
		form = AddForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/anime')
		return HttpResponse('Invalid Form')


class AnimeDetail(DetailView):
	template_name = 'detail.html'
	model = Anime