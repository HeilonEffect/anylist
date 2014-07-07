# -*- encoding: utf-8 -*-
import json
import itertools
import functools
import logging
import operator
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import F, Max, Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render_to_response, render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
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
                if item.get_absolute_url()[1:-1] == context['category'].lower():
                    context['category_id'] = item.id
                    category_group = item

            context['raiting'] = Raiting.objects.all()
            for limit in context['raiting']:
                limit.count = 0

            context['genres'] = [genre
                for item in GenreGroup.objects.filter(
                    category__category=category_group) for genre in item.genres.all()]
            for genre in context['genres']:
                genre.count = 0
        return context


class MainPage(BasePageMixin, ListView):
    ''' Main Page view. Content of main categories '''
    model = CategoryGroup
    template_name = 'index.html'


@require_http_methods(['GET'])
def search(request):
    ''' Простейший поиск по названиям произведений '''
    try:
        if len(request.GET['key']) > 1:
            result = dict(map(
                lambda item:
                (item.title, item.get_absolute_url()),
                Product.objects.filter(Q(title__icontains=request.GET['key']))
            ))

            return HttpResponse(
                json.dumps(result), content_type='application/json')
        else:
            return HttpResponse()
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError()


@login_required(login_url='/')
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
                logger.error(e) # del it
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
            status__name=status, product__category=category)
        return queryset


class ProductionList(BasePageMixin, ListView):
    '''
    List of multimedia product of selected category
    (anime, sci-fi, detective romans, etc.)
    '''
    template_name = 'list.html'

    def get_queryset(self):
        category = self.kwargs['category']
        for item in Category.objects.all():
            if item.get_absolute_url()[1:-1] == category:
                category = item
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super(ProductionList, self).get_context_data(**kwargs)
        context['header'] = 'List of %s' % self.kwargs['category']
        for product in context['object_list']:
            genres = product.genres.all()
            for genre in context['genres']:
                if genre in genres:
                    genre.count += 1
            for limit in context['raiting']:
                if limit == product.old_limit:
                    limit.count += 1
        return context


@require_http_methods(['POST'])
@login_required
def status_update(request, pk):
    ''' Process post-request with new status
    (especialy processing situation, where product not in user list yet) '''
    try:
        status = Status.objects.get(name=request.POST['name'])
        p = UserList.objects.filter(
            user=request.user, product__id=pk)
        if p:
            p.update(status=status)
        else:
            p = Product.objects.get(id=pk)
            UserList.objects.create(user=request.user, product=p, status=status)
        return HttpResponse(request.POST['name'])
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError()


# @require_http_methods(['POST'])
# @login_required
# def remove_from_list(request, pk):
#     UserList.objects.filter(user=request.user, product__id=pk).delete()
#     return HttpResponse()


class ProductDetail(BasePageMixin, DetailView):
    ''' Web page for a single product '''
    model = Product
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['header'] = context['object'].title
        context['category'] = self.kwargs['category']
        context['statuses'] = Status.objects.all()
        try:
            context['is_listed'] = UserList.objects.get(
                user=self.request.user.id,
                product__title=context['object'].title)
        except Exception as e: pass
        return context


class ProductionEdit(LoginRequiredMixin, BasePageMixin, UpdateView):
    template_name = 'forms/edit_form.html'
    model = Product
    form_class = AddProductForm

    def get_success_url(self):
        return '/%s/' % self.kwargs['category']

    def form_invalid(self, form):
        print(form.errors)
        return HttpResponse(form.errors)

    def get_context_data(self, **kwargs):
        context = super(ProductionEdit, self).get_context_data(**kwargs)

        context['header'] = 'Edit %s' % get_category(self)
        context['use_genres'] = self.model.objects.get(
            id=self.kwargs['pk']).genres.values()
        return context


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
    g = SeriesGroup.objects.get(product=cd['product'], number=int(cd['season']))
    old = cd['ident']   # номер той серии, что мы правим
    cd['season'] = g.id     # id сезона
    form = AddSerieForm(cd)
    if form.is_valid():
        cd = form.cleaned_data
        Serie.objects.filter(number=old, season=g.id).update(**cd)
        return HttpResponse('success')
    result = json.dumps([item for item in form.errors.keys()])
    return HttpResponse(result)


@require_http_methods(['POST', 'GET'])
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


class AddProduct(LoginRequiredMixin, BasePageMixin, CreateView):
    ''' Creating and Pubishing new product by form data '''
    template_name = 'forms/add_form.html'
    model = Product
    form_class = AddProductForm
    raise_exception = True

    def form_invalid(self, form):
        print(form.errors)
        return HttpResponse(form.errors)

    def get_context_data(self, **kwargs):
        context = super(AddProduct, self).get_context_data(**kwargs)

        context['category'] = self.kwargs['category']
        for item in Category.objects.all():
            if item.get_absolute_url() == context['category']:
                context['category_id'] = item.id
                context['header'] = 'Add new %s' % category
        return context


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

    def get_context_data(self, **kwargs):
        context = super(SerieView, self).get_context_data(**kwargs)
        p = Serie.objects.filter(product__id=self.kwargs['pk'])

        context['series'], context['num_season'] = self.series_serialize()
        return context


class ProductionChoiceView(ProductionList):
    template_name = 'list.html'
    model = Product

    def get_queryset(self):
        qs = {}
        tmp = self.kwargs['args'].split('/')

        tmp = list(filter(lambda item: item, tmp))

        qs = dict(zip(tmp[::2], [item.split(',') for item in tmp[1::2]]))

        tmp = qs.get('old_limit')
        q = []
        f = lambda item: Q(old_limit__name=item)
        if tmp:
            q = functools.reduce(operator.or_, map(f, tmp))

        category = get_category(self)
        if isinstance(q, list):
            q = self.model.objects.filter(category__name=category)
        else:
            q = self.model.objects.filter(category__name=category).filter(q)

        tmp = qs.get('genres')
        if tmp:
            for item in tmp:
                q = q.filter(genres__name=item)
        return q

    def get_context_data(self, **kwargs):
        context = super(ProductionChoiceView, self).get_context_data(**kwargs)
        context['header'] = 'Selection of %s' % get_category(self)
        return context


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
            self.kwargs['pk'], self.kwargs['name'])
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