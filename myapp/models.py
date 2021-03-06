import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

# from cacheops import cached_as
from easy_thumbnails.signals import saved_file
from rest_framework.authtoken.models import Token

from anylist.settings import MEDIA_ROOT


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(saved_file)
def generate_thumbnails_async(sender, fieldfile, **kwargs):
    tasks.generate_thumbnails.delay(
        model=sender, pk=fieldfile.instance.pk,
        field=fieldfile.field.name)

class TemplateModel(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CategoryGroup(TemplateModel):
    class Meta:
        ordering = ('name',)


class Raiting(TemplateModel):
    pass


class Category(TemplateModel):
    avatar = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)
    icon = models.ImageField(upload_to=MEDIA_ROOT, blank=True, null=True)
    group = models.ForeignKey(CategoryGroup)

    def avatar_path(self):
        return '/media/' + self.avatar.url.split('/')[-1]

    def icon_path(self):
        return '/media/' + self.icon.url.split('/')[-1]

    def get_absolute_url(self):
        return '/%s' % ''.join(self.name.lower().split(' '))

    class Meta:
        ordering = ('name',)


class Genre(TemplateModel):
    class Meta:
        ordering = ('name',)


class GenreGroup(TemplateModel):
    category = models.ForeignKey(CategoryGroup)
    genres = models.ManyToManyField(Genre)

    def category_group(self):
        return map(lambda item: item['id'],
                   self.category.category_set.values('id'))

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

    def roles(self):
        ''' Список продуктов, к созанию которых данный персонаж имеет
        отношение и его роль в них '''
        p = list(map(lambda item: item['id'],
                     self.creatoremploys_set.values('id')))
        p = Product.objects.filter(creators__in=p)

        def mapper(item):
            result = {}
            result['url'] = item.get_absolute_url()
            result['avatar_path'] = item.avatar_path()
            result['title'] = item.title
            result['role'] = item.creators.get(creator=self).employ.name
            return result

        p = map(mapper, p)
        return p

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

    def roles(self):
        p = self.product_set.all()

        def f(item):
            result = {}
            result['title'] = item.title
            result['avatar_path'] = item.avatar_path()
            result['url'] = item.get_absolute_url()
            return result

        p = map(f, p)
        return p

    def get_absolute_url(self):
        return '/hero/%d-%s/' % (self.id, ''.join(
            re.split('[ :()-]', self.name)))


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    # alt_names = models.ManyToManyField(AltName)
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
                'series_count': self.series_count(), 'category': self.category.id}

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
        return '/product/%d-%s/' % (self.id, title)

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

    def __str__(self):
        return '%s: season %d' % (self.product, self.number)


class SerieManager(models.Manager):

    def all_series(self, product):
        return Serie.objects.filter(season__product=product).order_by(
            '-season__number', '-number')


class Serie(models.Model):
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    season = models.ForeignKey(SeriesGroup, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    length = models.PositiveSmallIntegerField(blank=True, null=True)

    objects = models.Manager()
    manager = SerieManager()

    class Meta:
        ordering = ('-number', )

    def __str__(self):
        return 'Serie: %s' % self.number


class Status(TemplateModel):
    pass


class UserListManager(models.Manager):
    def get_or_create(self, **kwargs):
        try:
            p = self.get(**kwargs)
            return (p, False,)
        except ObjectDoesNotExist as e:
            kwargs['product'] = Product.objects.get(id=kwargs['product__id'])
            kwargs['status'] = Status.objects.get(name='Watch')
            del kwargs['product__id']
            p = self.create(**kwargs)
            return  (p, True,)


class UserList(models.Model):
    user = models.ForeignKey(User)
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    status = models.ForeignKey(Status)
    product = models.ForeignKey(Product)

    objects = models.Manager()
    manager = UserListManager()

    def add_watched_serie(self, **kwargs):
        ''' Добавляем одну серию в список просмотренных.
        Возвращаем экземпляр объекта SerieList '''
        try:
            self.product.seriesgroup_set.filter(id=kwargs['serie'].season.id)
            p = SerieList.objects.create(user_list=self,
                                         serie=kwargs['serie'],
                                         like=kwargs.get('like'))
            self.serielist_set.add(p)
            return p
        except ObjectDoesNotExist as e:
            pass

    def del_watched_serie(self, **kwargs):
        ''' Удаляем серию из списка просмотренных '''
        SerieList.objects.filter(user_list=self,
                                 serie=kwargs['serie']).delete()

    def series(self):
       return SerieList.objects.filter(user_list=self)

    def __str__(self):
        return '%s: %s' % (self.status.name, self.product.title)


class SerieListManager(models.Manager):
    def watched_series(self, user, product):
        return self.filter(user_list__user=user, user_list__product=product
        ).order_by('-serie__season__number', '-serie__number')


class SerieList(models.Model):
    serie = models.ForeignKey(Serie)
    user_list = models.ForeignKey(UserList)
    like = models.NullBooleanField()

    objects = models.Manager()
    manager = SerieListManager()

    def __str__(self):
        return str(self.serie)
