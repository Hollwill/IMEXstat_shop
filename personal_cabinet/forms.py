import os
from django import forms
from .models import Client



class ProfileForm(forms.ModelForm):

	class Meta:
		model = Client
		fields = ['lastname', 'firstname', 'middle_name', 'email', 'phone']
		exclude = ['user',]



class RequizitesForm(forms.ModelForm):
	class Meta:

		model = Client
		fields = ['firm_name', 'legal_adress', 'INN', 'KPP', 'requisites_file' ]



