import functools
import operator

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed

from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    CategoryGroup,
    Product,
    Category,
    Genre,
    Raiting,
    GenreGroup,
    UserList,
    Serie
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    RaitingSerializer,
    GenreGroupSerializer,
    UsersSerializer,
    UserListSerializer,
    SeriesSerializer,
    GenreSerializer
)


class CategoriesList(generics.ListAPIView):
    model = CategoryGroup
    serializer_class = CategorySerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.DATA, files=request.FILES)
        print(request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
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


class GenreGroupList(generics.ListAPIView):
    queryset = GenreGroup.objects.all()
    serializer_class = GenreGroupSerializer

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
            content = { 'status': p.status.name}
            return Response(content)
        else:
            return HTTP_400_BAD_REQUEST()


class SeriesView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SeriesSerializer


class GenreView(generics.ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')