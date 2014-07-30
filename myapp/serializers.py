from django.contrib.auth.models import User

from rest_framework import serializers

from .models import (
    CategoryGroup, Product, Raiting,  GenreGroup, UserList, Genre, Serie,
    SeriesGroup)


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
    # series = serializers.IntegerField(
    #     source='serie_set.count', read_only=True, required=False)

    class Meta:
        model = Product
        ordering = ('title',)
        fields = ('title', 'description', 'avatar', 'url',
                  'old_limit', 'category', 'genres', 'genres_list',)


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
    # series = serializers.PrimaryKeyRelatedField(
    #     many=True, source='serie_set', read_only=True)

    class Meta:
        model = SeriesGroup
        fields = ('id', 'number', 'name', 'series', 'product',)
