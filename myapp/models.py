from django.db import models

from anylist.settings import MEDIA_ROOT


class Names(models.Model):
	name = models.CharField(max_length=255, unique=True)


class Product(models.Model):
	''' Абстрактное описание одиночного продукта '''
	title = models.CharField(max_length=255, unique=True)
	alt_name = models.ManyToManyField(Names, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	avatar = models.ImageField(blank=True, upload_to=MEDIA_ROOT)

	def get_absolute_url(self):
		category = self.__doc__.split('(')[0].lower()
		return '%s/%s/' % (category, self.title)

	def __str__(self):
		return self.title
	
	class Meta:
		abstract = True
		ordering = ('title',)


class Mutator(object):
	def mutate(self):
		Product.objects.create()


ProductChilds = ['Anime', 'Manga', 'Game', 'Dorama', 'Ranobe', 'Visual Key', 'Detective', 'Fantasy', 'SciFi']

for product in ProductChilds:
	pass