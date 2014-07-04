import json

from django.test import TestCase
from django.test.client import Client

from myapp.models import *


# Create your tests here.
class MainPageTest(TestCase):
	fixtures = ['category.json']
	
	def setUp(self):
		self.client = Client()
		self.userdata = {'username': 'first', 'password': 'ShockiNg'}
		User.objects.create_user(**self.userdata)
	

	def test_main_page_available(self):
		''' Главная страничка грузится '''
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')


	def test_main_page_content(self):
		''' На главной странице отображён необходимый нам контент '''
		response = self.client.get('/')
		statuses = Category.objects.all()
		self.assertEqual(len(response.context['object_list']), len(statuses))
		for i in range(len(statuses)):
			self.assertEqual(response.context['object_list'][i], statuses[i])


	def test_main_page_search_available(self):
		''' Поиск выдаёт json '''
		response = self.client.get('/search?key=bo')
		self.assertEqual(response.status_code, 200)
		js = json.loads(str(response.content, 'utf-8'))
		self.assertTrue(isinstance(js, dict))


	def test_login_logout_main_page(self):
		''' Правильный код ответа при попытках зайти/выйти '''
		response = self.client.post('/login/', self.userdata)
		self.assertEqual(response.status_code, 302)

		response = self.client.post('/logout/', {})
		self.assertEqual(response.status_code, 302)

		response = self.client.put('/login/', self.userdata)
		self.assertEqual(response.status_code, 405)


	def test_login_logout_functional(self):
		''' При попытках зайти/выйти - перенаправляется на правильный шаблон
		и имя пользователя отрисовывается '''
		response = self.client.post('/login/', self.userdata, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')
		self.assertIn(self.userdata['username'],
			str(response.content, 'utf-8'))

		response = self.client.post('/logout/', self.userdata, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')
		self.assertNotIn(self.userdata['username'],
			str(response.content, 'utf-8'))


class ListPageTest(TestCase):
	fixtures = ['category.json', 'product.json']

	def setUp(self):
		self.client = Client()
		self.userdata = {'username': 'first', 'password': 'ShockiNg'}
		User.objects.create_user(**self.userdata)

	def test_list_page_available(self):
		''' Содержимое страниц с контентом всегда доступно '''
		for item in Category.objects.all():
			response = self.client.get('/%s/' % item.name.lower())
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'list.html')

	def test_list_page_content(self):
		''' На соответсвующей категории со списками размещён тот контент,
		который ожидется '''
		for item in Category.objects.all():
			response = self.client.get('/%s/' % item.name.lower())
			content = Product.objects.filter(status=item)

			self.assertEqual(len(content), response.context['object_list'])
			for i in range(len(content)):
				self.assertEqual(content[i], response.context['object_list'][i])

	def test_list_page_search_available(self):
		''' Поиск выдаёт json '''
		for item in Category.objects.all():
			response = self.client.get('/%s/search?key=bo' % item.name.lower())
			self.assertEqual(response.status_code, 200)
			js = json.loads(str(response.content, 'utf-8'))
			self.assertTrue(isinstance(js, dict))

	def test_login_logout_list_page(self):
		''' Правильный код ответа при попытках зайти/выйти '''
		for item in Category.objects.all():
			response = self.client.post('/%s/login/' % item.name.lower(),
				self.userdata)
			self.assertEqual(response.status_code, 302)

			response = self.client.post('/%s/logout/' % item.name.lower(), {})
			self.assertEqual(response.status_code, 302)

			response = self.client.put('/%s/login/' % item.name.lower(),
				self.userdata)
			self.assertEqual(response.status_code, 405)

	def test_login_logout_functional_from_list_page(self):
		''' При попытках зайти/выйти - перенаправляется на правильный шаблон
		и имя пользователя отрисовывается '''
		for item in Category.objects.all():
			url = '/%s/login/' % item.name.lower()
			response = self.client.post(url, self.userdata, follow=True)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'index.html')
			self.assertIn(self.userdata['username'],
				str(response.content, 'utf-8'))

			url = '/%s/logout/' % item.name.lower()
			response = self.client.post(url, self.userdata, follow=True)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'index.html')
			self.assertNotIn(self.userdata['username'],
				str(response.content, 'utf-8'))


class UserProfileTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.userdata = {'username': 'first', 'password': 'ShockiNg'}
		User.objects.create_user(**self.userdata)

	def test_profile_availabe(self):
		pass