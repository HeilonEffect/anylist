from .models import *
from rest_framework import serializers

class SeriesSerializer(serializers.ModelSerializer):
	class Meta:
		models = Serie
		fields = ('number', 'num_season', 'name', 'start_date', )