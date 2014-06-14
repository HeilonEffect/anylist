from django import forms
from django.forms import ModelForm
from django.forms.models import BaseModelFormSet

from apps.models import *


class AddForm(ModelForm):
	class Meta:
		model = Production


class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField()


class RegisterForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField()
	email = forms.EmailField()


class AddSerieForm(ModelForm):
	start_date = forms.DateTimeField(required=False,
		input_formats=['%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M'])
	length = forms.IntegerField(required=False)
	name = forms.CharField(required=False)
	class Meta:
		model = Serie


class AddMangaVolumeForm(ModelForm):
	name = forms.CharField(required=False)
	class Meta:
		model = SeriesGroup


class AddToListForm(ModelForm):
	series = forms.MultipleChoiceField(required=False)
	score = forms.IntegerField(required=False)
	class Meta:
		model = ListedProduct


class UpdateStatusForm(ModelForm):
	class Meta:
		model = Status


# Wizard Form
class CreateForm1(forms.Form):
	name = forms.CharField(max_length=255)
	description = forms.CharField()
	avatar = forms.FileField()
	old_limit = forms.ChoiceField()


class CreateForm2(forms.Form):
	genres = forms.MultipleChoiceField()

