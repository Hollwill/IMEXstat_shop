from django import forms
from .models import Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['lastname', 'firstname', 'middle_name', 'email', 'phone']
		exclude = ['user']


class RequizitesForm(forms.ModelForm):
	class Meta:

		model = Client
		fields = ['firm_name', 'legal_adress', 'INN', 'KPP', 'requisites_file']


class UserCreationWithEmailForm(UserCreationForm):
	username = forms.CharField(label="Your Username")
	email = forms.EmailField(label="Email Address")

	class Meta:
		model = User
		fields = UserCreationForm.Meta.fields

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
			return user
