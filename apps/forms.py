from django import forms
from django.forms import ModelForm
from django.forms.models import BaseModelFormSet

from apps.models import *


class AddForm(ModelForm):
	class Meta:
		model = Production
		fields = '__all__'


class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField()


class RegisterForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField()
	email = forms.EmailField()


class AddSerieForm(ModelForm):
	''' Добавляем новую серию '''
	start_date = forms.DateField(required=False,
		input_formats=['%Y-%m-%d', '%d/%m/%Y'])
	length = forms.IntegerField(required=False)
	name = forms.CharField(required=False)
	num_season = forms.CharField(required=False)

	class Meta:
		model = Serie
		fields = '__all__'


class AddToListForm(ModelForm):
	series = forms.MultipleChoiceField(required=False)
	score = forms.IntegerField(required=False)
	class Meta:
		model = ListedProduct


class UpdateStatusForm(ModelForm):
	class Meta:
		model = Status
