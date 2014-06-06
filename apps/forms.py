from django import forms
from django.forms import ModelForm
from django.forms.models import BaseModelFormSet

from haystack.forms import SearchForm

from apps.models import *


class ProductionSearchForm(SearchForm):
	title = forms.CharField(max_length=255)

	def search(self):
		sqs = super(ProductionSearchForm, self).search()

		if not self.is_valid():
			return self.no_query_found()

		sqs = sqs.filter(title__contains=self.cleaned_data['title'])

		return sqs


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
	start_date = forms.DateTimeField(required=False, input_formats=['%Y/%m/%d %H:%M'])
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


# Wizard Form
class CreateForm1(forms.Form):
	name = forms.CharField(max_length=255)
	description = forms.CharField()
	avatar = forms.FileField()
	old_limit = forms.ChoiceField()


class CreateForm2(forms.Form):
	genres = forms.MultipleChoiceField()

