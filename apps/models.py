import re

from django.db import models
from django.contrib.auth.models import User

from anylist.settings import MEDIA_ROOT, MEDIA_URL, STATICFILES_DIRS


class GenreGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def _genres(self):
        return Genre.objects.filter(group=self.id)
    genres = property(_genres)
    @genres.setter
    def set_genres(self, value):
        self.genres = value

    def __unicode__(self):
        return self.name


class Raiting(models.Model):
    name = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=140, unique=True)
    group = models.ForeignKey(GenreGroup)
    eng_name = models.CharField(max_length=140, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class ThematicGroup(models.Model):
    ''' Разделы сайта, объединенниые в группы '''
    name = models.CharField(max_length=50, unique=True)

    def _children(self):
        return Category.objects.filter(group=self.id)
    children = property(_children)

    def __str__(self):
        return self.name


class Category(models.Model):
    ''' Здесь мы перечисляем названия разделов сайта '''
    name = models.CharField(max_length=40, unique=True) # на английском
    avatar = models.FileField(upload_to=MEDIA_ROOT)
    group = models.ForeignKey(ThematicGroup)

    def get_absolute_url(self):
        return self.name.lower()

    def __str__(self):
        return self.name

    def avatar_path(self):
        return '/static/' + str(self.avatar).split('/')[-1]


class Product(models.Model):
    ''' Description single product '''
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    genres = models.ManyToManyField(Genre)

    avatar = models.FileField(upload_to=MEDIA_ROOT)

    start_date = models.DateField(null=True, blank=True)   # if emty - then it is anounce
    old_limit = models.ForeignKey(Raiting)

    def get_absolute_url(self):
        return '%i-%s' % (self.id, ''.join(re.split(r'[ :_!]', self.title)))

    def avatar_path(self):
        return '/static/' + str(self.avatar).split('/')[-1]

    class Meta:
        abstract = True
        ordering = ['title']

    def __str__(self):
        return self.title


#class Profile(models.Model):
 #   user = models.OneToOneField(User)
  #  avatar = models.FileField(upload_to=MEDIA_ROOT, blank=True, null=True)

# Таблица персонажей одна для всех, уникальные черты
# будут доступны через связи с ней
class Hero(models.Model):
    full_name = models.CharField(max_length=255)
    avatar = models.FileField(upload_to=MEDIA_ROOT)
    description = models.TextField()


class Anime(Product):
    def get_absolute_url(self):
        res = 'anime/' + super(Anime, self).get_absolute_url()
        return res


#class AnimeSeason(Season):
 #   link = models.ForeignKey(Anime)


#class AnimeSeries(Serie):
 #   season = models.ForeignKey(AnimeSeason)


#class AnimeSeries(models.Model):
 #   ''' Описывает одну серию аниме '''
#    number = models.PositiveSmallIntegerField()
#    name = models.CharField(max_length=255)
#    pub_date = models.DateTimeField(null=True)

#    anime = models.ForeignKey(Anime)


class Manga(Product):
    def get_absolute_url(self):
        res = 'manga/' + super(Manga, self).get_absolute_url()
        return res
