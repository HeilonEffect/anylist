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
    return render(request, 'profile.html')


def mylist(request, category, status):
    return render(request, 'user_list.html')


def product_list(request, category):
    context = {'category': category, 'header': 'List of %s' % category}
    return render(request, 'list.html', context)


class ProductDetail(DetailView):

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

#
# @require_http_methods(['POST', 'GET'])
# def register(request, url):
#     if request.POST:
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = User.objects.create_user(**cd)
#             user.save()
#             return auth1(request, url)
#         return HttpResponse(str(form))
#     else:
#         return HttpResponseRedirect('/%s' % url)


@require_http_methods(['POST'])
def register(request):
    ''' Регистрация нового пользователя '''
    form = RegisterForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = User.objects.create_user(**cd)
        user.save()
        token = Token.objects.create(user=user)
        return HttpResponse({'token': token, 'username': user.username},
                            content_type='application/json')
    return HttpResponse(form.errors)


def add_product(request, category):
    context = {'category': category, 'header': 'Add new %s' % category}
    return render(request, 'forms/add_form.html', context)


def serie_view(request, category, pk):
    return render(request, 'series.html')


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
