# -*- encoding: utf-8 -*-
import json
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.cache import cache
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView

from braces.views import LoginRequiredMixin

from apps.models import *
from apps.forms import *
from anylist.mixins import *


#------------ Base Views -----------------
class MainPage(ListView):
	model = ThematicGroup
	template_name = 'index.html'


def profile(request):
	''' профиль пользователя '''
	result = {}
	result['status'] = Status.objects.all()
	result['planned_manga'] = ListedProduct.objects.filter(
		product=F('product__manga__link'), status__name='Запланировано'
	).count()
	result['reading_manga'] = ListedProduct.objects.filter(
		product=F('product__manga__link'), status__name='Смотрю'
	)
	result['readed_manga'] = ListedProduct.objects.filter(
		product=F('product__manga__link'), status__name='Просмотрел'
	)
	result['rewatching_manga'] = ListedProduct.objects.filter(
		product=F('product__manga__link'), status__name='Пересматриваю'
	)
	result['dropped_manga'] = ListedProduct.objects.filter(
		product=F('product__manga__link'), status__name='Бросил'
	)
	result['deffered_manga'] = ListedProduct.objects.filter(
		product=F('product__manga__link'), status__name='Отложил'
	)
	result['category'] = Category.objects.all()
#	result['anime'] = ListedProduct.objects.filter(
#		product=F('product__anime__link')Ц
#	)
	return render(request, 'profile.html', result)


def add_list_serie(request):
	''' добваляем серию в список просмотренных '''
	p = Serie.objects.get(number=request.POST['number'],
		season__product=request.POST['product'],
		season__number=request.POST['season']
	)
	product = ListedProduct.objects.get(product=request.POST['product'])
	product.series.add(p)
	return HttpResponse("ok")


def delete_list_serie(request):
	''' удаляем серию из списка просмотренных (пока не реализовано) '''
	p = Serie.objects.get(number=request.POST['number'],
		season__product=request.POST['product'],
		season__number=request.POST['season']
	)
	product = ListedProduct.objects.get(product=request.POST['product'])
	product.series.remove(p)
	return HttpResponse("ok")


class UserList(ListView):
	''' список произведений, составленный пользователем '''
	template_name = 'user_list.html'

	def get_queryset(self):
		# Так мы делаем первую букву заглавной
		status = self.kwargs['status'][:1].upper() +\
			self.kwargs['status'][1:]
		self.queryset = ListedProduct.objects.filter(
			product=F('product__%s__link' % self.kwargs['category']),
			status__name=status
		)
		return self.queryset

	def get_context_data(self, **kwargs):
		context = super(UserList, self).get_context_data(**kwargs)

		category = self.kwargs['category'][:1].upper() +\
			self.kwargs['category'][1:]

		context['category'] = Category.objects.get(
			name=category).get_absolute_url()
		return context


def add_list(request):
	''' Добавляем произведение в список '''
	cd = request.POST.copy()
	cd['status'] = 1	# запланировано
	cd['user'] = request.user.id
	form = AddToListForm(cd)
	if form.is_valid():
		form.save()
		return HttpResponse('success')
	return HttpResponse(str(form))


#------- views for anime ---------
class AnimeListView(ListPageMixin, ListView):
	template_name = 'list.html'
	model1 = Anime
	header = 'Список аниме'
	category = 'Anime'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Standart', 'Anime Porn', 'Anime School']


class AddAnime(BasePageMixin, CreateView):
	model = Anime
	form_class = AddForm
	template_name = 'forms/add_form.html'
	header = 'Добавление продукта'
	success_url = '/anime'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Anime Standart', 'Anime School']


def add_anime(request):
	''' В случае с аниме, сезон всегда один, если есть второй сезон с
	аналогичным названием, то называем его <Название> [TV-2]. При
	создании любого экзампляра по-умолчанию создаем новый сезон '''
	form = AddForm(request.POST, request.FILES)
	if form.is_valid():
		cd = form.cleaned_data
		# Сохраням продукт
		form.save()
		p = Production.objects.filter(title=cd['title']).last()
		# Регистрируем новое аниме
		Anime.objects.create(link=p)

		# Создаём первый сезон
		SeriesGroup.objects.create(number=1, product=p)
		return HttpResponseRedirect('/anime')
	return HttpResponse(str(form))


class AnimeDetail(DetailPageMixin, DetailView):
	pass


class AnimeEdit(BasePageMixin, UpdateView):
	template_name = "forms/edit_form.html"
	model = Production
	genre_groups =\
		['Anime Male', 'Anime Female', 'Standart', 'Anime Porn', 'Anime School']


class AnimeChoiceView(BaseChoiceMixin, ListView):
	model = Production
	model1 = Anime
	template_name = 'list.html'
	header = 'Выборка'
	category = 'Anime'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Standart', 'Anime Porn', 'Anime School']


class AnimeSeriesView(InfoPageMixin, ListView):
	template_name = 'components/series.html'


def add_serie(request):
	''' в случае с аниме сезон на одно название всегда один, поэтому
	мы посылаем id самого аниме '''
	cd = request.POST.copy()
	g = SeriesGroup.objects.get(product=cd['product'])
	cd['season'] = g.id
	del cd['product']
	form = AddSerieForm(cd)
	if form.is_valid():
		cd = form.cleaned_data
		form.save()
		return HttpResponse('success')
	return HttpResponse('Invalid form data')


def edit_serie(request):
	''' Правим данные в анимешнной серии '''
	cd = request.POST.copy()
	g = SeriesGroup.objects.get(product=cd['product'])
	cd['season'] = g.id
	old = cd['ident']
	del cd['product']
	form = AddSerieForm(cd)
	if form.is_valid():
		cd = form.cleaned_data
		Serie.objects.filter(number=old, season=g.id).update(**cd)
		return HttpResponse('succes')
	return HttpResponse(str(form))


def auth1(request, url):
	url = "/%s" % url
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect(url)
		else:
			return HttpResponse('Account Disabled')
	else:
		return HttpResponse('Username or password incorrect')


def register(request, url):
	if request.POST:
		form = RegisterForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = User.objects.create_user(**cd)
			user.save()
			return auth1(request, url)
		return HttpResponse(str(form))
	else:
		return HttpResponseRedirect('/%s' % url)


def auth(request, url):
	if request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = User.objects.get(username=cd['username'])
			return auth1(request, url)
		return HttpResponse(str(form))
	else:
		return HttpResponseRedirect('/%s' % url)


def log_out(request, url):
	logout(request)
	print(url)
	return HttpResponseRedirect('/' + url)


#----------views for manga------------
class MangaListView(ListPageMixin, ListView):
	template_name = 'list.html'
	model = Production
	model1 = Manga
	header = 'Список манги'
	category = 'Manga'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Anime School', 'Standart', 'Anime Porn']


class AddManga(BasePageMixin, CreateView):
	model = Production
	form_class = AddForm
	template_name = 'forms/add_form.html'
	header = 'Добавление манги'
	success_url = '/manga/'
	genre_groups =\
		['Anime Male', 'Anime Female', 'Standart', 'Anime Porn', 'Anime School']


def add_manga(request):
	form = AddForm(request.POST, request.FILES)
	if form.is_valid():
		cd = form.cleaned_data
		form.save()
		p = Production.objects.filter(title=cd['title']).last()
		Manga.objects.create(link=p)
		return HttpResponseRedirect('/manga')
	return HttpResponse('Invalid form')


def add_manga_vol(request):
	''' Т.к у манги несколько томов (SeriesGroup), то
	кнопка добавления серии появляется возле каждого конкретного
	тома '''
	cd = request.POST.copy()
	cd['number'] = SeriesGroup.objects.filter(
		product=cd['product']).last() or 1
	if cd['number'] != 1:
		cd['number'] = cd['number'].number + 1
	form = AddMangaVolumeForm(cd)
	if form.is_valid():
		form.save()
		return HttpResponse('success')
	return HttpResponse(str(form))


def add_manga_serie(request):
	''' У манги может быть несолько томов, поэтому мы будем иметь
	возможность добавить новый том '''
	cd = request.POST.copy()
	cd['season'] = SeriesGroup.objects.get(
		product=cd['product'], number=cd['season']).id
	del cd['product']
	form = AddSerieForm(cd)
	print(cd)
	if form.is_valid():
		form.save()
		return HttpResponse('success')
	return HttpResponse(str(form))


class MangaSeriesView(InfoPageMixin, ListView):
	template_name = 'manga/series.html'


class MangaDetailView(DetailPageMixin, DetailView):
	pass


class MangaChoiceView(BaseChoiceMixin, ListView):
	model = Production
	template_name = 'list.html'
	header = 'Выборка манги по жанрам'
	category = 'Manga'
	genre_groups =\
		['Anime Male', 'Anime Female']#, 'Anime School', 'Standart', 'Anime Porn']
	model1 = Manga
