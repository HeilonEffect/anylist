import functools
import json
import operator

from django.db.models import Q
from django.http import HttpResponse

from rest_framework import generics, status
from rest_framework.permissions import (
    IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class CategoriesList(generics.ListAPIView):

    ''' Список разделов сайта '''
    model = Category
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
        ''' Создаёт новый "продукт". Для создания необходимо указать им
        занимаемый раздел, название (должно быть уникальным), описание
        (опционально), аватар,  '''
        data = json.loads(request.DATA['data'])
        serializer = ProductSerializer(data=data, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data,
                                status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        '''
        Выборка "продуктов" по указанным пользователем параметрам в том числе
        Параметры: жанры - если укзать несколько, то выборка будет тех жанров,
        что удовлетворяют всем условиям
        возрастное ограничение - если указать несколько, то будут выбраны все
        продукты, которые удовлетворяют хотя-бы одному условию
        '''
        result = Product.objects.all()
        category = self.request.QUERY_PARAMS.get('category')
        genres = self.request.QUERY_PARAMS.get('genres')
        if genres and ',' in genres:
            genres = genres.split(',')
        elif genres:
            genres = [genres]
        raitings = self.request.QUERY_PARAMS.get('old_limit')
        if raitings and ',' in raitings:
            raitings = raitings.split(',')
        elif raitings:
            raitings = [raitings]
        if category:
            result = result.filter(category=category)
        if raitings:
            query_set = functools.reduce(operator.or_,
                                         map(lambda item: Q(
                                             old_limit__name=item), raitings))
            result = result.filter(query_set)
        if genres:
            for genre in genres:
                result = result.filter(genres__name=genre)
        return result


class RaitingList(generics.ListAPIView):
    model = Raiting
    serializer_class = RaitingSerializer
    permission_classes = (AllowAny,)


class GenreGroupList(generics.ListAPIView):
    queryset = GenreGroup.objects.all()
    serializer_class = GenreGroupSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        ''' Если указана id категории, то '''
        result = GenreGroup.objects.all()
        category_id = self.request.QUERY_PARAMS.get('category')
        if category_id:
            result = result.filter(
                category=Category.objects.get(id=category_id).group)
        return result


class ProductDetail(generics.RetrieveUpdateAPIView):

    ''' Одиночный продукт '''
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
        d = {'id': a.id, 'product': a.product.id,
             'name': a.name, 'number': a.number}
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

    ''' Действия со списком пользователей '''
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
        return result

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
        ''' Получаем список серий '''
        result = self.model.objects.all()
        if self.request.user:
            result = result.filter(user_list__user=self.request.user)
        product = self.request.QUERY_PARAMS.get('product')
        if product:
            result = result.filter(user_list__product__id=product)
        return result

    def post(self, request, *args, **kwargs):
        ''' Добавление единичной серии в список просмотренных '''
        cd = {'serie': request.DATA['serie'], 'like': None}
        cd['user_list'] = UserList.manager.get_or_create(
            user=request.user, product__id=request.DATA['product'])[0].id

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


class SearchHeroView(generics.ListAPIView):
    model = Hero
    serializer_class = SearchHeroSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.model.objects.filter(
            Q(name__icontains=self.request.QUERY_PARAMS['hero']))[:10]


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
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


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
        avatar = request.FILES.get('avatar')
        if avatar and request.DATA['name']:
            serializer = CreatorSerializer(data=request.DATA,
                                           files=request.FILES)
            if serializer.is_valid():
                try:
                    p = serializer.save()

                    employ = Employ.objects.get(id=request.DATA['employ'])
                    c = CreatorEmploys.objects.get_or_create(
                        employ=employ, creator=p)

                    Product.objects.get(
                        id=request.DATA['product']).creators.add(c[0])
                    return JSONResponse(serializer.data,
                                        status=status.HTTP_201_CREATED)
                except Exception as e:
                    print(e)
                    return Response('', status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        # return Response('', status=status.HTTP_200_OK)


class HeroView(generics.ListCreateAPIView):
    model = Hero
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = HeroSerializer

    def get_queryset(self):
        result = self.model.objects.all()
        product = self.request.QUERY_PARAMS.get('product')
        if product:
            result = Product.objects.get(id=product).heroes.all()
            # result = result.filter(id=product)
        return result

    def post(self, request, *args, **kwargs):
        ''' Добавление нового персонажа с существующим актёром '''
        serializer = self.serializer_class(data=request.DATA,
                                           files=request.FILES)
        if serializer.is_valid():
            p = serializer.save()
            Product.objects.get(id=request.DATA['product']).heroes.add(p)
            return JSONResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class EmployView(generics.ListAPIView):
    model = Employ
    serializer_class = EmploySerializer
    permission_classes = (AllowAny,)


class ProductCreator(APIView):

    '''
    Привязывает/отвязывает лиц, связанных с созданием продукта
    к продукту. Предназначен для уже созданных персонажей. Если
    персонажи ещё не созданы, то следует воспользоваться CreatorView
    '''
    model = Product
    permission_classes = (IsAuthenticated,)
    serializer_class = CreatorSerializer

    def post(self, request, *args, **kwargs):
        creator = Creator.objects.get(id=int(request.DATA['id']))
        employ = Employ.objects.get(id=request.DATA['employ'])
        c = CreatorEmploys.objects.get_or_create(creator=creator,
                                                 employ=employ)
        Product.objects.get(id=kwargs['pk']).creators.add(c[0])
        serialize = CreatorSerializer(data=creator)
        return Response(serialize.data, status=status.HTTP_200_OK)


class SeriesCount(generics.UpdateAPIView):

    ''' Отмечает/удаляет серии, если известно только их новое число.
    Если серий отмечено больше, чем от самой последней просмотренной до конца,
    то излишек будет проигнорирован '''
    model = SerieList
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        number = int(request.DATA['series'])
        product = Product.objects.get(id=kwargs['pk'])
        user_list = UserList.manager.get_or_create(user=request.user,
                                                   product=product)[0]
        watched_series = SerieList.manager.watched_series(user=request.user,
                                                          product=product)
        if not watched_series:
            series = Serie.manager.all_series(product).reverse()[:number]
            for serie in series:
                user_list.add_watched_serie(serie=serie, like=None)

        elif number > watched_series.count():
            p = Serie.objects.filter(id__gt=watched_series.first().serie.id
                                     )[:number - watched_series.count(
                                     )].reverse()
            for serie in p:
                user_list.add_watched_serie(serie=serie, like=None)

        elif number < watched_series.count():
            ids = list(map(lambda item: item.id,
                           watched_series[:watched_series.count() - number]))
            SerieList.objects.filter(id__in=ids).delete()

        return Response('', status=status.HTTP_200_OK)


class CreatorDetailView(generics.RetrieveUpdateAPIView):
    model = Creator
    serializer_class = CreatorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class HeroDetailView(generics.RetrieveUpdateAPIView):
    model = Hero
    serializer_class = HeroSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
