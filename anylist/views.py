# -*- encoding: utf-8 -*-
import logging.config

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView

from rest_framework.authtoken.models import Token

from myapp.models import Product

from .dicLog import LOGGING

logger = logging.config.dictConfig(LOGGING)

get_category = lambda self: ''.join(
    [self.kwargs['category'][0].upper(), self.kwargs['category'][1:]])

def partials(request, path):
    ''' Подгружает шаблоны '''
    result = path
    if '/' in path:
        result = path.split('/')[-1]
    return HttpResponse(open('anylist/templates/%s.html' % result).read())

def main_page(request):
    return HttpResponse(open('anylist/templates/base.html').read())


# @require_http_methods(['POST'])
# def register(request):
#     ''' Регистрация нового пользователя '''
#     form = RegisterForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         user = User.objects.create_user(**cd)
#         user.save()
#         token = Token.objects.create(user=user)
#         return HttpResponse({'token': token, 'username': user.username},
#                             content_type='application/json')
#     return HttpResponse(form.errors)


# def error404(request):
#     context = {}
#     context['nav_groups'] = CategoryGroup.objects.all()
#     return render(request, 'error.html', context)
