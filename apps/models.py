import re

from django.db import models
from django.core.exceptions import ValidationError

from anylist.settings import MEDIA_ROOT


class GenreGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def _genres(self):
        return Genre.objects.filter(group=self.id)
    genres = property(_genres)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=140, unique=True)
    group = models.ForeignKey(GenreGroup)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)


def validate_old_limit(value):
    if value > 21 or value < 0:
        raise ValidationError(
            "Old limit don't mutch great, then 21 and small, then 0")


def validate_genres(value):
    if value in Genre.objects.all():
        pass


class Product(models.Model):
    ''' Description single product '''
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)

    avatar = models.FileField(upload_to=MEDIA_ROOT)

    start_date = models.DateField(blank=True)   # if emty - then it is anounce
    old_limit = models.PositiveSmallIntegerField(validators=[validate_old_limit])

#    category = models.ForeignKey(Category, blank=True)

    def get_absolute_url(self):
        return ''.join(re.split(r'[ :_]', self.title))
    
    class Meta:
        abstract = True
        ordering = ['title']

    def __str__(self):
        return self.title
    

class Anime(Product):
    pass
