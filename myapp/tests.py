import json
import os
import random

from django.test import TestCase

from rest_framework.test import APIRequestFactory, APIClient
from django_dynamic_fixture import G

from .views import *
from anylist.settings import MEDIA_ROOT


class SmokeTestsPages(TestCase):

    '''
    Проверяем базовую работоспособность функций, типа - на каждый корректный
    запрос получен корректный код и какие-то данные
    '''

    def setUp(self):
        user = User.objects.create_user(username='first', password='123456')
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.token = Token.objects.get_or_create(user=user)[0]
        self.category_view = CategoriesList.as_view()

    def test_main_page_available(self):
        '''
        Проверка доступности главной страницы
        '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_list_product_page_available(self):
        '''
        Проверка доступности страницы со списком продуктов
        '''
        category = G(Category)
        response = self.client.get('/#!/%s' % category.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_product_pages_available(self):
        '''
        Проверка доступности страницы с детальным описанием продукта
        '''
        category = G(Category)
        product = G(Product, category=category)
        response = self.client.get('/#!%s' % product.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/#!%s/series' % product.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/#!%s/creators' % product.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/#!%s/heroes' % product.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_profile_available(self):
        '''
        Проверка доступности страницы с профилем пользователя
        '''
        response = self.client.get('/#!/profile')
        self.assertEqual(response.status_code, 200)


class SmokeTestsAPI(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='first',
                                             password='123456')
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.token = Token.objects.get_or_create(user=self.user)[0]

    def test_get_categories(self):
        ''' Проверка доступности разделов '''
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertTrue(isinstance(response.data['results'], list))

        response = self.client.get('/api/categories')
        self.assertEqual(response.status_code, 301)

        response = self.client.post('/api/categories/')
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/api/categories/')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete('/api/categories/')
        self.assertEqual(response.status_code, 405)

    def test_content_header(self):
        '''
        В списке разделов содержатся добавленные туда данные
        '''
        group = G(CategoryGroup)
        cat1 = G(Category, group=group)
        cat2 = G(Category, group=group)
        response = self.client.get('/api/categories/')
        result = list(map(lambda item: item['id'], response.data['results']))
        self.assertIn(cat1.id, result)
        self.assertIn(cat2.id, result)

    def test_search_product_available(self):
        '''
        Запрос поиска возвращает корректный ответ
        '''
        product = G(Product)
        response = self.client.get('/api/search?product=%s' % product.title)
        self.assertEqual(response.status_code, 200)

    def test_data_search_product(self):
        '''
        Проверка корректности выдачи данных поиска по продукции
        '''
        product = G(Product)
        response = self.client.get('/api/search?product=%s' % product.title)
        result = map(lambda item: item['name'], response.data['results'])
        self.assertIn(product.title, result)
        result = map(lambda item: item['link'], response.data['results'])
        self.assertIn(product.get_absolute_url(), result)

    def test_data_product_available(self):
        '''
        Проверяет, что единичный продукт доступен через API
        '''
        category = G(Category)
        product = G(Product, category=category)
        response = self.client.get('/api/products/id:%d' % product.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(product.id, response.data['id'])

    def test_data_product_list_available(self):
        '''
        Проверяет, что список продуктов доступен через API
        '''
        category1 = G(Category)
        product1 = G(Product, category=category1)

        category2 = G(Category)
        product2 = G(Product, category=category2)
        product3 = G(Product, category=category2)

        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)

        result = list(map(lambda item: item['id'], response.data['results']))
        self.assertIn(product1.id, result)
        self.assertIn(product2.id, result)
        self.assertIn(product3.id, result)

        response = self.client.get('/api/products?category=%d' % category2.id)
        self.assertEqual(response.status_code, 200)

        result = list(map(lambda item: item['id'], response.data['results']))
        self.assertNotIn(product1.id, result)
        self.assertIn(product2.id, result)
        self.assertIn(product3.id, result)

    def test_user_list_available(self):
        '''
        Проверяет доступность списка пользователя
        '''
        category = G(Category)
        product = G(Product, category=category)
        status = G(Status)
        user_list = G(UserList, user=self.user, product=product,
                      status=status)

        response = self.client.get('/api/userlist')
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/userlist')
        self.assertEqual(response.status_code, 200)

        result = list(map(lambda item: item['id'], response.data['results']))
        self.assertIn(user_list.id, result)

        response = self.client.get('/api/userlist?category=%d&status=%d' % (
            category.id, status.id))
        self.assertEqual(response.status_code, 200)

        result = list(map(lambda item: item['id'], response.data['results']))
        self.assertIn(user_list.id, result)
        self.client.credentials()

    def test_product_series(self):
        '''
        Проверяем доступность серий для конкретного продукта, а также
        корректность формата полученных данных
        '''
        product = G(Product)
        season = G(SeriesGroup, product=product)
        serie = G(Serie, season=season)

        response = self.client.get('/api/seasons')
        self.assertEqual(response.status_code, 200)

        series = list(map(
            lambda item: item['id'], list(map(
                lambda item: item['series'], response.data['results']))[0]))
        self.assertIn(serie.id, series)

        response = self.client.get('/api/seasons?product=%d' % product.id)
        self.assertEqual(response.status_code, 200)

        series = list(map(
            lambda item: item['id'], list(map(
                lambda item: item['series'], response.data['results']))[0]))
        self.assertIn(serie.id, series)

    def test_product_creators(self):
        '''
        Проверяем доступность и соответсвие формату служебных персонажей
        '''
        creator = G(Creator)
        employ = G(Employ)
        ce = G(CreatorEmploys, creator=creator, employ=employ)
        product = G(Product)
        product.creators.add(ce)

        response = self.client.get('/api/creators?product=%d' % product.id)
        self.assertEqual(response.status_code, 200)
        urls = list(map(lambda item: item['url'], response.data['results']))

        response = self.client.get('/api/creators')
        self.assertEqual(response.status_code, 200)
        # Т.к. у нас только один creator, то первые элементы должны быть
        # идентичны
        self.assertEqual(list(map(
            lambda item: item['url'], response.data['results']))[0], urls[0])

        response = self.client.get('/#!%s' % urls[0])
        self.assertEqual(response.status_code, 200)

    def test_product_heroes(self):
        '''
        Доступность действующих лиц произведения
        '''
        hero = G(Hero)
        product = G(Product)
        product.heroes.add(hero)

        response = self.client.get('/api/heroes?product=%d' % product.id)
        self.assertEqual(response.status_code, 200)

        urls = list(map(lambda item: item['url'], response.data['results']))

        response = self.client.get('/#!' + urls[0])
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/heroes')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(urls[0], list(map(lambda item: item['url'],
                                           response.data['results']))[0])

    def test_limits(self):
        '''
        Доступность возрастных ограничений
        '''
        limit = G(Raiting)
        response = self.client.get('/api/raitings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(limit.id, response.data['results'][0]['id'])

    def test_products(self):
        '''
        Тестирование фильтров на разные продукты
        '''
        genre1 = G(Genre)
        genre2 = G(Genre)
        genre3 = G(Genre)

        limit1 = G(Raiting)
        limit2 = G(Raiting)

        product1 = G(Product)
        product2 = G(Product)

        product1.genres.add(genre1)
        product1.genres.add(genre2)
        product1.old_limit = limit1

        product2.genres.add(genre2)
        product2.genres.add(genre3)
        product1.old_limit = limit2

        response = self.client.get('/api/products?genres=%d&old_limit=%s' % (
            genre1.id, '%d,%d' % (limit1.id, limit2.id)))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/products?genres=%s&old_limit=%d' % (
            '%d,%d' % (genre1.id, genre2.id), limit1.id))
        self.assertEqual(response.status_code, 200)

    def test_genres(self):
        category = G(CategoryGroup)
        category1 = G(Category, season=category)

        genre1 = G(Genre)
        genre2 = G(Genre)
        genre3 = G(Genre)

        group = G(GenreGroup, category=category)
        group.genres.add(genre1)
        group.genres.add(genre2)

        response = self.client.get('/api/genres')
        self.assertEqual(response.status_code, 200)
        results = list(map(lambda item: item['id'],
                           response.data['results'][0]['genres']))
        self.assertIn(genre1.id, results)
        self.assertIn(genre2.id, results)

        # response = self.client.get('/api/genres?category=%d' % category.id)
        # self.assertEqual(response.status_code, 200)
        # print(response.data['results'])
        # results = list(map(lambda item: item['id'],
        #                    response.data['results'][0]['genres']))
        # self.assertIn(genre1.id, results)
        # self.assertIn(genre2.id, results)
        # self.assertNotIn(genre3.id, results)

    def test_product_detail(self):
        product = G(Product)

        response = self.client.get('/api/products/id:%d' % product.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], product.id)

    def test_user_statistic(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        category1 = G(Category)
        category2 = G(Category)

        status = G(Status)

        product1 = G(Product, category=category1)
        product2 = G(Product, category=category2)

        list1 = G(UserList, product=product1, status=status)

        response = self.client.get('/api/profile')
        self.assertEqual(response.status_code, 200)
        self.client.credentials()

    def test_add_product(self):
        category = G(Category)
        old_limit = G(Raiting)
        genre1 = G(Genre)
        genre2 = G(Genre)
        js = {'title': 'sda',
              'description': 'sasasasasas',
              'old_limit': old_limit.id,
              'genres': '%d,%d' % (genre1.id, genre2.id),
              'category': category.id}
        avatar = random.choice(os.listdir(MEDIA_ROOT))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/products',
            {'data': json.dumps(js)})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/products',
            {'data': json.dumps(js), 'avatar': avatar})
        print(response.content)

    # def test_add_creator(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     response = self.client.post('/api/creators', {'name': '12345'})
    #     self.assertEqual(response.status_code, 400)

    def test_search_hero(self):
        hero = G(Hero)
        response = self.client.get('/api/search_hero?hero=%s' % hero.name)
        self.assertEqual(response.status_code, 200)

        result = list(map(lambda item: item['name'],
            response.data['results']))
        self.assertIn(hero.name, result)
        
    def test_search_creator(self):
        creator = G(Creator)
        response = self.client.get(
            '/api/search_creator?creator=%s' % creator.name)
        self.assertEqual(response.status_code, 200)

        result = list(map(lambda item: item['name'],
            response.data['results']))
        self.assertIn(creator.name, result)

    def test_product_in_user_list(self):
        product1 = G(Product)
        product2 = G(Product)

        userlist = G(UserList, product=product1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
