from abc import ABCMeta, abstractmethod
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from easy_thumbnails.files import get_thumbnailer

from anylist.settings import MEDIA_ROOT


class TemplateModel(models.Model):
	name = models.CharField(max_length=40, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		abstract = True


class CategoryGroup(TemplateModel):
	def _categories(self):
		return Category.objects.filter(group=self.id)
	categories = property(_categories)


class Category(TemplateModel):
	avatar = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)
	icon = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)
	group = models.ForeignKey(CategoryGroup)

	def avatar_path(self):
		return 'media/%s' % self.avatar.url.split('/')[-1]

	def icon_path(self):
		options = {'size': (75, 75), 'crop': True}
		thumb_url = get_thumbnailer(self.icon).get_thumbnail(options).url
		return '/media/' + thumb_url.split('/')[-1]

	def get_absolute_url(self):
		return '/%s/' % ''.join(self.name.lower().split(' '))


class Genre(TemplateModel):
	pass
#	group = models.ForeignKey(GenreGroup)


class GenreGroup(TemplateModel):
	category = models.ForeignKey(CategoryGroup)
	genres = models.ManyToManyField(Genre)


class AltName(models.Model):
	name = models.CharField(max_length=255, unique=True)


class Employ(TemplateModel):
	''' Название профессии '''
	pass


class Creator(models.Model):
	name = models.CharField(max_length=255)
	employ = models.ForeignKey(Employ)
	avatar = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)


class Hero(models.Model):
	''' is_main_hero:
	True - Главный герой
	False - Не главный
	Null - Эпизодический '''
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	actor = models.ForeignKey(Creator)
	avatar = models.ImageField(upload_to=MEDIA_ROOT)
	is_main_hero = models.NullBooleanField()


class Product(models.Model):
# поставить old_limit
	title = models.CharField(max_length=255, unique=True)
	alt_names = models.ManyToManyField(AltName)
	description = models.TextField(blank=True, null=True)
	avatar = models.ImageField(upload_to=MEDIA_ROOT)

	category = models.ForeignKey(Category)
	genres = models.ManyToManyField(Genre)

	creators = models.ManyToManyField(Creator)
	heroes = models.ManyToManyField(Hero)

	def _series(self):
		return Series.objects.filter(product=self.id).order_by('-num_season', '-number')

	def get_absolute_url(self):
		title = ''.join(re.split('[ :()-]', self.title))
		return '/%s/%d-%s' % (self.category.name.lower(), self.id, title)

	def avatar_path(self):
		return '/media/%s' % str(self.avatar).split('/')[-1]

	def __str__(self):
		return self.title


class Serie(models.Model):
	number = models.PositiveSmallIntegerField()
	num_season = models.PositiveSmallIntegerField()
	name = models.CharField(max_length=255, blank=True, null=True)
	start_date = models.DateTimeField(blank=True, null=True)
	length = models.PositiveSmallIntegerField()
	product = models.ForeignKey(Product)

	class Meta:
		ordering = ('-number', )


class Status(TemplateModel):
	pass


class UserList(models.Model):
	user = models.ForeignKey(User)
	score = models.PositiveSmallIntegerField()
	status = models.ForeignKey(Status)
	product = models.ForeignKey(Product)
#	series = models.ManyToManyField(Series)


class SerieList(models.Model):
	serie = models.ForeignKey(Serie)
	user_list = models.ForeignKey(UserList)
	like = models.NullBooleanField()