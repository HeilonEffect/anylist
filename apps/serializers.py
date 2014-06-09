from .models import Production
from rest_framework import serializers

class ProductSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Production
		fields = ('title',)
