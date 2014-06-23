import itertools
import json
import functools
import operator

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q
from django.http import HttpResponseNotFound

from apps.forms import *
from apps.models import *


Types = {'anime': Anime, 'manga': Manga, 'criminalystic': Criminalystic}


class BasePageMixin(object):
	def dispatch(self, *args, **kwargs):
		if 'category' not in kwargs or kwargs['category'] not in Types:
			return HttpResponseNotFound('<h1>Page Not Found</h1>')
		else:
			return super(BasePageMixin, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		return context


class ListPageMixin(object):
	model = Production
	template_name = 'list.html'

	def get_queryset(self):
		if not self.queryset:
			self.queryset = [p.link for p in Types[self.kwargs['category']].objects.all()]
			return self.queryset
		else:
			return self.queryset


	def get_context_data(self, **kwargs):
		context = super(ListPageMixin, self).get_context_data(**kwargs)
		context['raiting'] = Raiting.objects.all()
		context['header'] = 'This list of %s' % self.kwargs['category']
		context['nav_groups'] = ThematicGroup.objects.all()

		context['listed'] =\
			[item.product for item in ListedProduct.objects.filter(
			user=context['view'].request.user.id)]

		context['category'] = self.kwargs['category']

		context['genre_groups'] = []

		# вычисляем, сколько раз встретился каждый жанр
		# на данной странице (фича аля яндекс.маркет)
		num_genres = {}
		for genre in Genre.objects.all():
			num_genres[genre.name] = 0

		for item in self.queryset:
			genres = item.genres.all()
			#genres = item.genres.count())
			for genre in genres:
				num_genres[genre.name] += 1

		# число жанров будет пересчитываться,
		# ибо содержимое страницы непостоянно в реальном времени
		for group in self.genre_groups:
			p = GenreGroup.objects.get(name=group)

			g = []
			for item in p.genres:
				item.__setattr__('count', num_genres[item.name])
				g.append(item)
			d = {'name': p.name, 'genres': g}
			context['genre_groups'].append(d)

		for item in context['raiting']:
			item.count = 0
			for val in self.queryset:
				if val.old_limit == item:
					item.count += 1
		return context


class BaseChoiceMixin(ListPageMixin):

	def get_queryset(self):
		qs = {}
		tmp = self.kwargs['args'].split('/')

		# избавляемся от пустых значений
		tmp = list(filter(lambda item: item, tmp))

		# преобразовываем пары в словарь
		qs = dict(zip(tmp[::2],  [item.split(',') for item in tmp[1::2]]))

		tmp = qs.get('old_limit')
		q = []
		f = lambda item: Q(link__old_limit__name=item)
		if tmp:
			q = functools.reduce(operator.or_, map(f, tmp))

		if isinstance(q, list):
			q = Types[self.kwargs['category']].objects
		else:
			q = Types[self.kwargs['category']].objects.filter(q)

		tmp = qs.get('genres')
		if tmp:
			for item in tmp:
				q = q.filter(link__genres__name=item)
		self.queryset = q
		self.queryset = [item.link for item in self.queryset]
		return self.queryset
