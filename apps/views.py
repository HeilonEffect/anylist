from django.shortcuts import render

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from .models import Production
from .serializers import ProductSerializer


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'products': reverse('product-list', request=request),
		'search': reverse('search-list', request=request)
	})


class ProductList(generics.ListCreateAPIView):
	model = Production
	serializer_class = ProductSerializer
