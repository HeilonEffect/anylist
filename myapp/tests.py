from django.test import TestCase

from rest_framework.test import APIRequestFactory, APIClient
from django_dynamic_fixture import G

from .views import *

class TestHeader(TestCase):
    '''
    Проверяем работоспособность функций, доступной с каждой страницы:
    разделы, поиск, профиль
    '''
    def setUp(self):
        user = User.objects.create(username='first', password='123456')
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.token = Token.objects.create(user=user)
        self.category_view = CategoriesList.as_view()

    def test_get_categories(self):
        ''' Проверка доступности '''
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

        response = self.client.delete('/api/categories')
        self.assertEqual(response.status_code, 405)

    def test_content_header(self):
        '''
        В списке разделов содержатся добавленные туда данные
        '''
        group = G(CategoryGroup)
        cat1 = G(Category, group=group)
        cat2 = G(Category, group=group)
        response = self.client.get('/api/categories')
        result = list(map(lambda item: item.id, response.data['results']))
        self.assertIn(cat1.id, result)
        self.assertIn(cat2.id, result)


class TestAddDeleteSerie(TestCase):
    def setUp(self):
        self.product = G(Product)
        self.user_list = G(UserList, product=self.product)
        self.serie_group = G(SeriesGroup, product=self.product)
        self.serie = G(Product, season=self.serie_group)

    def test_add_watch_serie(self):
        pass