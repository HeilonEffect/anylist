# -*- encoding: utf-8 -*-
import json
import logging
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.cache import cache
from django.db.models import F, Max, Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render_to_response, render
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView

from braces.views import LoginRequiredMixin

from apps.models import *
from apps.forms import *
from apps.serializers import ProductSerializer

from .mixins import *


logger = logging.getLogger(__name__)
Types = {'anime': Anime, 'manga': Manga}

#------------ Base Views -----------------
class MainPage(ListView):
    model = ThematicGroup
    template_name = 'index.html'


@require_http_methods(['GET'])
def search(request):
    ''' Простейший поиск по названиям произведений '''
    try:
        if len(request.GET['key']) > 1:
            result = dict(map(
                lambda item:
                (item.title, '/' + item.get_category() + '/' + item.get_absolute_url()),
                Production.objects.filter(Q(title__icontains=request.GET['key']))
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


class ProductionList(ListPageMixin, ListView):
    ''' Список произведений указанной категории '''
    genre_groups =\
        ['Anime Male', 'Anime Female', 'Standart', 'Anime Porn', 'Anime School']

    def dispatch(self, *args, **kwargs):
        if 'category' not in kwargs or kwargs['category'] not in Types:
            return HttpResponseNotFound('<h1>Page not Found</h1>')
        else:
            return super(ProductionList, self).dispatch(*args, **kwargs)


def status_update(request, pk):
    ''' Меняем статус просмотра произведения '''
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

    def dispatch(self, *args, **kwargs):
        if 'pk' not in kwargs:
            return HttpResponseNotFound('<h1>PageNotFound</h1>')
        else:
            return super(ProductDetail, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['header'] = context['object'].title
        context['category'] = self.kwargs['category']
        context['is_listed'] = ListedProduct.objects.filter(
            user=self.request.user.id, product__title=context['object'].title
            ).first()
        return context


class ProductionEdit(UpdateView):
    template_name = 'forms/edit_form.html'
    model = Production

    success_url = '/manga/'

    def get_context_data(self, **kwargs):
        context = super(ProductionEdit, self).get_context_data(**kwargs)

        context['genres'] = Genre.objects.all()
        context['header'] = 'Edit %s' % self.kwargs['category']
        context['use_genres'] = json.dumps(
            [str(item.name) for item in context['object'].genres.all()],
            ensure_ascii=False
        )
        context['raiting'] = Raiting.objects.all()
        return context


@require_http_methods(['POST'])
def add_serie(request, category, pk):
    ''' Добавляем новую серию в указанный сезон '''
    try:
        form = AddSerieForm(request.POST)
        print(request.POST)
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
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(username=cd['username'])
            return auth1(request, url)
        return HttpResponse(str(form))
    else:
        return HttpResponseRedirect('/%s' % url)


@require_http_methods(['POST', 'GET'])
def log_out(request, url):
    logout(request)
    if 'profile' in url:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/' + url)


class AddProduct(LoginRequiredMixin, BasePageMixin, CreateView):
    template_name = 'forms/add_form.html'
    model = Production
    form_class = AddForm    

    def get_success_url(self):
        try:
            p = Production.objects.last()
            Types[self.kwargs['category']].objects.create(link=p)
            return '/%s/' % self.kwargs['category']
        except Exception as e:
            logger.error(e)
            raise
    
    def get_context_data(self, **kwargs):
        context = super(AddProduct, self).get_context_data(**kwargs)

        context['genres'] = Genre.objects.all()
        context['header'] = 'Create new %s' % self.kwargs.get('category')
        context['raiting'] = Raiting.objects.all()

        return context


@require_http_methods(['GET'])
def production_series_view(request, category, pk):
    try:
        result = {}
        result['nav_groups'] = ThematicGroup.objects.all()
        return render(request, 'series.html', result)
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError()


@require_http_methods(['GET'])
def seasons_view(request, category, pk):
    '''
    Сериализует в json список серий, сгруппированных по сезонам, с учетом
    прав пользователя (модераторы пока не)
    Формат: {'number': <int>, 'name': <str>, 'series': [{
        'number': <int>, 'name': <str>, 'start_date': <date_time>,
        'length': <int>
    }]}'''
    try:
        js = []
        listed = []
        queryset = Serie.objects.filter(product=pk)
        seasons = queryset.aggregate(Max('num_season'))

        # Получаем список серий, просмотренных текущим юзером
        if seasons['num_season__max'] and request.user.is_authenticated():
            listed = [i.id for item in
                ListedProduct.objects.filter(user=request.user, product=pk)
                for i in item.series.all()]
        
        # "Обходим" по сезонам список серий
        for season in range(1, (seasons['num_season__max'] or 0) + 1):
            series = queryset.filter(num_season=season)
            item = []
            for i, serie in enumerate(series):
                tmp = {'name': serie.name, 'number': serie.number,
                    'start_date': str(serie.start_date or '-'),
                    'length': serie.length
                    }
                if request.user.is_authenticated():
                    if serie.id in listed:
                        tmp['listed'] = 'Remove from list'
                    else:
                        tmp['listed'] = 'Add to list'
                    tmp['imgUrl'] = '/static/img/edit.png'
                item.append(tmp)
            js.append({'number': season, 'series': item})

        return HttpResponse(
            json.dumps(js[::-1], ensure_ascii=False),
            content_type='application/json')
    
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError()


class ProductionChoiceView(BaseChoiceMixin, ListView):
    model = Production
    template_name = 'list.html'
    header = 'Выборка манги по жанрам'
    category = 'Manga'
    genre_groups =\
        ['Anime Male', 'Anime Female', 'Anime School', 'Standart', 'Anime Porn']
    model1 = Manga
