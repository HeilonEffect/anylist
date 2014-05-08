from django.db import models
from anylist.settings import MEDIA_ROOT


class Genre(models.Model):
	name = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=255)


class Anime(models.Model):
	jp_name = models.CharField(max_length=255)
	ru_name = models.CharField(max_length=255, blank=True)
	en_name = models.CharField(max_length=255, blank=True)

	description = models.TextField(blank=True)
	genres = models.ManyToManyField(Genre)
	
