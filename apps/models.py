import re
import sys

from django.db import models
from django.db.models import Q

import floppyforms as forms
from select2light.models import Select2ModelChoiceField, Select2ModelMultipleChoiceField

from anylist.settings import MEDIA_ROOT, MEDIA_URL, STATICFILES_DIRS


reload(sys)
sys.setdefaultencoding('utf-8')


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
#    objects = GenreManager()
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

    def get_absolute_url(self):
        return '%i-%s' % (self.id, ''.join(re.split(r'[ :_]', self.title)))

    def avatar_path(self):
        return '/static/' + str(self.avatar).split('/')[-1]
    
    class Meta:
        abstract = True
        ordering = ['title']

    def __unicode__(self):
        return self.title


class Anime(Product):
    def get_absolute_url(self):
        res = 'anime/' + super(Anime, self).get_absolute_url()
        return res


class Manga(Product):
    pass
