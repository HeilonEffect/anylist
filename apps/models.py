from django.db import models
from django.core.exceptions import ValidationError


class GenreGroup(models.Model):
    ''' Группа жанров, объединенная одним признаком '''
    group_name = models.CharField(unique=True)

    def _genres(self):
        return Genre.objects.filter(id=self.id)
    genres = property(_genres)


class Genre(models.Model):
    name = models.CharField(max_length=140, unique=True)
    group = models.ForeignKey(GenreGroup)

    def __str__(self):
        return self.name


class Copyrighter(models.Model):
    ''' Описывает производителя '''
    name = models.CharField(max_length=255, unique=True)
    logotype = models.ImageField(blank=True)
    start_date = models.DateField(blank=True)

    class Meta:
        abstract = True


class Product(models.Model):
    ''' Описывает одиночный объект '''
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    url = models.CharField(max_length=255, unique=True)

    avatar = models.ImageField()

    start_date = models.DateField(blank=True)   # если пусто - то анонс
    old_limit = models.SmallInteger(validators=[validate_old_limit])
    
    class Meta:
        abstract = True
        ordering = ['title']

    def __str__(self):
        return self.title
    

def validate_old_limit(value):
    if value > 21 or value < 0:
        raise ValidationError(
            "Old limit don't mutch great, then 21 and small, then 0")