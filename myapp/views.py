import functools
import operator

from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed

from rest_framework import generics

from .models import (
    CategoryGroup,
    Product,
    Category,
    Genre,
    Raiting,
    GenreGroup)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    RaitingSerializer,
    GenreGroupSerializer
)


class CategoriesList(generics.ListAPIView):
    model = CategoryGroup
    serializer_class = CategorySerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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
