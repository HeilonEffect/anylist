from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(CategoryGroup)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreGroup)
admin.site.register(Employ)
admin.site.register(Status)
admin.site.register(Raiting)
admin.site.register(Product)