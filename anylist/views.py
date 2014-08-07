# -*- encoding: utf-8 -*-
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import *
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView

from myapp.forms import *

logger = logging.getLogger(__name__)


get_category = lambda self: ''.join(
    [self.kwargs['category'][0].upper(), self.kwargs['category'][1:]])


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


def serie_view(request, category, pk):
    return render(request, 'series.html')


def hero_view(request, pk):
    return render(request, 'hero.html')


def heroes_list(request, category, pk):
    return render(request, 'heroes_list.html')


def creator_view(request, pk):
    return render(request, 'creator.html')

def creators_list(request, category, pk):
    return render(request, 'creators_list.html')


def error404(request):
    context = {}
    context['nav_groups'] = CategoryGroup.objects.all()
    return render(request, 'error.html', context)
