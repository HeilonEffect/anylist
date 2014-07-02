from django.shortcuts import render

from rest_framework import generics

from .models import *
from .serializers import *
# Create your views here.

class APISeriesView(generics.ListAPIView):
	serializer_class = SeriesSerializer
	queryset = Serie.objects.all()
	def get_queryset(self):
		return Serie.objects.filter(product__id=self.kwargs['pk'])