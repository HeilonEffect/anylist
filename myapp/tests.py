import json
import random

from django.test import TestCase, LiveServerTestCase
from django.test.client import Client

from selenium import webdriver

from myapp.models import *

selenium_url = 'http://188.120.228.166/'

class MainPageFunctionalTest(LiveServerTestCase):
    fixtures = ['category.json', 'category_group.json']
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        #self.browser.implicitly_wait(3)

    def test_pages(self):
        self.browser.get('localhost:8082')

        # поле поиска видно
        body = self.browser.find_elements_by_xpath('//input[@type="search"]')
        self.assertIsNotNone(body)
        self.assertTrue(body[0].is_displayed())

        # naigation panel
        elems = self.browser.find_elements_by_tag_name('details')
        self.assertTrue(body[0].is_displayed())

        elems = self.browser.find_elements_by_xpath(
            '//img[@src="/static/img/show_main_menu.png"]')
        self.assertTrue(elems[0].is_displayed())

        # панель навигации по нужному нажатию показывается и убирается
        elems[0].click()
        self.assertTrue(
            self.browser.find_elements_by_tag_name('details')[0].is_displayed())
        elems[0].click()
        self.assertFalse(
            self.browser.find_elements_by_tag_name('details')[0].is_displayed())

        # Все категории отображаются на главной странице
        elems = self.browser.find_elements_by_xpath('//main/ul/li/a/figure')
        self.assertEqual(Category.objects.count(), len(elems))
        
        for i, item in enumerate(Product.objects.all()):
            self.assertEqual(item, elems[i])

        # auth form
        elem = self.browser.find_elements_by_tag_name('button')[0]

        self.assertFalse(self.browser.find_element_by_id(
            'auth_form').is_displayed())
        elem.click()
        self.assertTrue(self.browser.find_element_by_id(
            'auth_form').is_displayed())

        # по клику доступна страничка с контентом
        random.choice(elems).click()
        elems = self.browser.find_elements_by_tag_name('header')
        self.assertIn('List of', elems[0].text)


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

        response = self.client.get('/search?key=123456789')
        self.assertEqual(response.content, b'{}')

        response = self.client.get('/search?key=1')
        self.assertEqual(response.content, b'')

        response = self.client.get('/search?name=bo')
        self.assertEqual(response.status_code, 500)


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


class UserListTest(TestCase):
    fixtures = ['category.json', 'category_group.json', 'product.json',
        'old_limit.json', 'genres.json', 'status.json']

    def setUp(self):
        self.client = Client()
        self.userdata = {'username': 'first', 'password': 'ShockiNg'}
        User.objects.create_user(**self.userdata)
        product = random.choice(Product.objects.all())
        status = random.choice(Status.objects.all())
        UserList.objects.create(
            product=product, status=status, user=User.objects.first())

    def test_content(self):
        # Rewrite, if it will add fixture whith UserList
        item = UserList.objects.first()
        url = item.product.get_absolute_url()
        url = '/profile/list/%s/%s' % (url.split('/')[1], item.status.name.lower())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        self.client.post('/login/', self.userdata)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'user_list.html')


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
        response = self.client.get(item.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'detail.html')

    def test_detail_content_available(self):
        ''' В шаблон грузится именно тот контент, который мы ожидаем '''
        item = random.choice(Product.objects.all())
        response = self.client.get(item.get_absolute_url())
        
        self.assertEqual(response.context['object'], item)

    def test_extra_context(self):
        '''
        В шаблон передаются именно те дополнительные данные, которые нужно
        '''
        item = random.choice(Product.objects.all())
        response = self.client.get(item.get_absolute_url())

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
            item.get_absolute_url() + 'login/', self.userdata, follow=True)
        
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


class AddProductTest(TestCase):
    fixtures = ['category.json', 'category_group.json', 'product.json',
        'old_limit.json', 'genres.json', 'status.json']

    def setUp(self):
        self.client = Client()
        self.userdata = {'username': 'first', 'password': 'ShockiNg'}
        User.objects.create_user(**self.userdata)

    def test_anon_no_avaibility(self):
        for category in Category.objects.all():
            response = self.client.get(category.get_absolute_url() + 'add')
            self.assertEqual(response.status_code, 403)

    def test_user_avaibility(self):
        self.client.post('/login/', self.userdata)
        for category in Category.objects.all():
            response = self.client.get(category.get_absolute_url() + 'add')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.template_name[0], 'forms/add_form.html')

    def test_extra_context(self):
        self.client.post('/login/', self.userdata)
        for category in Category.objects.all():
            response = self.client.get(category.get_absolute_url() + 'add')

            self.assertEqual(response.context['category'],
                category.get_absolute_url()[1:-1])
            
            for item in Category.objects.all():
                if item.get_absolute_url() == response.context['category']:
                    context['category_id'] = item.id
                    context['header'] = 'Add new %s' % category

    def test_add(self):
        self.client.post('/login/', self.userdata)
        data = ['title', 'description']
        data = dict(zip(data, data))
        data['category'] = random.choice(Category.objects.all())
        genres = Genre.objects.all()
        data['genres'] = [random.choice(genres) for i in range(2)]
        with open('/home/ctulhu/anylist/myapp/img1.png', 'rb') as fp:
            data['avatar'] = fp
            response = self.client.post(
                '%sadd' % data['category'].get_absolute_url(), data,
                follow=True)
            self.assertEqual(response.status_code, 200)


class HeroTest(TestCase):
    fixtures = ['category.json', 'category_group.json', 'product.json',
        'old_limit.json', 'genres.json', 'status.json', 'creator.json',
        'employ.json', 'hero.json']

    def setUp(self):
        self.client = Client()
        self.userdata = {'username': 'first', 'password': 'ShockiNg'}
        User.objects.create_user(**self.userdata)


    def test_hero_item_avaibility(self):
        item = random.choice(Hero.objects.all())
        response = self.client.get(item.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'hero.html')
        self.assertEqual(response.context['object'], item)


    def test_hero_list_avaibility(self):
        item = random.choice(Product.objects.all())
        response = self.client.get(item.get_absolute_url() + 'heroes/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'heroes_list.html')
        for i, hero in enumerate(item.heroes.all()):
            self.assertEqual(self.context['object_list'][i], hero)


class CreatorTest(TestCase):
    fixtures = ['category.json', 'category_group.json', 'product.json',
        'old_limit.json', 'genres.json', 'status.json', 'creator.json',
        'employ.json', 'hero.json']

    def setUp(self):
        self.client = Client()
        self.userdata = {'username': 'first', 'password': 'ShockiNg'}
        User.objects.create_user(**self.userdata)


    def test_creator_item_avaibility(self):
        item = random.choice(Creator.objects.all())
        response = self.client.get(item.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'creator.html')
        self.assertEqual(response.context['object'], item)


    def test_creator_list_avaibility(self):
        item = random.choice(Product.objects.all())
        response = self.client.get(item.get_absolute_url() + 'creators/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'creators_list.html')
        for i, hero in enumerate(item.creators.all()):
            self.assertEqual(self.context['object_list'][i], hero)


class RandomSelectedProductList(TestCase):
    ''' Если мы в на списке произведений указали выборку '''
    fixtures = ['category.json', 'category_group.json', 'product.json',
        'old_limit.json', 'genres.json', 'status.json', 'creator.json',
        'employ.json', 'hero.json']

    def setUp(self):
        self.client = Client()
        self.userdata = {'username': 'first', 'password': 'ShockiNg'}
        User.objects.create_user(**self.userdata)

    def test_content(self):
        ''' Rewrite this! '''
        response = self.client.get('/anime/filter/genres/Shounen,School/old_limit/PG-13/')
        result = Product.objects.filter(genres__name='Shounen').filter(
            genres__name='School').filter(
            category__name='Anime', old_limit__name='PG-13')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'list.html')
        for i, item in enumerate(result):
            self.assertEqual(response.context['object_list'][i], item)


class UserListOperationTest(TestCase):
    fixtures = ['category.json', 'category_group.json', 'product.json',
        'old_limit.json', 'genres.json', 'status.json']

    def setUp(self):
        self.client = Client()
        self.userdata = {'username': 'first', 'password': 'ShockiNg'}
        User.objects.create_user(**self.userdata)
        product = random.choice(Product.objects.all())
        status = random.choice(Status.objects.all())
        UserList.objects.create(
            product=product, status=status, user=User.objects.first())

    def test_status_update(self):
        self.client.post('/login/', self.userdata)

        product = UserList.objects.first().product
        response = self.client.get(product.get_absolute_url())
        status = random.choice(Status.objects.all())

        response = self.client.post(product.get_absolute_url() + 'status',
            {'name': status.name})
        
        self.assertEqual(response.status_code, 200)

        product = Product.objects.last()
        status = random.choice(Status.objects.all())

        response = self.client.post(product.get_absolute_url() + 'status',
            {'name': status.name})
        response = self.client.get(product.get_absolute_url())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], product)

        response = self.client.post(product.get_absolute_url() + 'status',
            {'name': 'Не статус'})
        self.assertEqual(response.status_code, 500)


    def test_editing_available(self):
        self.client.post('/login/', self.userdata)
        for product in Product.objects.all():
            response = self.client.get(product.get_absolute_url() + 'edit')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.template_name[0], 'forms/edit_form.html')
            self.assertEqual(response.context['object'], product)

            data = ['title', 'description']
            data = dict(zip(data, data))
            data['category'] = random.choice(Category.objects.all())
            genres = Genre.objects.all()
            data['genres'] = [random.choice(genres) for i in range(2)]
            with open('/home/ctulhu/anylist/myapp/img1.png', 'rb') as fp:
                data['avatar'] = fp
            
                response = self.client.post(product.get_absolute_url() + 'edit',
                    data, follow=True)

            self.assertEqual(response.status_code, 200)

class ModelTest(TestCase):
    fixtures = ['category.json', 'category_group.json', 'product.json',
        'old_limit.json', 'genres.json', 'status.json', 'creator.json',
        'employ.json', 'hero.json', 'serie.json']
    
    def setUp(self):
        self.userdata = {'username': 'first', 'password': 'ShockiNg'}
        User.objects.create_user(**self.userdata)
        product = random.choice(Product.objects.all())
        status = random.choice(Status.objects.all())
        UserList.objects.create(
            product=product, status=status, user=User.objects.first())

        SerieList.objects.create(serie=Serie.objects.first(),
            user_list=UserList.objects.first())

    def test_model_str_resolve(self):
        p = Creator.objects.first()
        self.assertEqual(p.name, str(p))

        p = Hero.objects.first()
        self.assertEqual(p.name, str(p))

        p = UserList.objects.first()
        self.assertEqual('%s: %s' % (p.status.name, p.product.title), str(p))

        p = Serie.objects.first()
        self.assertEqual('<%s>: Season: %d Serie: %d' % (p.product,
            p.num_season, p.number), str(p))

        p = SerieList.objects.first()
        self.assertEqual(str(p.serie), str(p))


class SerieTest(TestCase):
    fixtures = ['category.json', 'category_group.json', 'product.json',
        'old_limit.json', 'genres.json', 'status.json', 'creator.json',
        'employ.json', 'hero.json']

    def setUp(self):
        self.userdata = {'username': 'first', 'password': 'ShockiNg'}
        User.objects.create_user(**self.userdata)
        product = random.choice(Product.objects.all())
        status = random.choice(Status.objects.all())
        Serie.objects.create(number=1, num_season=1, length=20,
            product=Product.objects.first())

    # def test_add_list_serie(self):
    #     data = 'number=1&num_season=1&product=1'
    #     response = self.client.post('/mylist/series/add', data)
    #     self.assertEqual(response.status_code, 302)

    #     self.assertIsNone(SerieList.objects.last().number, 1)

    def test_series_view(self):
        response = self.client.get(
            Product.objects.first().get_absolute_url() + 'series/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'series.html')
        for i, item in enumerate(SerieList.objects.filter(
            user_list__product__id=1, user_list__user=User.objects.first())):
            
            self.assertEqual(response.context['object_list'][i], item)


class AddCreatorTest(TestCase):
    fixtures = ['category.json', 'category_group.json', 'product.json',
        'old_limit.json', 'genres.json', 'status.json', 'creator.json',
        'employ.json', 'hero.json']

    def setUp(self):
        self.userdata = {'username': 'first', 'password': 'ShockiNg'}
        User.objects.create_user(**self.userdata)
        self.client = Client()
 
    def test_avaibiity(self):
        self.client.post('/login/', self.userdata)

        response = self.client.get('/creator/add')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'forms/add_creator.html')

        for i, item in enumerate(Employ.objects.all()):
            self.assertEqual(response.context['employers'][i], item)

    def test_add_hero(self):
        self.client.post('/login/', self.userdata)

        url = '%sheroes/add' % Product.objects.first().get_absolute_url()
        print(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'forms/add_hero.html')