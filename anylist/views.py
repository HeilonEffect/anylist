# -*- encoding: utf-8 -*-
import json
import logging
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import F, Max, Q
from django.http import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from braces.views import LoginRequiredMixin

from myapp.models import *
from myapp.forms import *

logger = logging.getLogger(__name__)


get_category = lambda self: ''.join(
    [self.kwargs['category'][0].upper(), self.kwargs['category'][1:]])


class BasePageMixin(object):

    def get_context_data(self, **kwargs):
        context = super(BasePageMixin, self).get_context_data(**kwargs)
        context['nav_groups'] = CategoryGroup.objects.all()

        if self.kwargs.get('category'):
            context['category'] = get_category(self)
            context['pk'] = self.kwargs.get('pk')

            category_group = None
            for item in Category.objects.all():
                url = item.get_absolute_url()[1:-1]
                if url == context['category'].lower():
                    context['category_id'] = item.id
                    category_group = item

            context['raiting'] = Raiting.objects.all()
            for limit in context['raiting']:
                limit.count = 0

            context['genres'] = [genre
                                 for item in GenreGroup.objects.filter(
                                     category__category=category_group
                                 ) for genre in item.genres.all()]
            for genre in context['genres']:
                genre.count = 0
        return context


def main_page(request):
    return render(request, 'index.html')


@require_http_methods(['GET'])
def profile(request):
    ''' User Profile '''
    result = {}
    result['nav_groups'] = CategoryGroup.objects.all()
    mylist = UserList.objects.filter(user=request.user)

    result['object_list'] = []
    statuses = Status.objects.all()
    for category in Category.objects.all():
        tmp = []
        for status in statuses:
            p = mylist.filter(
                product__category=category, status=status).count()
            if p > 0:
                tmp.append({
                    'status': status.name,
                    'count': p
                })
        if tmp:
            result['object_list'].append({'key': category, 'values': tmp})
    return render(request, 'profile.html', result)


@require_http_methods(['POST'])
@login_required
def add_list_serie(request):
    ''' Add selected serie to SerieList table (watched) '''
    try:
        form = AddToListSerieForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            serie = Serie.objects.get(**cd)

            try:
                user_list = UserList.objects.get(
                    product=cd['product'], user=request.user)
            except Exception as e:
                logger.error(e)  # del it
                user_list = UserList.objects.create(
                    product=cd['product'], user=request.user,
                    status=Status.objects.get(name='Watch'))

            if not SerieList.objects.filter(serie=serie, user_list=user_list):
                SerieList.objects.create(serie=serie, user_list=user_list)
            return HttpResponse('Ok')
        else:
            logger.error('Invalid data from series addition')
            logger.error('data %s' % request.POST)
            return HttpResponse('Ooooops')
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError()


@require_http_methods(['POST'])
@login_required
def del_list_serie(request):
    ''' Deleting Serie from UserList '''
    try:
        form = AddToListSerieForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            serie = Serie.objects.get(**cd)

            user_list = UserList.objects.get(product=cd['product'],
                                             user=request.user)

            SerieList.objects.filter(serie=serie, user_list=user_list).delete()
            return HttpResponse()
        else:
            logger.error('Invalid data form series deletion')
            logger.error('data: %s' % request.POST)
            return HttpResponse('Ooooops')
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError()


class MyList(BasePageMixin, LoginRequiredMixin, ListView):

    ''' список произведений, составленный пользователем '''
    template_name = 'user_list.html'

    def get_queryset(self):
        # ReWrite This!!!
        status = self.kwargs['status'][:1].upper() +\
            self.kwargs['status'][1:]
        if status == 'Rewatching':
            status = 'ReWatching'

        category = self.kwargs['category']
        for item in Category.objects.all():
            if item.get_absolute_url()[1:-1] == category:
                category = item
        queryset = UserList.objects.filter(user=self.request.user,
                                           status__name=status,
                                           product__category=category)
        return queryset


def product_list(request, category):
    context = {'category': category, 'header': 'List of %s' % category}
    return render(request, 'list.html', context)


class ProductDetail(BasePageMixin, DetailView):

    ''' Web page for a single product '''
    model = Product
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['header'] = context['object'].title
        return context


@login_required
def product_edit(request, category, pk):
    context = {'header': 'Edit %s' % category}
    return render(request, 'forms/add_form.html', context)


@require_http_methods(['POST'])
@login_required
def add_serie(request, category, pk):
    ''' Добавляем новую серию в указанный сезон '''
    try:
        form = AddSerieForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            return HttpResponseServerError(json.dumps(form.errors))
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError()


# TODO: review
def edit_serie(request):
    cd = request.POST.copy()
    g = SeriesGroup.objects.get(
        product=cd['product'], number=int(cd['season']))
    old = cd['ident']   # номер той серии, что мы правим
    cd['season'] = g.id     # id сезона
    form = AddSerieForm(cd)
    if form.is_valid():
        cd = form.cleaned_data
        Serie.objects.filter(number=old, season=g.id).update(**cd)
        return HttpResponse('success')
    result = json.dumps([item for item in form.errors.keys()])
    return HttpResponse(result)

@csrf_exempt
@require_http_methods(['POST', 'GET'])
def auth1(request, url):
    print(request.POST)
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


@require_http_methods(['POST', 'GET'])
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


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def auth(request, url):
    try:
        if request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = User.objects.get(username=cd['username'])
                return auth1(request, url)
            logger.debug(form.errors)
            return HttpResponse(json.dumps(form.errors))
        else:
            return HttpResponseRedirect('/%s' % url)
    except Exception as e:
        logger.error(e)


@require_http_methods(['POST', 'GET'])
@login_required
def log_out(request, url):
    logout(request)
    if 'profile' in url:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/' + url)


def add_product(request, category):
    context = {'category': category, 'header': 'Add new %s' % category}
    return render(request, 'forms/add_form.html', context)


class SerieView(BasePageMixin, ListView):

    ''' List of series by concrete product '''
    template_name = 'series.html'

    def series_serialize(self):
        ''' json-like format, describe series list '''
        p = Serie.objects.filter(product__id=self.kwargs['pk'])
        if p:
            num_season = p.aggregate(Max('num_season'))['num_season__max']
            result = [{'series': p.filter(num_season=item + 1).values(),
                       'number': item + 1}
                      for item in range(num_season)]
            result = result[::-1]

            vals = [item.serie.id for item in self.queryset]

            if self.request.user.is_authenticated():
                for season in result:
                    for serie in season['series']:
                        if serie['id'] in vals:
                            serie['listed'] = 'Remove from List'
                        else:
                            serie['listed'] = 'Add To List'
            num_season = len(result)
            result = str(result).replace('None', '"-"')
            return result, num_season
        return [], 0

    def get_queryset(self):
        ''' List of readed series '''
        self.queryset = SerieList.objects.filter(
            user_list__product__id=self.kwargs['pk'],
            user_list__user=self.request.user.id)
        return self.queryset


class HeroView(BasePageMixin, DetailView):
    model = Hero
    template_name = 'hero.html'


class HeroesListView(BasePageMixin, ListView):
    template_name = 'heroes_list.html'

    def get_queryset(self):
        return Product.objects.get(id=self.kwargs['pk']).heroes.all()


class AddHero(LoginRequiredMixin, BasePageMixin, CreateView):
    model = Hero
    template_name = 'forms/add_hero.html'
    form_class = AddHeroForm

    def get_success_url(self):
        p = Hero.objects.last()
        Product.objects.get(id=self.kwargs['pk']).heroes.add(p)
        return p.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(AddHero, self).get_context_data(**kwargs)
        context['url'] = '/%s/%s-%s/heroes/add' % (self.kwargs['category'],
                                                   self.kwargs['pk'],
                                                   self.kwargs['name'])
        return context


class CreatorView(BasePageMixin, DetailView):
    model = Creator
    template_name = 'creator.html'


class CreatorsListView(BasePageMixin, ListView):
    template_name = 'creators_list.html'

    def get_queryset(self):
        return Product.objects.get(id=self.kwargs['pk']).creators.all()

    def get_context_data(self, **kwargs):
        context = super(CreatorsListView, self).get_context_data(**kwargs)
        return context


class AddCreator(LoginRequiredMixin, BasePageMixin, CreateView):
    model = Creator
    template_name = 'forms/add_creator.html'

    def get_success_url(self):
        return Creator.objects.last().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(AddCreator, self).get_context_data(**kwargs)
        context['employers'] = Employ.objects.all()
        return context


def error404(request):
    context = {}
    context['nav_groups'] = CategoryGroup.objects.all()
    return render(request, 'error.html', context)
