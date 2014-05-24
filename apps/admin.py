from django.contrib import admin
from .models import Genre, GenreGroup, Raiting, ThematicGroup, Category

# Register your models here.
admin.site.register(Genre)
admin.site.register(GenreGroup)
admin.site.register(Raiting)
admin.site.register(ThematicGroup)
admin.site.register(Category)