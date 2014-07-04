import json

from django.test import TestCase
from django.test.client import Client

from myapp.models import *


# Create your tests here.
class MainPageTest(TestCase):

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
		statuses = Status.objects.all()
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
	pass