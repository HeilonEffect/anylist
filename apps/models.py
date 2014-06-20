import re

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

from easy_thumbnails.files import get_thumbnailer

from anylist.settings import MEDIA_ROOT, MEDIA_URL, first_static


class GenreGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def _genres(self):
        return Genre.objects.filter(group=self.id)
    genres = property(_genres)
    @genres.setter
    def set_genres(self, value):
        self.genres = value

    def __str__(self):
        return self.name


class Raiting(models.Model):
    name = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=140, unique=True)
    group = models.ForeignKey(GenreGroup)

    def __str__(self):
        return "%i-%s" % (self.id, self.name)


# возможно избыточная структура и её следует удалить
class ThematicGroup(models.Model):
    ''' Разделы сайта, объединенные в группы '''
    name = models.CharField(max_length=50, unique=True)

    def _children(self):
        return Category.objects.filter(group=self.id)
    children = property(_children)

    def _dashs(self):
        return DashBoard.objects.filter(group=self.id)
    dashs = property(_dashs)

    def __str__(self):
        return self.name


class DashBoard(models.Model):
    name = models.CharField(max_length=30, unique=True)
    icon = models.ImageField(upload_to=MEDIA_ROOT)
    group = models.ForeignKey(ThematicGroup)

    def get_absolute_url(self):
        return self.name.lower()

    def __str__(self):
        return self.name

    def avatar_path(self):
        return '/media/' + str(self.icon).split('/')[-1]


class Category(models.Model):
    ''' Здесь мы перечисляем названия разделов сайта '''
    name = models.CharField(max_length=40, unique=True) # на английском
    avatar = models.ImageField(upload_to=MEDIA_ROOT)
    group = models.ForeignKey(ThematicGroup)

    def get_absolute_url(self):
        return self.name.lower()

    def __str__(self):
        return self.name

    def avatar_path(self):
        return '/media/' + str(self.avatar).split('/')[-1]


class Production(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)

    genres = models.ManyToManyField(Genre)
    old_limit = models.ForeignKey(Raiting)

    pub_date = models.DateTimeField(auto_now=True)

    avatar = models.ImageField(upload_to=MEDIA_ROOT)

#    def avatar_path(self):
#        return '/media/' + str(self.avatar).split('/')[-1]

    def avatar_path(self):
        options = {'size': (250, 310), 'crop': True}
        thumb_url = get_thumbnailer(self.avatar).get_thumbnail(options).url
        return '/media/' + thumb_url.split('/')[-1]

    def get_category(self):
        for category in Category.objects.all():
            if category.name.lower() in dir(self):
                return str(category.name.lower())

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '%i-%s' % (self.id, ''.join(re.split(r"[- &'(!):]", self.title)))


# Таблица персонажей одна для всех, уникальные черты
# будут доступны через связи с ней
# пока не используется
class Hero(models.Model):
    full_name = models.CharField(max_length=255)
    avatar = models.FileField(upload_to=MEDIA_ROOT)
    description = models.TextField()


class Anime(models.Model):
    link = models.OneToOneField(Production)

    def __str__(self):
        return self.link.title


class Manga(models.Model):
    link = models.OneToOneField(Production)

    def __str__(self):
        return self.link.title


# Насчёт названия сезона - везде, где у сезона есть название - 
# можно создать новый Production
class Serie(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255, null=True)
    num_season = models.PositiveSmallIntegerField(null=True, blank=True)
    product = models.ForeignKey(Production)
    start_date = models.DateField(null=True, blank=True)
    length = models.IntegerField(null=True)

    def __str__(self):
        return "%i-%s" % (self.number, self.name)

    class Meta:
        ordering = ['-number']


class Status(models.Model):
    ''' Запланировано, Смотрю, Пересматриваю, Просмотрел, Отложил, Бросил '''
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

    def _alt_name(self):
        return self.name.lower()
    alt_name = property(_alt_name)


class ListedProduct(models.Model):
    ''' Продукт, который находится в списке у пользователя.
    Поле <series> - список просмотренных/прочитанных пользователем
    серий/глав '''
    product = models.ForeignKey(Production)
    status = models.ForeignKey(Status, default=1)
    series = models.ManyToManyField(Serie, null=True)
    user = models.ForeignKey(User, null=True)  # null=True - на самом деле нет
    score = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.product.title
