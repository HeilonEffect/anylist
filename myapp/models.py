from abc import ABCMeta, abstractmethod
import re

from django.contrib.auth.models import User
from django.db import models

from anylist.settings import MEDIA_ROOT


class Names(models.Model):
	name = models.CharField(max_length=255, unique=True)


class AbstractProduct(models.Model):
	title = models.CharField(max_length=255, unique=True)
	alt_names = models.ManyToManyField(Names, null=True)
	
	description = models.TextField(blank=True, null=True)
	source_description = models.URLField()
	old_limit = models.PositiveSmallIntegerField()

	avatar = models.ImageField(upload_to=MEDIA_ROOT)

#	creators = models.ManyToManyField(Creator, null=True)
#	heroes = models.ManyToManyField(Hero, null=True)
#	series = models.ManyToManyField(Series, null=True)

#	genres = models.ManyToManyField(Genre)

	def get_absolute_url(self):
		orig = re.sub('[ :()]', '_', self.title, flags=re.G)
		return '/%s/' % orig

	class Meta:
		abstract = True


class Categories(models.Model):
	''' То, что отображено на главной странице и экспресс панели '''
	icon = models.ImageField(upload_to=MEDIA_ROOT)
	avatar = models.ImageField(upload_to=MEDIA_ROOT)
	name = models.CharField(max_length=30, unique=True)


class ProductRouter(object):
	'''
	Указывает сохранять все модели в postgres таблицу
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