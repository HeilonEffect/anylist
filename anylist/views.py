# -*- encoding: utf-8 -*-
import json
import logging.config

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from myapp.forms import RegisterForm

from rest_framework.authtoken.models import Token


from .dicLog import LOGGING

logger = logging.config.dictConfig(LOGGING)

get_category = lambda self: ''.join(
    [self.kwargs['category'][0].upper(), self.kwargs['category'][1:]])

def partials(request, path):
    ''' Подгружает шаблоны '''
    result = path
    if '/' in path:
        result = path.split('/')[-1]
    return render_to_response('%s.html' % result)

def main_page(request):
    return render_to_response('base.html')


@require_http_methods(['POST'])
@csrf_exempt
def register(request):
    ''' Регистрация нового пользователя '''
    print(request.POST)
    form = RegisterForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = User.objects.create_user(**cd)
        token = Token.objects.get(user=user)
        return HttpResponse(json.dumps({'token': token.key,
                             'username': cd['username']}),
                            content_type='application/json')
    return HttpResponse(form.errors)


def error404(request):
    return HttpResponse(open('anylist/templates/error.html').read())
