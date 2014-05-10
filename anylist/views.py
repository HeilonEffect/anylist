from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView

from content.models import *


class BasePageMixin(object):
	header = ''
	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		context['header'] = self.header
		return context


class PaginateMixin(object):
	''' Делает выборку ограниченного полем count числа элементов
	из каждой из нескольких	указанных таблиц '''
	count = 5
	db = []

	def get_context_data(self, **kwargs):
		context = super(PaginateMixin, self).get_context_data(**kwargs)
		context['object_list'] = []
		for item in self.db:
			context['object_list'].append(item.objects.all()[:self.count])


class MainView(ListView):
	''' Главная страница '''
	header = '''Здесь вы можете хранить списки книг и фильмов,
		которые смотрели или планируете посмотреть'''
	template_name = 'index.html'
	model = Categories


class JapView(PaginateMixin, TemplateView):
	template_name = 'japanese.html'
	db = [Anime]
