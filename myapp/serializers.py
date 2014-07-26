from django.contrib.auth.models import User

from rest_framework import serializers

from .models import (
    CategoryGroup, Product, Raiting,  GenreGroup, UserList, Genre)


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
    genres = GenreSerializer(many=True)
    # genres = serializers.RelatedField(many=True)
    old_limit = serializers.RelatedField()
    series = serializers.IntegerField(source='serie_set.count', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'description', 'avatar', 'url',
                  'old_limit', 'category', 'genres', 'series',)


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


class ProductDetailSerializer(serializers.ModelSerializer):

    '''
    Для одиночного продукта
    '''
    class Meta:
        model = Product
        fields = ('title', 'description', 'avatar', 'category', )
