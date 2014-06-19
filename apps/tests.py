from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.test import TestCase
from django.test.client import Client, RequestFactory

from selenium import webdriver

from .models import *
from anylist.views import *

Types = {'anime': Anime, 'manga': Manga}


class HomePageTest(TestCase):
	def test_get_page(self):
		'Тестируем доступность главной страницы'
		request = RequestFactory().get('/')
		view = MainPage.as_view()

		response = view(request)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')

#	def test_register(self):
#		request = RequestFactory().post('/register')


class CategoryPageTest(TestCase):
	def test_get_category_page(self):
		''' Проверка, что все списки с различными категориями либо доступны,
		либо выдаётся стандартная 404 ошибка '''
		categories = Category.objects.all()
		for category in categories:
			request = RequestFactory().get('/%s/' % category.get_absolute_url())
			view = ProductionList.as_view()

			response = view(request)

			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'list.html')
		request = RequestFactory().get('/yob/')
		view = ProductionList.as_view()

		response = view(request)
		self.assertEqual(response.status_code, 404)


class DetailPageTest(TestCase):
	def test_get_anime_page(self):
		view = ProductDetail.as_view()
		for item in Anime.objects.all():
			request = RequestFactory().get('/anime/%s/' % item.link.get_absolute_url())

			response = view(request)

			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'detail.html')

		request = RequestFactory().get('/anime/yob')
		response = view(request)

		self.assertEqual(response.status_code, 404)


	def test_get_manga_page(self):
		view = ProductDetail.as_view()
		for item in Manga.objects.all():
			request = RequestFactory().get('/manga/%s/' % item.link.get_absolute_url())

			response = view(request)

			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'detail.html')

		request = RequestFactory().get('/manga/yob')
		response = view(request)

		self.assertEqual(response.status_code, 404)


class AddProductPageTest(TestCase):

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='jacob', email='jacob@_',
			password='top_secret')
		self.view = AddProduct.as_view()


#	def test_get_add_product(self):
#		''' Доступность странички для добавления нового продукта
#		для зарегестрированных пользователей '''
#		view = AddProduct.as_view()
#		for category in Types:
#			request = self.factory.get('/%s/add' % category)
#			#request.user = User.objects.get(id=1)
#
#			self.assertTrue(self.user.is_authenticated())
#			user = authenticate(username='jacob', password='top_secret')
#			#login(request, user)
#			request.user = user
#
#			response = view(request)
#
#			self.assertEqual(response.status_code, 200)
#			self.assertEqual(response.template_name[0], 'forms/add_form.html')
#
#
	def test_get_add_product_unregister(self):
		''' Недоступность страницы для добавления нового продукта для
		незарегистрированных пользователей '''
		for category in Types:
			request = self.factory.get('/%s/add' % category)
			request.user = User.objects.get(id=1)
			response = self.view(request)
			self.assertEqual(response.status_code, 404)


	def test_get_not_exits_product(self):
		''' Страничка для добавления продукта несуществующей категории '''
		view = AddProduct.as_view()
		request = RequestFactory().get('yob/add')
		request.user = User.objects.get(id=1)

		response = view(request)

		self.assertEqual(response.status_code, 404)


