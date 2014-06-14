import json

from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'products': reverse('product-list', request=request),
		'series': reverse('series-list', request=request)
	})


class ProductList(generics.ListCreateAPIView):
	model = Production
	serializer_class = ProductSerializer


class StatusList(generics.ListCreateAPIView):
	model = Status
	serializer_class = StatusSerializer


class SeriesView(generics.ListAPIView):
	queryset = Serie.objects.all()
	
	def get_queryset(self):
		if self.kwargs.get('number'):
			return self.queryset.filter(
				season__product__id=self.kwargs['pk'],
				season__number=self.kwargs['number'])
		else:
			return self.queryset.filter(
				season__product__id=self.kwargs['pk']).order_by('-season__id', '-number')
	serializer_class = SerieSerializer


