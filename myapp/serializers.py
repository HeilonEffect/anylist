from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    categories = serializers.Field(source='categories_json')

    class Meta:
        model = CategoryGroup
        fields = ('name', 'categories',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.Field(source='get_absolute_url')
    genres = serializers.PrimaryKeyRelatedField(many=True)
    old_limit = serializers.PrimaryKeyRelatedField()
    genres_list = GenreSerializer(
        source='genres.values', required=False, read_only=True)
    series_count = serializers.Field(source='series_count')

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'avatar', 'url',
                  'old_limit', 'category', 'genres', 'genres_list', 'series_count',)


class GenreGroupSerializer(serializers.ModelSerializer):
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


class UserListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = UserList
        fields = ('user', 'score', 'status', 'product',)


class SeriesSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=['%d.%m.%Y, %H:%M:%S'],
                                       required=False)

    class Meta:
        model = Serie
        fields = ('number', 'name', 'season', 'start_date', 'length',)


class SeasonsSerializer(serializers.ModelSerializer):
    series = serializers.Field(source='serie_set.values')

    class Meta:
        model = SeriesGroup
        fields = ('id', 'number', 'name', 'series', 'product',)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserList
        fields = ('user', 'product', 'score', 'status',)


class SerieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerieList
        fields = ('serie', 'user_list', 'like',)


class SearchSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='title')
    link = serializers.Field(source='get_absolute_url')
    class Meta:
        model = Product
        fields = ('name', 'link',)