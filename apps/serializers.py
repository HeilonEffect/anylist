from .models import *
from rest_framework import serializers

class ProductSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Production
		fields = ('title',)


class StatusSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Status
		fields = ('name',)


class SerieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Serie
		fields = ('id', 'number', 'name', 'start_date', 'length')
