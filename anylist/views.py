import json
import re

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView

from content.models import *
from content.models import UploadForm

from pymongo import Connection


db = connection.test_database

title_to_path =lambda title, hub:
	'%s/%s' % (hub, ''.join(re.split(r'[ -_:]', title.lower())))


class BasePageMixin(object):
	''' Содержит одинаковые для всех классов приложения операции '''
	category = ''
	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		#context['header'] = self.header
		context['category'] = self.category
		#context['genres'] = Genre.objects.all()
		context['category_genres'] = Category.objects.all()
		context['studies'] = Studio.objects.all()
		context['raiting'] = Raiting.objects.all()
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

	def post(self, request):
		js = json.load(request.POST['data'])

		# загрузка картинки
		avatar = request.FILES['avatar']
		with open(, 'wb+') as f:
			for chunk in avatar.chunks:
				f.write(chunk)


class TmpView(BasePageMixin, TemplateView):
	template_name = 'detail.html'
