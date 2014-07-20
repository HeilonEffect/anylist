from rest_framework import serializers

from .models import CategoryGroup, Product, Raiting,  GenreGroup


class CategorySerializer(serializers.ModelSerializer):
	categories = serializers.Field(source='categories_json')
	class Meta:
		model = CategoryGroup
		fields = ('name', 'categories',)


class ProductSerializer(serializers.ModelSerializer):
	avatar = serializers.Field(source='avatar_path')
	url = serializers.Field(source='get_absolute_url')
	genres = serializers.Field(source='_genres')
	old_limit = serializers.Field(source='_old_limit')
	class Meta:
		model = Product
		fields = ('title', 'description', 'avatar', 'url', 'genres', 'old_limit',)


class GenreGroupSerializer(serializers.ModelSerializer):
	genres = serializers.Field(source='_genres')
	class Meta:
		model = GenreGroup
		fields = ('name', 'genres',)


class RaitingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Raiting
		fields = ('name',)