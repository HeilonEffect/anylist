from django import forms
from django.forms import ModelForm
from django.forms.models import BaseModelFormSet

from apps.models import *


class AddForm(ModelForm):
	class Meta:
		model = Production


#class AddAnimeSeriesForm(ModelForm):
#	pub_date = forms.DateTimeField(
#		required=False, input_formats=['%Y/%m/%d %H:%M'])

#	class Meta:
#		model = AnimeSeries


class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField()


class RegisterForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField()
	email = forms.EmailField()


#class AddAnimeSeasonsForm(ModelForm):
#	class Meta:
#		model = AnimeSeason


class AddMangaForm(ModelForm):
	class Meta:
		model = Production
