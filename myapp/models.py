from abc import ABCMeta, abstractmethod
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from easy_thumbnails.files import get_thumbnailer

from anylist.settings import MEDIA_ROOT


class CategoryGroup(models.Model):
	name = models.CharField(max_length=40, unique=True)
	def _categories(self):
		return Category.objects.filter(group=self.id)
	children = property(_categories)

	def __str__(self):
		return self.name


class Category(models.Model):
	''' То, что отображено на главной странице и экспресс панели (разделы) '''
	icon = models.ImageField(upload_to=MEDIA_ROOT, null=True)
	avatar = models.ImageField(upload_to=MEDIA_ROOT, null=True)
	name = models.CharField(max_length=30, unique=True)
	group = models.ForeignKey(CategoryGroup)

	def icon_path(self):
		options = {'size': (100, 100), 'crop': True}
		thumb_url = get_thumbnailer(self.icon).get_thumbnail(options).url
		return '/media/%s' % thumb_url.split('/')[-1]

	def avatar_path(self):
		options = {'size': (300, 400), 'crop': True}
		thumb_url = get_thumbnailer(self.avatar).get_thumbnail(options).url
		return '/media/%s' % thumb_url.split('/')[-1]

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return '/%s/%s/' % (self.group.name, self.name)


class Status(models.Model):
	name = models.CharField(max_length=15, unique=True)


class GenreGroup(models.Model):
	name = models.CharField(max_length=30, unique=True)
	def _genres(self):
		return Genre.objects.filter(group=self.id)
	genres = property(_genres)


class Genre(models.Model):
	name = models.CharField(max_length=40)
	group = models.ForeignKey(GenreGroup)


class Employ(models.Model):
	''' Род занятий '''
	name = models.CharField(max_length=50, unique=True)


class Creator(models.Model):
	name = models.CharField(max_length=200)
	employ = models.ManyToManyField(Employ)
	avatar = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)


class Hero(models.Model):
	'''
	Таблица персонажей
	'''
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	source_description = models.URLField(blank=True, null=True)
	avatar = models.ImageField(upload_to=MEDIA_ROOT)


# Список полей для таблицы продукта
class Product(models.Model):
	title = models.CharField(max_length=255, unique=True)
	description = models.TextField(blank=True, null=True)
	source_description = models.URLField(blank=True, null=True)

	avatar = models.ImageField(upload_to=MEDIA_ROOT)
	
	old_limit = models.PositiveSmallIntegerField()
	genres = models.ManyToManyField(Genre)
	
	creators =  models.ManyToManyField(Creator)
	heroes = models.ManyToManyField(Hero)

	def _series(self):
		raise Exception('Not Implemented Error')
	series = property(_series)

	class Meta:
		abstract = True


# Список полей для таблицы серий
class Serie(models.Model):
	number = models.PositiveSmallIntegerField()
	num_season = models.PositiveSmallIntegerField(blank=True, null=True)
	name = models.CharField(max_length=255, blank=True, null=True)
	description = models.CharField(max_length=1024, blank=True, null=True)
	length = models.PositiveSmallIntegerField()

	class Meta:
		abstract = True


class UserList(models.Model):
	score = models.PositiveSmallIntegerField(blank=True, null=True)
	user = models.ForeignKey(User)
	status = models.ForeignKey(Status)

	class Meta:
		abstract = True


class Anime(Product):
	def _series(self):
		return AnimeSerie.objects.filter(product=self.id)


class AnimeSerie(Serie):
	product = models.ForeignKey(Anime)


class AnimeList(UserList):
	product = models.ForeignKey(Anime)
	series = models.ManyToManyField(AnimeSerie)


class Manga(Product):
	def _series(self):
		return MangaSerie.objects.filter(product=self.id)


class MangaSerie(Serie):
	product = models.ForeignKey(Manga)


class MangaList(UserList):
	product = models.ForeignKey(Manga)
	series = models.ManyToManyField(MangaSerie)


class Ranobe(Product):
	def _series(self):
		return RanobeSerie.objects.filter(product=self.id)


class RanobeSerie(Serie):
	product = models.ForeignKey(Ranobe)


class RanobeList(UserList):
	product = models.ForeignKey(Ranobe)
	series = models.ManyToManyField(RanobeSerie)


class DetectiveRoman(Product):
	def _series(self):
		return RanobeSerie.objects.filter(product=self.id)


class DetectiveSerie(Serie):
	product = models.ForeignKey(DetectiveRoman)


class DetectiveBookList(UserList):
	product = models.ForeignKey(DetectiveRoman)
	series = models.ManyToManyField(DetectiveSerie)


class DetectiveVideo(Product):
	def _series(self):
		return DetectiveVideoSerie.objects.filter(product=self.id)


class DetectiveVideoSerie(Serie):
	product = models.ForeignKey(DetectiveVideo)


class DetectiveVideoList(UserList):
	product = models.ForeignKey(DetectiveVideo)
	series = models.ManyToManyField(DetectiveVideoSerie)


class FantasticSerial(Product):
	def _series(self):
		return FantasticSerialSerie.objects.filter(product=self.id)


class FantasticSerialSerie(Serie):
	product = models.ForeignKey(FantasticSerial)


class FantasticSerialList(UserList):
	product = models.ForeignKey(FantasticSerial)
	series = models.ManyToManyField(FantasticSerialSerie)


class FantasticBook(Product):
	def _series(self):
		return FantasticBookSerie.objects.filter(product=self.id)


class FantasticBookSerie(Serie):
	product = models.ForeignKey(FantasticBook)


class FantasticBookList(UserList):
	product = models.ForeignKey(FantasticBook)
	series = models.ManyToManyField(FantasticBookSerie)
