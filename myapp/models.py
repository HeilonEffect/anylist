from abc import ABCMeta, abstractmethod
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver

from easy_thumbnails.files import get_thumbnailer
from rest_framework.authtoken.models import Token

from anylist.settings import MEDIA_ROOT


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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

    def categories_json(self):
        p = Category.objects.filter(group=self.id)
        result = []
        for item in p:
            tmp = {}
            tmp['id'] = item.id
            tmp['name'] = item.name
            tmp['avatar'] = item.avatar_path()
            tmp['icon'] = item.icon_path()
            tmp['url'] = item.get_absolute_url()[1:]
            result.append(tmp)
        return result

    class Meta:
        ordering = ('name',)


class Raiting(TemplateModel):
    pass


class Category(TemplateModel):
    avatar = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)
    icon = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)
    group = models.ForeignKey(CategoryGroup)

    def avatar_path(self):
        options = {'size': (320, 480), 'crop': True}
        thumb_url = get_thumbnailer(self.avatar).get_thumbnail(options).url
        return '/media/' + thumb_url.split('/')[-1]

    def icon_path(self):
        options = {'size': (75, 75), 'crop': True}
        thumb_url = get_thumbnailer(self.icon).get_thumbnail(options).url
        return '/media/' + thumb_url.split('/')[-1]

    def get_absolute_url(self):
        return '/%s/' % ''.join(self.name.lower().split(' '))

    class Meta:
        ordering = ('name',)


class Genre(TemplateModel):
    count = 0
    class Meta:
        ordering = ('name',)


class GenreGroup(TemplateModel):
    category = models.ForeignKey(CategoryGroup)
    genres = models.ManyToManyField(Genre)

    def _genres(self):
        return self.genres.values('id', 'name')


class AltName(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Employ(TemplateModel):

    ''' Название профессии '''
    pass


class Creator(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)

    def get_absolute_url(self):
        return '/creator/%d-%s' % (
            self.id, ''.join(re.split('[ :()-]', self.name)))

    def __str__(self):
        return self.name

    def avatar_path(self):
        return '/media/%s' % str(self.avatar).split('/')[-1]


class CreatorEmploys(models.Model):
    employ = models.ForeignKey(Employ)
    creator = models.ForeignKey(Creator)

    def __str__(self):
        return '%s:%s' % (self.creator, self.employ)


class Hero(models.Model):

    ''' is_main_hero:
    True - Главный герой
    False - Не главный
    Null - Эпизодический '''
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    actor = models.ForeignKey(Creator, blank=True, null=True)
    avatar = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)
    is_main_hero = models.NullBooleanField()

    def __str__(self):
        return self.name

    def avatar_path(self):
        return '/media/%s' % str(self.avatar).split('/')[-1]

    def get_absolute_url(self):
        return '/hero/%d-%s/' % (self.id, ''.join(
            re.split('[ :()-]', self.name)))


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    alt_names = models.ManyToManyField(AltName)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=MEDIA_ROOT)

    category = models.ForeignKey(Category)
    genres = models.ManyToManyField(Genre)
    old_limit = models.ForeignKey(Raiting, null=True, blank=True)

    creators = models.ManyToManyField(CreatorEmploys)
    heroes = models.ManyToManyField(Hero)

    def series_count(self):
        return sum([
            item.serie_set.count() for item in self.seriesgroup_set.all()])

    def _values(self):
        return {'title': self.title, 'id': self.id, 'description': self.description,
                'avatar': self.avatar_path(), 'url': self.get_absolute_url(),
                'series_count': self.series_count()}

    def _series(self):
        return Serie.objects.filter(season__product=self.id).order_by(
            '-num_season', '-number')
    def _series_count(self):
        return Serie.objects.filter(season__product=self.id).count()
    series = property(_series)

    def _genres(self):
        return [item['name'] for item in self.genres.values('name')]

    def _category(self):
        return self.category.name

    def get_absolute_url(self):
        title = ''.join(re.split('[ :()-.!?]', self.title))
        return '%s%d-%s/' % (self.category.get_absolute_url(), self.id,
                            title)

    def avatar_path(self):
        return '/media/%s' % str(self.avatar).split('/')[-1]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class SeriesGroup(models.Model):
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    frozen = models.BooleanField(default=False)
    product = models.ForeignKey(Product)

    class Meta:
        ordering = ('-number',)


class Serie(models.Model):
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    season = models.ForeignKey(SeriesGroup, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    length = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ('-number', )

    def __str__(self):
        return 'Serie: %s' % (self.number)


class Status(TemplateModel):
    pass


class UserList(models.Model):
    user = models.ForeignKey(User)
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    status = models.ForeignKey(Status)
    product = models.ForeignKey(Product)

    def _series(self):
        return SerieList.objects.filter(user_list=self)
    series = property(_series)

    def __str__(self):
        return '%s: %s' % (self.status.name, self.product.title)


class SerieList(models.Model):
    serie = models.ForeignKey(Serie)
    user_list = models.ForeignKey(UserList)
    like = models.NullBooleanField()

    def __str__(self):
        return str(self.serie)
