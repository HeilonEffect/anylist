from django.db import models
from anylist.settings import MEDIA_ROOT


class Raiting(models.Model):
	''' Возрастные ограничения '''
	name = models.CharField(max_length=5)
	tooltip = models.CharField(max_length=45)

	def __str__(self):
		return self.name


#-----------------------------
class ImgType(models.Model):
	''' Cosplay, Avatar, Art '''
	name = models.CharField(max_length=10)


class AnimeType(models.Model):
	''' Сколько сезонов сериала понятно на основе названия '''
	name = models.CharField(max_length=20, unique=True)
#-------------------------


class Picture(models.Model):
	img = models.URLField()
	img_type = models.ForeignKey(ImgType)


class Category(models.Model):
	''' Примеры - <for man>, <crime>, <pron>, <fantastic>, <life> '''
	name = models.CharField(max_length=30, unique=True)

	def _genres(self):
		return Genre.objects.filter(category=self.id)
	genres = property(_genres)

	def __str__(self):
		return self.name


class Genre(models.Model):
	name = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=255, blank=True)
	category = models.ForeignKey(Category)

	def __str__(self):
		return self.name


#----------------------------------
class Profession(models.Model):
	''' Список профессий (звукорежиссер, сценарист, сейю, мангака) '''
	name = models.CharField(max_length=140)


class Employer(models.Model):
	''' Работавший над фильмом, аниме, мангой '''
	name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30)
	avatar = models.URLField()	# а там картинка
	profession = models.ManyToManyField(Profession)


class Studio(models.Model):
	name = models.CharField(max_length=140)
	foundation_date = models.DateField(blank=True)

	def __str__(self):
		return self.name
#------------------------------


class Hero(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	avatars = models.ManyToManyField(Picture)


class Anime(models.Model):
	jp_name = models.CharField(max_length=255)
	ru_name = models.CharField(max_length=255, blank=True)
	en_name = models.CharField(max_length=255, blank=True)

	description = models.TextField(blank=True)
	genres = models.ManyToManyField(Genre)
	studios = models.ManyToManyField(Studio)
	
	avatars = models.ManyToManyField(Picture)

	# номер сезона
	season = models.IntegerField(blank=True)

	# Статус можно вычислить и на основе этих данных
	start_date = models.DateTimeField(blank=True)
	end_date = models.DateTimeField(blank=True)
	num_series = models.IntegerField(blank=True)

	length_episode = models.IntegerField(default=24)
	period = models.IntegerField(default=7)	# периодичность (в неделю, месяц)

	raiting = models.ForeignKey(Raiting)
	limitation = models.IntegerField()	# возрастные ограничения

	typ = models.ForeignKey(AnimeType)

	heroes = models.ManyToManyField(Hero, blank=True)


class Opening(models.Model):
	url = models.URLField(unique=True)
	anime = models.ForeignKey(Anime)
	number = models.IntegerField(default=1)


class Ending(models.Model):
	url = models.URLField(unique=True)
	anime = models.ForeignKey(Anime)
	number = models.IntegerField(default=1)


class Preview(models.Model):
	url = models.URLField(unique=True)
	anime = models.ForeignKey(Anime)


class AnimeSeries(models.Model):
	''' Номер и название каждой серии аниме '''
	name = models.CharField(max_length=255, blank=True)
	number = models.IntegerField()


class AMW(models.Model):
	name = models.CharField(max_length=255)
	url = models.URLField(unique=True)
	anime = models.ManyToManyField(Anime)


# Две таблицы ниже - меню стартовой страницы
class Categories(models.Model):
	name = models.CharField(max_length=40, unique=True)

	def _values(self):
		return SubCategories.objects.filter(categories=self.id)
	values = property(_values)


class SubCategories(models.Model):
	name = models.CharField(max_length=30, unique=True)
	img = models.CharField(max_length=100, unique=True)	# ccылка на картинку
	url = models.CharField(max_length=50, unique=True)
	categories = models.ForeignKey(Categories)