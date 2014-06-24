import re, json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.test import TestCase
from django.test.client import Client, RequestFactory

from selenium import webdriver

from .models import *
from anylist.views import *

Types = {'anime': Anime, 'manga': Manga, 'criminalystic': Criminalystic}


class HomePageTest(TestCase):	
	def test_get_page(self):
		'Тестируем доступность главной страницы'
		request = RequestFactory().get('/')
		view = MainPage.as_view()

		response = view(request)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')


	def test_register(self):
		''' Возможность залогиниться/разлогиниться '''
		User.objects.create_user(username='first', password='ShockiNg')
		c = Client()
		response = c.post('/login/', {'username': 'first', 'password': 'ShockiNg'})
		self.assertEqual(response.status_code, 302)

		response = c.post('/logout/', {}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')
		
		response = c.post('/login/', {'username': 'first', 'password': 'ShockiNg'}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')
		
		self.assertEqual('first', re.search(
			r'<a href="/profile">(\w+)</a>', str(response.content, 'utf-8')).group(1))

	def test_search(self):
		''' Возможность поиска '''
		Raiting.objects.create(name='NC-17')
		Production.objects.create(title='Bones', old_limit=Raiting.objects.get(name='NC-17'))
		c = Client()
		response = c.get('/search?key=bo')
		self.assertEqual(response.status_code, 200)
		
		content = json.loads(str(response.content, 'utf-8'))

		self.assertIn('Bones', content)


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
		''' страница доступна и выдаёт нужный url '''
		view = ProductDetail.as_view()

		for item in Anime.objects.all():
			request = RequestFactory().get('/anime/%s/' % item.link.get_absolute_url())

			response = view(request)

			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'detail.html')

		request = RequestFactory().get('/anime/yob')
		response = view(request)

		self.assertEqual(response.status_code, 404)


class ActionProductTest(TestCase):
	''' Добавление продукта в список, смена статуса, указание серии '''

	def setUp(self):
		User.objects.create_user(username='first', password='ShockiNg')
		Raiting.objects.create(name='PG-13')
		p = Production.objects.create(
			title='Angel Beats', old_limit=Raiting.objects.get(name='PG-13'))
		Anime.objects.create(link=p)
		Status.objects.create(name='Planned')
		p = ThematicGroup.objects.create(name='Anime')
		Category.objects.create(name='Anime', group=p)
		Status.objects.create(name='Watch')
	
	def test_add_product(self):
		''' Возможность добавления в список '''
		c = Client()
		response = c.post('/login/', {'username': 'first', 'password': 'ShockiNg'}, follow=True)
		self.assertEqual(response.status_code, 200)
		
		response = c.post('/anime/1-angelbeats/status', {'name': 'Planned'})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(str(response.content, 'utf-8'), 'Planned')

		response = c.get('/profile/list/anime/planned')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'user_list.html')
		self.assertEqual(
			re.search('(Angel Beats)', str(response.content, 'utf-8')).group(1),
			'Angel Beats')


class AddProductPageTest(TestCase):

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='jacob', email='jacob@_',
			password='top_secret')
		self.view = AddProduct.as_view()


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


class FunctionalHomePageTest(LiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
		self.browser.get(self.live_server_url + '/')
		self.buttons = self.browser.find_elements_by_tag_name('button')
		self.auth_form = self.browser.find_element_by_id('auth_form')

	def tearDown(self):
		self.browser.quit()

	def test_home_page_available(self):
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Main Page', body.text)

	def test_login_button_available(self):
		self.assertIn('Log In', [button.text for button in self.buttons])

	def test_login_form_available(self):
		self.assertFalse(self.auth_form.is_displayed())
		button = [item for item in self.buttons if item.text == 'Log In']
		button[0].click()
		self.assertTrue(self.auth_form.is_displayed())

	def test_login_sucess(self):
		c = Client()
		User.objects.create_user(username='first', password='ShockiNg')
		response = c.post('/login/',
			{'username': 'first', 'password': 'ShockiNg'})
		self.assertEqual(response.status_code, 302)
		
		response = c.post('/logout/', {})
		self.assertEqual(response.status_code, 302)
		
		response = c.post('/login/',
			{'username': 'first', 'password': 'ShockiNg'}, follow=True)
		self.assertEqual(response.status_code, 200)
		
		# Проверяем, что после залогинивания виден профиль пользователя
		r = str(response.content, 'utf-8')
		self.assertEqual(
			re.search(r'<a href="/profile">(\w+)</a>', r).group(1), 'first')


	def test_categories_available(self):
		# Ссылки содержат изображения
		self.categories = self.browser.find_elements_by_xpath('//main/ul/li/a')
		#self.images = self.browser.find_elements_by_xpath('//main/ul/li/a/figure/img')
		self.category_names = [item.text for item in self.categories]
		for category in self.category_names:
			# Загружаем контент с указанной ссылки
			self.browser.find_element_by_link_text(category).click()
			body = self.browser.find_element_by_tag_name('body')
			self.assertIn(category, body.text)
