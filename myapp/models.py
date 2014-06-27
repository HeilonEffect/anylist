from abc import ABCMeta, abstractmethod
import re

from django.contrib.auth.models import User
from django.db import models

from anylist.settings import MEDIA_ROOT


class Names(models.Model):
	name = models.CharField(max_length=255, unique=True)


class AbstractHero(models.Model):
	name = models.CharField(max_length=1024)
	description = models.TextField(blank=True, null=True)
	avatar = models.ImageField(upload_to=MEDIA_ROOT)


class AbstractCreator(models.Model):
	''' Т.к creator'ов явно меньше, чем остальных, то сделаем одну таблицу
	на всех '''
	name = models.CharField(max_length=255)
	emploe = models.CharField(max_length=100)	# должность
	avatar = models.ImageField(upload_to=MEDIA_ROOT)


class AbstractProduct(models.Model):
	title = models.CharField(max_length=255, unique=True)
	alt_names = models.ManyToManyField(Names, null=True)
	
	description = models.TextField(blank=True, null=True)
	source_description = models.URLField()

	avatar = models.ImageField(upload_to=MEDIA_ROOT)

	creators = models.ManyToManyField(AbstractCreator, null=True)
	heroes = models.ManyToManyField(AbstractHero, null=True)

	def get_absolute_url(self):
		orig = re.sub('[ :()]', '_', self.title, flags=re.G)
		return '/%s/' % orig

	class Meta:
		abstract = True


class AbstractRelation(models.Model):
	''' Связывает произведения, серии и героев (Colleague) '''
	class Meta:
		abstract = True


class Colleague(metaclass=ABCMeta):
	def __init__(self, product, hero, creator):
		self._product = product
		self._hero = hero
		self._creator = creator


class Japanese(AbstractProduct):
	pass


class Detective(AbstractProduct):
	pass


class Fantastic(AbstractProduct):
	pass


class ProductRouter(object):
	'''
	Указывает сохранять все модели в mysql таблицу
	'''
	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'myapp':
			return 'product_db'
		return None

	def db_for_write(self, model, **hints):
		if model._meta.app_label == 'myapp':
			return 'product_db'
		return None

	def allow_relation(self, obj1, obj2, **hints):
		if obj1._meta.app_label == 'myapp' or obj2._meta.app_label == 'myapp':
			return True
		return None

	def allow_syncdb(self, db, model):
		if db == 'product_db':
			return model._meta.app_label == 'myapp'
		elif model._meta.app_label == 'myapp':
			return False
		return None