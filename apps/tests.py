import json
import itertools

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from .models import *


class MainPageTest(TestCase):
	''' Тесты главной страницы '''
	fixtures = ['production.json', 'nav_group.json', 'category.json']
	userdata = {'username': 'first', 'password': 'ShockiNg'}

	def setUp(self):
		self.user = User.objects.create_user(**self.userdata)
		self.client = Client()

	def test_login_logout(self):
		''' Возможность залогиниться/разлогиниться '''
		response = self.client.post('/login/', self.userdata)
		self.assertEqual(response.status_code, 302)

		response = self.client.post('/logout/', {})
		self.assertEqual(response.status_code, 302)

		response = self.client.post('/login/', self.userdata, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')
		self.assertIn(
			self.userdata['username'], str(response.content, 'utf-8'))

		response = self.client.post('/logout/', {}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')
		self.assertNotIn(
			self.userdata['username'], str(response.content, 'utf-8'))


	def test_search(self):
		''' Поиск с главной страницы '''
		response = self.client.get('/search?key=bo')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Bones', json.loads(str(response.content, 'utf-8')))

	def test_categories(self):
		''' Все категории тематические группы отображаются
		в шаблоне главной страницы '''
		response = self.client.get('/')
		categories = [child for group in response.context['object_list']
			for child in group.children]
		
		for category in Category.objects.all():
			self.assertIn(category, categories)


	def test_global_nav(self):
		''' Все категории отображаются в глобальном меню '''
		response = self.client.get('/')
		categories = [child for group in response.context['nav_groups']
			for child in group.children]

		for category in Category.objects.all():
			self.assertIn(category, categories)



class ListPageTest(TestCase):
	''' Тесты для списка произведений '''
	fixtures = ['production.json', 'nav_group.json', 'category.json',
		'genre.json', 'genre_group.json', 'anime.json']
	userdata = {'username': 'first', 'password': 'ShockiNg'}

	def setUp(self):
		self.user = User.objects.create_user(**self.userdata)
		self.client = Client()


	def test_login_logout(self):
		''' Возможность залогиниться/разлогиниться '''
		response = self.client.post('/anime/login/', self.userdata)
		self.assertEqual(response.status_code, 302)

		response = self.client.post('/anime/logout/', {})
		self.assertEqual(response.status_code, 302)

		response = self.client.post('/anime/login/', self.userdata, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'list.html')
		self.assertIn(
			self.userdata['username'], str(response.content, 'utf-8'))

		response = self.client.post('/anime/logout/', {}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'list.html')
		self.assertNotIn(
			self.userdata['username'], str(response.content, 'utf-8'))


	def test_count_categories(self):
		response = self.client.get('/anime/')
		self.assertEqual(response.status_code, 200)