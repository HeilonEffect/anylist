from django import forms
from django.forms import ModelForm

from .models import *

class AddProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ('title', 'description', 'avatar', 'category', 'genres', )
