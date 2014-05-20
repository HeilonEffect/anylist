from django.contrib import admin
from .models import Genre, GenreGroup, Category

# Register your models here.
admin.site.register(Genre)
admin.site.register(GenreGroup)
admin.site.register(Category)