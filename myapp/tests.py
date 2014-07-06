import json
import random

from django.test import TestCase
from django.test.client import Client

from myapp.models import *


# Create your tests here.
class MainPageTest(TestCase):
	fixtures = ['category.json', 'category_group.json']
	
	def setUp(self):
		self.client = Client()
		self.userdata = {'username': 'first', 'password': 'ShockiNg'}
		User.objects.create_user(**self.userdata)
	

	def test_main_page_available(self):
		''' Главная страничка грузится '''
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')


	def test_main_page_extra_content(self):
		''' "Экспресс панель" '''
		response = self.client.get('/')
		for i, category in enumerate(CategoryGroup.objects.all()):
			self.assertEqual(response.context['nav_groups'][i], category)


	def test_main_page_content(self):
		''' На главной странице отображён необходимый нам контент '''
		response = self.client.get('/')
		categories = CategoryGroup.objects.all()
		self.assertEqual(len(response.context['object_list']), len(categories))
		for i in range(len(categories)):
			self.assertEqual(response.context['object_list'][i], categories[i])


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
	fixtures = ['category.json', 'category_group.json', 'product.json',
		'old_limit.json', 'genres.json', 'status.json']

	def setUp(self):
		self.client = Client()
		self.userdata = {'username': 'first', 'password': 'ShockiNg'}
		User.objects.create_user(**self.userdata)

	
	def test_list_page_available(self):
		''' Содержимое страниц с контентом всегда доступно '''
		for item in Category.objects.all():
			response = self.client.get(item.get_absolute_url())
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'list.html')

	
	def test_list_page_extra_content(self):
		''' Содержимое всех страниц всегда содержит ожидаемые элементы,
		передаваемые через get_context_data '''
		for item in Category.objects.all():
			response = self.client.get(item.get_absolute_url())
			self.assertEqual(response.context['header'],
				'List of %s' % item.get_absolute_url().split('/')[1])
			
			for i, limit in enumerate(Raiting.objects.all()):
				self.assertEqual(limit, response.context['raiting'][i])
			# оставить жанры на потом


	def test_list_page_content(self):
		''' На соответсвующей категории со списками размещён тот контент,
		который ожидется '''
		for item in Category.objects.all():
			response = self.client.get(item.get_absolute_url())
			content = Product.objects.filter(category=item)

			self.assertEqual(len(content), len(response.context['object_list']))
			for i in range(len(content)):
				self.assertEqual(content[i], response.context['object_list'][i])

	def test_login_logout_list_page(self):
		''' Правильный код ответа при попытках зайти/выйти '''
		for item in Category.objects.all():
			response = self.client.post('%slogin/' % item.get_absolute_url(),
				self.userdata)
			self.assertEqual(response.status_code, 302)

			response = self.client.post('%slogout/' % item.get_absolute_url(), {})
			self.assertEqual(response.status_code, 302)

			response = self.client.put('%slogin/' % item.get_absolute_url(),
				self.userdata)
			self.assertEqual(response.status_code, 405)

	def test_login_logout_functional_from_list_page(self):
		''' При попытках зайти/выйти - перенаправляется на правильный шаблон
		и имя пользователя отрисовывается '''
		for item in Category.objects.all():
			response = self.client.post('%slogin/' % item.get_absolute_url(),
				self.userdata, follow=True)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'list.html')
			self.assertIn(self.userdata['username'],
				str(response.content, 'utf-8'))

			url = '%slogout/' % item.get_absolute_url()
			response = self.client.post(url, {}, follow=True)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.template_name[0], 'list.html')
			self.assertNotIn(self.userdata['username'],
				str(response.content, 'utf-8'))


class UserProfileTest(TestCase):
	fixtures = ['category.json', 'category_group.json', 'product.json',
		'old_limit.json', 'genres.json', 'status.json']

	def setUp(self):
		self.client = Client()
		self.userdata = {'username': 'first', 'password': 'ShockiNg'}
		User.objects.create_user(**self.userdata)

		product = random.choice(Product.objects.all())
		status = random.choice(Status.objects.all())
		UserList.objects.create(
			product=product, status=status, user=User.objects.get(
				username=self.userdata['username']))

	
	def test_profile_availabe(self):
		'''
		После регистрации профиль доступен, при выходе - перенаправляется
		на главную страницу, если пользователь не зарегестрирован - 301
		'''
		response = self.client.get('/profile')
		self.assertEqual(response.status_code, 301)

		response = self.client.post('/login/', self.userdata)
		self.assertEqual(response.status_code, 302)
		
		response = self.client.get('/profile/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.templates[0].name, 'profile.html')

		response = self.client.post('/profile/logout/', {}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'index.html')


	def test_profile_content_available(self):
		'''
		В профиль передаётся тот контент, который мы ожидаем
		'''
		self.client.post('/', self.userdata)
		response = self.client.get('/profile/')

		result = []
		mylist = UserList.objects.filter(user__name=self.userdata['username'])
		statuses = Status.objects.all()
		for category in Category.objects.all():
			tmp = []
			for status in statuses:
				p = mylist.filter(
					product__category=category, status=status).count()
				if p > 0:
					tmp.append({
						'status': status.name,
						'count': p
					})
			if tmp:
				result.append({'key': category, 'values': tmp})
		self.assertEqual(json.dumps(result),
			json.dumps(response.context['object_list']))


class UserListTest(TestCase):
	fixtures = ['category.json', 'category_group.json', 'product.json',
		'old_limit.json', 'genres.json', 'status.json']

	def setUp(self):
		self.client = Client()
		self.userdata = {'username': 'first', 'password': 'ShockiNg'}
		User.objects.create_user(**self.userdata)
		product = random.choice(Product.objects.all())
		status = random.choice(Status.objects.all())
		UserList.objects.create(product=product, status=status, user=User.objects.get(id=1))


class DetailProductTest(TestCase):
	fixtures = ['category.json', 'category_group.json', 'product.json',
		'old_limit.json', 'genres.json', 'status.json']

	def setUp(self):
		self.client = Client()
		self.userdata = {'username': 'first', 'password': 'ShockiNg'}
		User.objects.create_user(**self.userdata)

	def test_detail_available(self):
		''' Страничка произвольного продукта загружается
		'''
		item = random.choice(Product.objects.all())
		response = self.client.get(item.get_absolute_url() + '/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.template_name[0], 'detail.html')

	def test_detail_content_available(self):
		''' В шаблон грузится именно тот контент, который мы ожидаем '''
		item = random.choice(Product.objects.all())
		response = self.client.get(item.get_absolute_url() + '/')
		
		self.assertEqual(response.context['object'], item)

	def test_extra_context(self):
		'''
		В шаблон передаются именно те дополнительные данные, которые нужно
		'''
		item = random.choice(Product.objects.all())
		response = self.client.get(item.get_absolute_url() + '/')

		self.assertEqual(response.context['header'], item.title)
		self.assertEqual(response.context['category'],
			item.get_absolute_url().split('/')[1])
		for i, status in enumerate(Status.objects.all()):
			self.assertEqual(response.context['statuses'][i], status)

		p = None
		try:
			p = response.context['is_listed']
		except KeyError as e: pass
		self.assertIsNone(p)

	def test_is_listed_context(self):
		'''
		Авторизация происходит без проблем, после авторизации нам доступен
		статус просмотра этого продукта
		'''
		item = random.choice(Product.objects.all())
		response = self.client.post(
			item.get_absolute_url() + '/login/', self.userdata, follow=True)
		
		p = None
		p1 = None
		try:
			p1 = response.context['is_listed']
			p = UserList.objects.get(product=item,
				user__name=self.userdata['name'])
		except Exception as e:
			self.assertIsNone(p)
		else:
			self.assertEqual(p1, p)

		self.assertEqual(response.status_code, 200)
