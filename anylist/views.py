from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView

#from content.models import *
from menues.models import *


class BasePageMixin(object):

	def get_context_data(self, **kwargs):
		context = super(BasePageMixin, self).get_context_data(**kwargs)
		context['headers'] = NavigationMenu.objects.all()
		return context


def index(request):
	return render_to_response('base.html')


class CatalogView(BasePageMixin, TemplateView):
	template_name = 'base.html'


class CardView(BasePageMixin, TemplateView):
	tempalte_name = 'card.html'