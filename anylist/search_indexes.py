from haystack import indexes
from apps.models import Production

class ProductionIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.CharField(model_attr='title')

	def get_model(self):
		return Production

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(title__contains='x.3')