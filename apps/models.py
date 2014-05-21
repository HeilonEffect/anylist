import re

from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

import select2.fields
import select2.models
import floppyforms as forms
from select2light.models import Select2ModelChoiceField, Select2ModelMultipleChoiceField

from anylist.settings import MEDIA_ROOT


class GenreGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def _genres(self):
        return Genre.objects.filter(group=self.id)
    genres = property(_genres)

    def __unicode__(self):
        return self.name



class GenreManager(models.Manager):
    def as_choices(self):
        for genre in self.all():
            yield (genre.pk, unicode(genre))
    

class Genre(models.Model):
    name = models.CharField(max_length=140, unique=True)
    objects = GenreManager()
    group = models.ForeignKey(GenreGroup)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    ''' Description single product '''
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    genres = Select2ModelMultipleChoiceField(Genre)

    avatar = models.FileField(upload_to=MEDIA_ROOT)

    start_date = models.DateField(blank=True)   # if emty - then it is anounce
    old_limit = models.PositiveSmallIntegerField()

#    category = models.ForeignKey(Category, blank=True)

    def get_absolute_url(self):
        return ''.join(re.split(r'[ :_]', self.title))
    
    class Meta:
        abstract = True
        ordering = ['title']

    def __unicode__(self):
        return self.title


class Anime(Product):
    pass
