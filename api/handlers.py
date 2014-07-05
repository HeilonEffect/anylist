from piston.handler import BaseHandler
from piston.utils import validate

from myapp.models import *
from myapp.forms import *


class ProductHandler(BaseHandler):
	allowed_methods = ('GET', 'POST', 'PUT', )
	model = Product
	fields = ('id', 'title', 'description', 'old_limit', 'avatar', 'category', ('genres', ('name')))

	def read(self, request, product_id=None):
		'''
		Returns a single post if `product_id` is given,
		otherwise a subset
		'''
		base = Product.objects

		if product_id:
			return base.get(id=product_id)
		else:
			return base.all()

	@validate(AddProductForm, 'POST')
	def create(self, request):
		if request.content_type:
			data = request.data

			self.model.objects.create(**data)

			return rc.CREATED

	@validate(AddProductForm, 'PUT')
	def update(self, request, product_id):
		if request.content_type:
			data = request.data

			self.model.objects.filter(id=product_id).update(**data)
			return rc