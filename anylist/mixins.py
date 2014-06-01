from django.db.models import F, Q

from apps.models import *

class BasePageMixin(object):
	''' Содержит одинаковые для всех классов приложения операции '''
	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		context['header'] = self.header
		context['genres'] = Genre.objects.all()
		context['raiting'] = Raiting.objects.all()
		context['nav_groups'] = ThematicGroup.objects.all()
		try:
			context['category'] = Category.objects.get(name=self.category)
		except AttributeError as e:
			print('Category is not defined')
		return context


class DetailPageMixin(object):
	def get_context_data(self, **kwargs):
		context = super(DetailPageMixin, self).get_context_data(**kwargs)
		context['nav_groups'] = ThematicGroup.objects.all()
		context['category'] = Category.objects.get(name=self.category)
		context['url'] = self.model.objects.get(
			id=self.kwargs['pk']).get_absolute_url()
		return context


class ChildDetailPageMixin(object):
	def get_queryset(self):
		return self.model.objects.filter(link__id=self.kwargs['pk'])
	
	def get_context_data(self, **kwargs):
		context = super(ChildDetailPageMixin, self).get_context_data(**kwargs)
		context['nav_groups'] = ThematicGroup.objects.all()
		context['category'] = Category.objects.get(name=self.category)
		context['num_season'] = self.get_queryset().count()
		
		context['url'] = self.parent_model.objects.get(
			id=self.kwargs['pk']).get_absolute_url()
		return context


class ListPageMixin(object):
	def get_queryset(self):
		if not self.queryset:
			self.queryset = [p.link for p in self.model1.objects.all()]
			return self.queryset
		else:
			return self.queryset

	def get_context_data(self, **kwargs):
		context = super(ListPageMixin, self).get_context_data(**kwargs)
		context['nav_groups'] = ThematicGroup.objects.all()
		context['raiting'] = Raiting.objects.all()
		context['header'] = self.header
		context['category'] =\
			Category.objects.get(name=self.category).name.lower()

		context['genre_groups'] = []

		# вычисляем, сколько раз встретился каждый жанр
		# на данной странице (фича аля яндекс.маркет)
		num_genres = {}
		for genre in Genre.objects.all():
			num_genres[genre.name] = 0

		for item in self.queryset:
			genres = item.genres.all()
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
		tmp = self.args[0].split('/')

		# избавляемся от пустых значений
		tmp = list(filter(lambda item: item, tmp))

		keys = tmp[::2]
		values = [item.split(',') for item in tmp[1::2]]
		qs = dict(zip(keys, values))

		tmp = qs.get('old_limit')
		q = []
		if tmp:
			q, *rest = tmp
			q = Q(link__old_limit__name=q)
			for item in rest:
				q = q.__or__(Q(link__old_limit__name=item))

		if isinstance(q, list):
			q = self.model1.objects
		else:
			q = self.model1.objects.filter(q)
		
		tmp = qs.get('genres')
		if tmp:
			for item in tmp:
				q = q.filter(link__genres__name=item)
		self.queryset = q
		self.queryset = [item.link for item in self.queryset]
		return self.queryset
