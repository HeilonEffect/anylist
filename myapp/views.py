import functools
import json
import operator

from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

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
                        if not isinstance(q, list):
                            p = p.filter(q)

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
        result = GenreGroup.objects.all()
        category = self.request.QUERY_PARAMS.get('category')
        if category:
            result = result.filter(category=category)
        genres = self.request.QUERY_PARAMS.get('genres', None)
        res = {}
        if genres:
            p = Product.objects.all()
            for genre in genres.split(','):
                p = p.filter(genres__name=genre)
            if category:
                p = p.filter(category=category)
            counter = [genre['name'] for item in p for genre in item.genres.values('name')]
            for genre in counter:
                if genre in res:
                    res[genre] += 1
                else:
                    res[genre] = 1
        # Добавить в вывод
        for group in result:
            for genre in group.genres.all():
                genre.count = res.get(genre.name, 0)
        return result


class ProductDetail(generics.RetrieveUpdateAPIView):
    model = Product
    serializer_class = ProductSerializer

    def put(self, request, *args, **kwargs):
        ''' Обновляет информацию о продукте '''
        data = json.loads(request.DATA['data'])
        id = data['id']
        if request.FILES:
            data['avatar'] = request.FILES['avatar']
        p = Product.objects.get(id=data['id'])
        p.avatar = request.FILES['avatar']
        if p.title != data['title']:
            p.title = data['title']
        if p.description != data['description']:
            p.description = data['description']
        if p.old_limit.id != data['old_limit']:
            p.old_limit = Raiting.objects.get(id=data['old_limit'])
        genres = p.genres.all()
        p.genres.clear()
        for genre in data['genres']:
            g = Genre.objects.get(id=genre)
            p.genres.add(g)
        p.save()
        return Response('', status=status.HTTP_200_OK)


class User(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(content)


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
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserListSerializer
    model = UserList
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        product = self.request.QUERY_PARAMS.get('product')
        category = self.request.QUERY_PARAMS.get('category')
        status = self.request.QUERY_PARAMS.get('status')
        result = self.model.objects.all()
        if category:
            for item in Category.objects.all():
                if item.get_absolute_url()[1:-1] == category:
                    category = item
            result = result.filter(user=self.request.user,
                                             product__category=category)
        if product:
            result = result.filter(product=product, user=self.request.user)
        if status:
            result = result.filter(status=status)
        return  result

    def post(self, request, *args, **kwargs):
        ''' Обрабатывает такие случаи, как
            - добавить в список
            - оценить (пока не обрабатывает)
        '''
        data = {}
        data['product'] = request.DATA.get('product')
        data['status'] = request.DATA.get('status')
        data['user'] = request.user.id
        # serializer = UsersSerializer(data=data)
        serializer = UsersSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListUpdate(generics.RetrieveUpdateDestroyAPIView):
    ''' Одиночные действия со списком продуктов:
     - добавить в список
     - обновить статус '''
    model = UserList
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        ''' Обновляет статус продукта '''
        st = Status.objects.get(name=request.DATA['name'])
        p = UserList.objects.get(product__id=kwargs['id'],
                                user=request.user)
        p.status = st
        p.save()
        return Response('', status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        ''' Добавляет продукт в список просмотренного '''
        st = Status.objects.get(name=request.DATA['name'])
        product = Product.objects.get(id=kwargs['id'])
        p = UserList.objects.create(product=product, status=st,
                                    user=request.user)
        serializer = self.serializer_class(p)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SerieListView(generics.ListCreateAPIView):
    ''' Действия со списоком серий (с множеством объектов) '''
    model = SerieList
    serializer_class = SerieListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user:
            return self.model.objects.filter(user_list__user=self.request.user)
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        ''' Добавление серии в список просмотренных '''
        cd = {'serie': request.DATA['serie'], 'like': None}
        try:
            user_list = UserList.objects.get(
                user=request.user, product__id=request.DATA['product'])
            cd['user_list'] = user_list.id
        except Exception as e:
            p = Product.objects.get(id=request.DATA['product'])
            st = Status.objects.get(name='Watch')
            user_list = UserList.objects.create(
                user=request.user, product=p, status=st
            )
            cd['user_list'] = user_list.id
        serializer = self.serializer_class(data=cd)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('', status=status.HTTP_400_BAD_REQUEST)


class SearchView(generics.ListAPIView):
    model = Product
    serializer_class = SearchSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Product.objects.filter(
            Q(title__icontains=self.request.QUERY_PARAMS['product']))[:10]


class SearchCreatorView(generics.ListAPIView):
    model = Creator
    serializer_class = SearchCreatorSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Creator.objects.filter(
            Q(name__icontains=self.request.QUERY_PARAMS['creator']))[:10]


class SingleSerieListView(generics.RetrieveUpdateDestroyAPIView):
    ''' Действия над единичным объектом из списка серий, отмеченных юзером '''
    model = SerieList
    serializer_class = SerieListSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        self.model.objects.filter(serie__id=kwargs['id']).delete()
        return Response('', status=status.HTTP_204_NO_CONTENT)


class SingleSerieView(generics.RetrieveUpdateAPIView):
    model = Serie
    serializer_class = SeriesSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        ''' Обновление содержимого серии '''
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            del serializer.data['id']
            Serie.objects.filter(id=kwargs['id']).update(**serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserStatistic(APIView):
    ''' Отображает сколько произведений на какой стадии у пользователя '''
    model = Product
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        p = UserList.objects.filter(user=self.request.user)
        result = {}
        categories = Category.objects.all()
        statuses = Status.objects.all()
        for category in categories:
            result[category.name] = {'items': [], 'count': 0,
                                     'name': category.name}
            for status in statuses:
                tmp = {'status': status.name}
                tmp['count'] = p.filter(product__category=category,
                                        status=status).count()
                tmp['url'] = r'/profile/list/%s/%s' % (
                    category.name.lower().replace(' ', ''),
                    status.name.lower())
                result[category.name]['items'].append(tmp)
                result[category.name]['count'] += tmp['count']
        return Response(result)


class CreatorView(generics.ListCreateAPIView):
    model = CreatorEmploys
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CreatorEmploysSerializer

    def get_queryset(self):
        result = self.model.objects.all()
        product = self.request.QUERY_PARAMS.get('product')
        if product:
            result = Product.objects.get(id=product).creators.all()
        return result

    def post(self, request, *args, **kwargs):
        '''
        Если есть имя нового персонажа и аватар - то сохраняем
        персонажа и добавляем его в список причастных к продукту.
        Если передаём id персонажа, id продукта и id специальности, то
        ищем, либо создаём запись в таблице и добавляем запись
        в список причастных
        '''
        print(request.DATA)
        avatar = request.FILES.get('avatar')
        if avatar and request.DATA['name']:
            serializer = CreatorSerializer(data=request.DATA,
                                           files=request.FILES)
            if serializer.is_valid():
                try:
                    p = serializer.save()
                    e = Employ.objects.get(id=request.DATA['employ'])
                    c = CreatorEmploys.objects.get_or_create(employ=e, creator=p)
                    Product.objects.get(id=request.DATA['product']).creators.add(c[0])
                    return Response('', status=status.HTTP_201_CREATED)
                except Exception as e:
                    print(e)
                    return Response('', status=status.HTTP_200_OK)
            else:
                return Response('', status=status.HTTP_400_BAD_REQUEST)
        return Response('', status=status.HTTP_200_OK)


class HeroView(generics.ListCreateAPIView):
    model = Hero
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = HeroSerializer

    def get_queryset(self):
        result = self.model.objects.all()
        product = self.request.QUERY_PARAMS.get('product')
        if product:
            result = result.filter(id=product)
        return result

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployView(generics.ListAPIView):
    model = Employ
    serializer_class = EmploySerializer
    permission_classes = (AllowAny,)


class UpdateNumSeriveView(APIView):
    ''' Если мы указываем, что мы просмотрли N серий, то данные об этом
     шлются сюда'''
    def post(self, request, *args, **kwargs):
        pass


class ProductCreator(APIView):
    '''
    Привязывает/отвязывает лиц, связанных с созданием продукта
    к продукту. Предназначен для уже созданных персонажей. Если
    персонажи ещё не созданы, то следует воспользоваться CreatorView
    '''
    model = Product
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        c = CreatorEmploys.objects.get(creator=request.DATA['id'],
                                       employ=request.DATA['employ'])
        Product.objects.get(id=kwargs['pk']).creators.add(c)
        return Response('', status=status.HTTP_200_OK)