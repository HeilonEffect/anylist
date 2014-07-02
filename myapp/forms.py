from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import *

class AddProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ('title', 'description', 'avatar', 'category', 'genres', )


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()


class AddSerieForm(ModelForm):
	class Meta:
		model = Serie
		fields = '__all__'