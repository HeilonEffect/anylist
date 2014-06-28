from django.db import models

from myapp.models import AbstractProduct


class Names(models.Model):
	name = models.CharField(max_length=255, unique=True)


class GenreGroup(models.Model):
	name = models.CharField(max_length=30, unique=True)


class Genre(models.Model):
	name = models.CharField(max_length=50)
	group = models.ForeignKey(GenreGroup)


class Hero(models.Model):
	name = models.CharField(max_length=1024)
	description = models.TextField(blank=True, null=True)
	avatar = models.ImageField(upload_to=MEDIA_ROOT)


class Creator(models.Model):
	name = models.CharField(max_length=255)
	emploe = models.CharField(max_length=100) # должность (режиссер, сценарист)
	avatar = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)


class Series(models.Model):
	number = models.PositiveSmallIntegerField(null=True, blank=True)
	num_season = models.PositiveSmallIntegerField(null=True, blank=True)
	name = models.CharField(max_length=255, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	length = models.PositiveSmallIntegerField()


class Anime(AbstractProduct):
	def get_absolute_url(self):
		result = super(Anime, self).get_absolute_url()
		return '/jp-anime' % result


class Manga(AbstractProduct):
	def get_absolute_url(self):
		result = super(Manga, self).get_absolute_url()
		return '/jp-manga' % result


class Ranobe(AbstractProduct):
	def get_absolute_url(self):
		result = super(Ranobe, self).get_absolute_url()
		return '/jp-ranobe'