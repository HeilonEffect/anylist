from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView

from content.models import *


class BasePageMixin(object):
	category = ''
	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		context['header'] = self.header
		context['category'] = self.category
		return context


class MainView(BasePageMixin, ListView):
	''' Главная страница '''
	header = '''Здесь вы можете хранить списки книг и фильмов,
		которые смотрели или планируете посмотреть'''
	template_name = 'index.html'
	model = Categories


class JapView(BasePageMixin, ListView):
	template_name = 'japanese.html'
	model = Anime
	header = 'Anime'
	category = 'Anime'


class AnimeView(BasePageMixin, CreateView):
	template_name = 'forms/add_form.html'
	model = Anime
	header = 'Add New Anime'
	category = 'Anime'