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

#from apps.models import *
#from apps.forms import *
#from apps.serializers import ProductSerializer

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
            context['category_id'] = Category.objects.get(
                name=context['category']).id
            context['raiting'] = Raiting.objects.all()
            for limit in context['raiting']:
                limit.count = 0

            context['genres'] = [genre
                for item in GenreGroup.objects.filter(category_id=context['category_id'])
                for genre in item.genres.all()]
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
    ''' страница профиля пользователя '''
    result = {}
    result['nav_groups'] = CategoryGroup.objects.all()
    result['category'] = Category.objects.all()
    st = Status.objects.all()
#    for cat in result['category']:
#        status = [item for item in st]
#        values = []
#        cat.status = []
#        for item in status:
#            kwargs = {'status__name': item}
#            k = F('product__%s__link' % cat.name.lower())
#            kwargs['product'] = k
#            cat.status.append({'name': item, 'count': 
#                ListedProduct.objects.filter(**kwargs).count()})
    return render(request, 'profile.html', result)


@require_http_methods(['POST'])
def add_list_serie(request):
    ''' добаваляем серию в список просмотренных '''
    try:
        form = AddSerieForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ListedProduct.objects.get(product=cd['product'], user=request.user
                ).series.add(Serie.objects.get(product=cd['product'],
                    num_season=cd['num_season'], number=cd['number']))
            return HttpResponse('ok')
        else:
            return HttpResponseServerError()
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError()


@require_http_methods(['POST'])
def del_list_serie(request):
    ''' Удаляем серию из списка просмотренных '''
    try:
        form = AddSerieForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ListedProduct.objects.get(product=cd['product'], user=request.user
                ).series.remove(Serie.objects.get(product=cd['product'],
                    num_season=cd['num_season'], number=cd['number']))
            return HttpResponse('Ok')
        else:
            return HttpResponseServerError()
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError()


class MyList(LoginRequiredMixin, ListView):
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
        print(context['object_list'])
        context['nav_groups'] = ThematicGroup.objects.all()

        category = self.kwargs['category'][:1].upper() +\
            self.kwargs['category'][1:]

        context['category'] = Category.objects.get(
            name=category).get_absolute_url()
        context['status'] = Status.objects.all()
        return context


@require_http_methods(['POST'])
def add_list(request):
    ''' Добавляем произведение в список '''
    cd = request.POST.copy()
    cd['status'] = 1    # запланировано
    cd['user'] = request.user.id
    form = AddToListForm(cd)
    if form.is_valid():
        form.save()
        return HttpResponse('success')
    return HttpResponse(str(form))


class ProductionList(BasePageMixin, ListView):
    '''
    List of multimedia product of selected category
    (anime, sci-fi, detective romans, etc.)
    '''
    template_name = 'list.html'

    def get_queryset(self):
        category = self.kwargs['category']
        category = ''.join([category[0].upper(), category[1:]])
        return Product.objects.filter(category__name=category)

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


def remove_from_list(request, pk):
    ListedProduct.objects.filter(user=request.user, product__id=pk).delete()
    return HttpResponse('Ok')


class ProductDetail(BasePageMixin, DetailView):
    model = Product
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['header'] = context['object'].title
        context['category'] = self.kwargs['category']
        context['statuses'] = Status.objects.all()
        context['is_listed'] = UserList.objects.get(
            user=self.request.user.id, product__title=context['object'].title)
        return context


class ProductionEdit(BasePageMixin, UpdateView):
    template_name = 'forms/edit_form.html'
    model = Product
    form_class = AddProductForm

    def get_success_url(self):
        return '/%s/' % self.kwargs['category']

    def form_invalid(self, form):
        print(form.errors)

    def get_context_data(self, **kwargs):
        context = super(ProductionEdit, self).get_context_data(**kwargs)

        context['header'] = 'Edit %s' % get_category(self)
        context['use_genres'] = self.model.objects.get(
            id=self.kwargs['pk']).genres.values()
        return context


@require_http_methods(['POST'])
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

    def get_context_data(self, **kwargs):
        context = super(AddProduct, self).get_context_data(**kwargs)
        category = get_category(self)
        p = Category.objects.get(name=category).group
        
        context['category'] = self.kwargs['category']
        context['category_id'] = Category.objects.get(name=category).id
        context['header'] = 'Add new %s' % category
        return context


class SerieView(BasePageMixin, ListView):
    ''' List of series by concrette product '''
    template_name = 'series.html'

    def series_serialize(self):
        p = Serie.objects.filter(product__id=self.kwargs['pk'])
        if p:
            num_season = p.aggregate(Max('num_season'))['num_season__max']
            result = [{'series': p.filter(num_season=item + 1).values(), 
                'number': item + 1}
                for item in range(num_season)]
            result = result[::-1]
            result = str(result).replace('None', '"-"')
            return result
        return []
    
    def get_queryset(self):
        return UserList.objects.filter(
            product__id=self.kwargs['pk'], user=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(SerieView, self).get_context_data(**kwargs)
        p = Serie.objects.filter(product__id=self.kwargs['pk'])
        
        context['num_season'] = Serie.objects.filter(
            product__id=self.kwargs['pk']).aggregate(Max('num_season')
            )['num_season__max'] or 0
        context['series'] = self.series_serialize()
        
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