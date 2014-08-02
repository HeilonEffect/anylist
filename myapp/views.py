import functools
import json
import operator

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed

from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AddProductForm

from .models import *

from .serializers import *


class CategoriesList(generics.ListAPIView):
    ''' Список разделов сайта '''
    model = CategoryGroup
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class ProductList(generics.ListCreateAPIView):
    '''
    Список медийных продуктов, читать могут все, править -
     зарегестрированные пользователи
     '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def post(self, request, *args, **kwargs):
        data = json.loads(request.DATA['data'])
        serializer = ProductSerializer(data=data, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        '''
        Если передавался параметр <name> - произойдет фильтрация по указанной
        в <name> категории.
        Если передавался параметр <args> - произойдет сложная выборка по
        куче параметров, определенных пользователем
        Во всех остальных случаях - вернёт все объекты
        Формат url'a при <args>:
        filter/old_limit/<limit1>,<limit2>/genres/<genre1>,<genre2>/
        '''
        if 'name' in self.kwargs:
            for item in Category.objects.all():
                if item.get_absolute_url()[1:-1] == self.kwargs['name']:
                    p = Product.objects.filter(category__name=item.name)

                    if 'args' in self.kwargs:
                        print('args in self.kwargs')
                        qs = {}
                        tmp = self.kwargs['args'].split('/')
                        tmp = list(filter(lambda item: item, tmp))

                        qs = dict(zip(
                            tmp[::2], [item.split(',') for item in tmp[1::2]]))

                        q = []
                        f = lambda item: Q(old_limit__name=item)
                        tmp = qs.get('old_limit')
                        if tmp:
                            q = functools.reduce(operator.or_, map(f, tmp))
                        print(q)
                        if not isinstance(q, list):
                            p = p.filter(q)
                            print(p)

                        tmp = qs.get('genres')
                        if tmp:
                            for item in tmp:
                                p = p.filter(genres__name=item)
                    return p
            return Product.objects.all()
        else:
            return Product.objects.all()


class RaitingList(generics.ListAPIView):
    model = Raiting
    serializer_class = RaitingSerializer
    permission_classes = (AllowAny,)


class GenreGroupList(generics.ListAPIView):
    queryset = GenreGroup.objects.all()
    serializer_class = GenreGroupSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        if 'name' in self.kwargs:
            for item in Category.objects.all():
                if item.get_absolute_url()[1:-1] == self.kwargs['name']:
                    return GenreGroup.objects.filter(category=item.group)
        else:
            return GenreGroup.objects.all()


class ProductDetail(generics.RetrieveUpdateAPIView):
    model = Product
    serializer_class = ProductSerializer


class User(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(content)


class StatusView(generics.GenericAPIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = (UsersSerializer,)

    def get(self, request, pk):
        p = UserList.objects.filter(user=request.user,
                                    product__id=pk).first()
        if p:
            content = {'status': p.status.name}
            return Response(content)
        else:
            return Response('', status=status.HTTP_400_BAD_REQUEST)


class GenreView(generics.ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')


class SeasonsView(generics.ListCreateAPIView):
    serializer_class = SeasonsSerializer
    model = SeriesGroup
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        ''' Создание нового "сезона" '''
        product = request.DATA['product']
        num_season = self.model.objects.filter(
            product__id=product).count() + 1
        a = self.model.objects.create(number=num_season,
                                  product=Product.objects.get(id=product))
        d = {'id': a.id, 'product': a.product.id, 'name': a.name, 'number': a.number}
        serializer = self.serializer_class(data=d)
        if serializer.is_valid():
            return Response(serializer.data, status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if 'product' in self.request.GET:
            return self.model.objects.filter(
                product=self.request.GET['product'])
        else:
            return self.model.objects.all()


class SeriesView(generics.ListCreateAPIView):
    serializer_class = SeriesSerializer
    model = Serie
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        serializer = SeriesSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserListSerializer
    model = UserList
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        product = self.request.QUERY_PARAMS.get('product')
        category = self.request.QUERY_PARAMS.get('category')
        if category:
            for item in Category.objects.all():
                if item.get_absolute_url()[1:-1] ==\
                        self.request.QUERY_PARAMS['category']:
                    category = item
            return self.model.objects.filter(user=self.request.user,
                                             product__category=category)
        elif product:
            return  self.model.objects.filter(product=product, user=self.request.user)
        else:
            return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        ''' Обрабатывает такие случаи, как
            - добавить в список
            - оценить
        '''
        data = {}
        data['product'] = request.DATA.get('product')
        data['status'] = request.DATA.get('status')
        data['user'] = request.user.id
        # serializer = UsersSerializer(data=data)
        serializer = UsersSerializer(data=request.DATA)
        if serializer.is_valid():
            print(serializer.DATA)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListUpdate(generics.RetrieveUpdateDestroyAPIView):
    ''' Одиночные действия со списком продуктов '''
    model = UserList
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        ''' Обновляет статус продукта
        (если продукта в списке нет - добавляет) '''
        st = Status.objects.get(name=request.DATA['name'])
        p = UserList.objects.get(product__id=kwargs['id'],
                                user=request.user)
        p.status = st
        p.save()
        return Response('', status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        st = Status.objects.get(name=request.DATA['name'])
        product = Product.objects.get(id=kwargs['id'])
        UserList.objects.create(product=product, status=st, user=request.user)
        return Response('', status=status.HTTP_201_CREATED)


class SerieListView(APIView):
    model = SerieList
    serializer_class = SerieListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.all()