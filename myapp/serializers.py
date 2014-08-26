from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.Field('get_absolute_url')
    avatar = serializers.Field('avatar_path')
    icon = serializers.Field('icon_path')

    class Meta:
        model = Category
        fields = ('id', 'name', 'avatar', 'icon', 'url',)


class GenreSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Genre
        fields = ('id', 'name', 'count',)


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.Field(source='get_absolute_url')
    genres = serializers.PrimaryKeyRelatedField(many=True)
    old_limit = serializers.PrimaryKeyRelatedField()
    limit = serializers.CharField(source='old_limit.name', read_only=True)
    genres_list = GenreSerializer(
        source='genres.values', required=False, read_only=True)
    series_count = serializers.Field(source='series_count')
    avatar_path = serializers.Field(source='avatar_path')

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'avatar', 'url',
                  'old_limit', 'category', 'genres', 'genres_list',
                  'series_count', 'limit', 'avatar_path',)


class UpdateProductSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'avatar', 'old_limit',
                  'category', 'genres',)


class GenreGroupSerializer(serializers.ModelSerializer):
    genres = serializers.Field(source='_genres')
    categories = serializers.Field(source='category_group')

    class Meta:
        model = GenreGroup
        fields = ('name', 'genres', 'categories',)


class RaitingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Raiting
        fields = ('id', 'name',)


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class SeriesSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=['%d.%m.%Y, %H:%M:%S', '%Y-%m-%d'],
                                       required=False)

    class Meta:
        model = Serie
        fields = ('id', 'number', 'name', 'season', 'start_date', 'length',)


class SeasonsSerializer(serializers.ModelSerializer):
    series = serializers.Field(source='serie_set.values')

    class Meta:
        model = SeriesGroup
        fields = ('id', 'number', 'name', 'series', 'product',)


class UserListSerializer(serializers.ModelSerializer):
    '''
    user не выдаётся, т.к. каждый может получить только свой список
    '''
    product = serializers.Field(source='product._values')
    series = serializers.Field(source='serielist_set.count')

    class Meta:
        model = UserList
        fields = ('id', 'product', 'score', 'status', 'series',)


class SerieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SerieList
        fields = ('id', 'serie', 'user_list', 'like',)


class SearchSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='title')
    link = serializers.Field(source='get_absolute_url')

    class Meta:
        model = Product
        fields = ('name', 'link',)


class UserStatisticSerializer(serializers.Serializer):
    category = serializers.CharField()
    status = serializers.CharField()
    count = serializers.IntegerField()
    url = serializers.CharField()


class EmployProductSerializer(serializers.ModelSerializer):
    ''' Предназначен для показа роли служебного персонажа в каждом
    конкретном продукте '''
    url = serializers.Field(source='get_absolute_url')
    class Meta:
        model = Product
        fiels = ('title', 'avatar_path', 'url', 'role',)

class CreatorSerializer(serializers.ModelSerializer):
    url = serializers.Field(source='get_absolute_url')
    avatar_path = serializers.Field()
    roles = serializers.Field()

    class Meta:
        model = Creator
        fields = ('name', 'avatar', 'url', 'avatar_path', 'roles',)


class CreatorEmploysSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='creator.name')
    avatar_path = serializers.Field(source='creator.avatar_path')
    employ = serializers.Field(source='employ.name')
    url = serializers.Field(source='creator.get_absolute_url')

    class Meta:
        model = CreatorEmploys
        fields = ('name', 'avatar_path', 'employ', 'url',)


class HeroSerializer(serializers.ModelSerializer):
    actor = serializers.PrimaryKeyRelatedField(required=False)
    url = serializers.Field(source='get_absolute_url')
    avatar_path = serializers.Field(source='avatar_path')
    description = serializers.CharField(required=False)
    roles = serializers.Field()

    class Meta:
        model = Hero
        fields = ('name', 'description', 'avatar', 'actor', 'url', 'avatar_path', 'roles',)


class EmploySerializer(serializers.ModelSerializer):

    class Meta:
        model = Employ
        fields = ('id', 'name',)


class SearchCreatorSerializer(serializers.ModelSerializer):
    avatar = serializers.Field(source='avatar_path')

    class Meta:
        model = Creator
        fields = ('id', 'name', 'avatar',)


class SearchHeroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hero
        fields = ('id', 'name',)