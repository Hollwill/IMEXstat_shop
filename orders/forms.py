from django import forms
from personal_cabinet.models import Client



class IndividualForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['lastname', 'firstname', 'email', 'phone']
		exclude = ['user',]



class EntityForm(forms.ModelForm):
	class Meta:

		model = Client
		fields = ['firstname', 'lastname', 'firm_name', 'email', 'phone', 'INN', 'KPP']



