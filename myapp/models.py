from django.contrib.auth.models import User
from django.db import models

from anylist.settings import MEDIA_ROOT


class Names(models.Model):
	name = models.CharField(max_length=255, unique=True)


class Status(models.Model):
	name = models.CharField(max_length=10, unique=True)


class Product(models.Model):
	''' Абстрактное описание одиночного продукта '''
	title = models.CharField(max_length=255, unique=True)
	alt_name = models.ManyToManyField(Names, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	avatar = models.ImageField(blank=True, upload_to=MEDIA_ROOT)
	old_limit = models.PositiveSmallIntegerField(default=0)

	def get_absolute_url(self):
		category = self.__doc__.split('(')[0].lower()
		return '%s/%s/' % (category, self.title)

	def __str__(self):
		return self.title
	
	class Meta:
		abstract = True
		ordering = ('title',)


class ListedProduct(models.Model):
	'''  '''
	product = models.ForeignKey(Product)
	status = models.ForeignKey(Status)
	score = models.PositiveSmallIntegerField(null=True, blank=True)
	user = models.ForeignKey(User)
	class Meta:
		abstract = True


class Mutator(object):
	def mutate(self):
		Product.objects.create()

