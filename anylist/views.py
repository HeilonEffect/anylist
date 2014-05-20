import json
import re

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView

from apps.models import *
from apps.forms import AddForm


class BasePageMixin(object):
	''' Содержит одинаковые для всех классов приложения операции '''
	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		context['header'] = self.header
		context['genres'] = Genre.objects.all()
		return context



class MainPage(BasePageMixin, ListView):
	model = Anime
	template_name = 'list.html'
	header = 'Welcome'


class AddAnime(BasePageMixin, CreateView):
	model = Anime
	form_class = AddForm
	template_name = 'forms/add_form.html'
	header = 'Добавление продукта'

	def post(self, request):
		form = AddForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponse('Valid Form')
		return HttpResponse('Invalid Form')


def save_anime(request):
	print(request.POST)
	return HttpResponse()