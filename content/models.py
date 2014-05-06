from django.db import models
from django.contrib import admin

# Create your models here.
class NavigationItem(models.Model):
	url = models.CharField(max_length=60)
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


class NavigationSubItem(models.Model):
	head = models.ForeignKey(NavigationItem)
	url = models.CharField(max_length=60)
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


# Admin interface
class NavigationItemAdmin(admin.ModelAdmin):
	fields = ('name', 'url',)

class NavigationSubItemAdmin(admin.ModelAdmin):
	fields = ('head', 'name', 'url',)

admin.site.register(NavigationItem, NavigationItemAdmin)
admin.site.register(NavigationSubItem, NavigationSubItemAdmin)
