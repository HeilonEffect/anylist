# -*- encoding: utf-8 -*-
import json
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView

from braces.views import LoginRequiredMixin

from apps.models import *
from apps.forms import *
from anylist.mixins import *


#------------ Base Views -----------------
class MainPage(BasePageMixin, ListView):
	model = ThematicGroup
	template_name = 'index.html'
	header = 'Welcome'


class ProfileView(LoginRequiredMixin, ListView):
	template_name = 'profile.html'
	model = ThematicGroup

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		return context


#------- views for anime ---------
class AnimeListView(ListPageMixin, ListView):
	template_name = 'list.html'
	model = Production
	model1 = Anime
	header = 'Список аниме'
	category = 'Anime'
	genre_groups =\
		['Anime Male', 'Anime Female']#, 'Anime School', 'Standart', 'Anime Porn']


class AddAnime(BasePageMixin, CreateView):
	model = Anime
	form_class = AddForm
	template_name = 'forms/add_form.html'
	header = 'Добавление продукта'
	success_url = '/anime'
	category = 'Anime'


def add_anime(request):
	form = AddForm(request.POST, request.FILES)
	if form.is_valid():
		cd = form.cleaned_data
		form.save()
		p = Production.objects.filter(title=cd['title']).last()
		Anime.objects.create(link=p)
		return HttpResponseRedirect('/anime')
	return HttpResponse('Invalid form data')


class AnimeDetail(DetailPageMixin, DetailView):
	template_name = 'detail.html'
	category = 'Anime'


#class AnimeSeriesView(ChildDetailPageMixin, ListView):
#	template_name = 'components/series.html'
#	model = AnimeSeason
#	category = "Anime"
#	parent_model = Anime


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
	form = AddAnimeSeriesForm(data)
	if form.is_valid():
		form.save()
		return HttpResponse()
	return HttpResponse('Invalid Form')


class AnimeChoiceView(BaseChoiceMixin, ListView):
	model = Production
	model1 = Anime
	template_name = 'list.html'
	header = 'Выборка'
	category = 'Anime'
	genre_groups =\
		['Anime Male', 'Anime Female']#, 'Anime School', 'Standart', 'Anime Porn']


def auth1(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user:
		if user.is_active:
			login(request, user)
			return HttpResponse('Succes')
		else:
			return HttpResponse('Account Disabled')
	else:
		return HttpResponse('Username or password incorrect')


def auth2(request):
	form = RegisterForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		user = User.objects.create_user(**cd)
		user.save()
	return auth1(request)


def auth(request):
	form = LoginForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		user = User.objects.get(username=cd['username'])
	return auth1(request)


def log_out(request):
	logout(request)
	return HttpResponse('logout')


#----------views for manga------------
class MangaListView(ListPageMixin, ListView):
	template_name = 'list.html'
	model = Production
	model1 = Manga
	header = 'Список манги'
	category = 'Manga'
	genre_groups =\
		['Anime Male', 'Anime Female']#, 'Anime School', 'Standart', 'Anime Porn']


class AddManga(BasePageMixin, CreateView):
	model = Production
	form_class = AddMangaForm
	template_name = 'forms/add_form.html'
	header = 'Добавление манги'
	success_url = '/manga/'
	category = 'Manga'


def add_manga(request):
	form = AddForm(request.POST, request.FILES)
	if form.is_valid():
		cd = form.cleaned_data
		form.save()
		p = Production.objects.filter(title=cd['title']).last()
		Manga.objects.create(link=p)
		return HttpResponseRedirect('/manga')
	return HttpResponse('Invalid form')


class MangaDetailView(DetailPageMixin, DetailView):
	template_name = 'detail.html'
	category = 'Manga'


class MangaChoiceView(BaseChoiceMixin, ListView):
	model = Production
	template_name = 'list.html'
	header = 'Выборка манги по жанрам'
	category = 'Manga'
	genre_groups =\
		['Anime Male', 'Anime Female']#, 'Anime School', 'Standart', 'Anime Porn']
	model1 = Manga
