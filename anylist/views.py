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
from apps.serializers import ProductSerializer

from .mixins import *


Types = {'anime': Anime, 'manga': Manga}


#------------ Base Views -----------------
class MainPage(ListView):
    model = ThematicGroup
    template_name = 'index.html'


def search(request):
    ''' Простейший поиск по названиям произведений '''
    result = dict(map(
        lambda item:
        (item.title, '/' + item.get_category() + '/' + item.get_absolute_url()),
        Production.objects.filter(Q(title__icontains=request.GET['key']))
    ))

    return HttpResponse(
        json.dumps(result), content_type='application/json')


def profile(request):
    ''' страница профиля пользователя '''
    result = {}
    result['category'] = Category.objects.all()
    st = Status.objects.all()
    for cat in result['category']:
        status = [item for item in st]
        values = []
        cat.status = []
        for item in status:
            kwargs = {'status__name': item}
            k = F('product__%s__link' % cat.name.lower())
            kwargs['product'] = k
            cat.status.append({'name': item, 'count': 
                ListedProduct.objects.filter(**kwargs).count()})
    return render(request, 'profile.html', result)


def add_list_serie(request):
    ''' добваляем серию в список просмотренных '''
    p = Serie.objects.get(number=request.POST['number'],
        season__product__id=request.POST['product'],
        season__number=request.POST['season']
    )
    product = ListedProduct.objects.get(
        product__id=request.POST['product'], user=request.user)
    product.series.add(p)
    return HttpResponse("ok")


def del_list_serie(request):
    p = Serie.objects.get(number=request.POST['number'],
        season__product=request.POST['product'],
        season__number=request.POST['season']
    )
    product = ListedProduct.objects.get(product=request.POST['product'])
    product.series.remove(p)
    return HttpResponse('Ok')


class UserList(LoginRequiredMixin, ListView):
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
        context['status'] = Status.objects.all()
        return context


def add_list(request):
    ''' Добавляем произведение в список '''
    cd = request.POST.copy()
    cd['status'] = 1    # запланировано
    cd['user'] = request.user.id
    form = AddToListForm(cd)
    if form.is_valid():
        form.save()
        return HttpResponse('success')
    print(form)
    return HttpResponse(str(form))


#------- views for anime ---------
class ProductionList(ListPageMixin, ListView):
    genre_groups =\
        ['Anime Male', 'Anime Female', 'Standart', 'Anime Porn', 'Anime School']


class AddAnime(CreateMixin, CreateView):
    header = 'Добавление продукта'
    genre_groups =\
        ['Anime Male', 'Anime Female', 'Anime Standart', 'Anime School']


def status_update(request, pk):
    p = ListedProduct.objects.get(user=request.user, product__id=pk)
    p.status=Status.objects.get(name=request.POST['name'])
    p.save()
    return HttpResponse('Ok')


def remove_from_list(request, pk):
    ListedProduct.objects.filter(user=request.user, product__id=pk).delete()
    return HttpResponse('Ok')


class ProductDetail(DetailView):
    model = Production
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['header'] = context['object'].title
        context['category'] = self.kwargs['category']
        context['is_listed'] = ListedProduct.objects.filter(
            user=self.request.user, product__title=context['object'].title
            ).first()
        return context


class AnimeEdit(BasePageMixin, UpdateView):
    template_name = "forms/edit_form.html"
    model = Production
    genre_groups =\
        ['Anime Male', 'Anime Female', 'Standart', 'Anime Porn', 'Anime School']


def add_serie(request, category, pk):
    ''' Добавляем новую серию в указанный сезон '''
    cd = request.POST.copy()
    pk = Production.objects.get(id=pk)
    p = SeriesGroup.objects.get_or_create(product=pk, number=cd['season'])
    if isinstance(p, tuple):
        p = p[0]
    cd['season'] = p.id
    form = AddSerieForm(cd)
    if form.is_valid():
        form.save()
        return HttpResponse('success')
    return HttpResponse('Invalid form data')


def edit_serie(request):
    cd = request.POST.copy()
    g = SeriesGroup.objects.get(product=cd['product'], number=int(cd['season']))
    old = cd['ident']   # номер той серии, что мы правим
    cd['season'] = g.id     # id сезона
    form = AddSerieForm(cd)
    if form.is_valid():
        cd = form.cleaned_data
        Serie.objects.filter(number=old, season=g.id).update(**cd)
        return HttpResponse('success')
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
    if 'profile' in url:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/' + url)


#----------views for manga------------
class AddManga(CreateMixin, CreateView):
    header = 'Добавление манги'
    genre_groups =\
        ['Anime Male', 'Anime Female', 'Standart', 'Anime Porn', 'Anime School']


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


class ProductionSeriesView(ListView):
    ''' передаёт дополнительную информацию в страницы, где
    указаны серии, герои, создатели и т.д '''
    template_name = 'manga/series.html'
    
    def get_queryset(self):
        self.queryset = SeriesGroup.objects.filter(product=self.kwargs['pk'])
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(ProductionSeriesView, self).get_context_data(**kwargs)
        # Список тех серий, что мы посмотрели
        context['numbers'] = [i.id for item in
            ListedProduct.objects.filter(user=self.request.user,
                product=self.kwargs['pk']) for i in item.series.all()]
        print(context['numbers'])
        context['numbers'] = json.dumps(context['numbers'])
        return context



class ProductionChoiceView(BaseChoiceMixin, ListView):
    model = Production
    template_name = 'list.html'
    header = 'Выборка манги по жанрам'
    category = 'Manga'
    genre_groups =\
        ['Anime Male', 'Anime Female']#, 'Anime School', 'Standart', 'Anime Porn']
    model1 = Manga
