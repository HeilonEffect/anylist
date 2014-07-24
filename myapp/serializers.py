from django.contrib.auth.models import User

from rest_framework import serializers

from .models import CategoryGroup, Product, Raiting,  GenreGroup


class CategorySerializer(serializers.ModelSerializer):
	categories = serializers.Field(source='categories_json')
	class Meta:
		model = CategoryGroup
		fields = ('name', 'categories',)


class ProductSerializer(serializers.ModelSerializer):
	avatar_path = serializers.Field(source='avatar_path', required=False)
	url = serializers.Field(source='get_absolute_url')
	genres = serializers.Field(source='_genres')
	old_limit = serializers.Field(source='_old_limit')
	class Meta:
		model = Product
		fields = ('title', 'description', 'avatar', 'url', 'genres', 'old_limit', 'category', 'avatar_path')


class GenreGroupSerializer(serializers.ModelSerializer):
	# genres = serializers.HyperLinkedIdentityField('genres', view_name='genres_list', lookup_field='name')
	genres = serializers.Field(source='_genres')
	class Meta:
		model = GenreGroup
		fields = ('name', 'genres',)


class RaitingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Raiting
		fields = ('id', 'name',)


class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username',)