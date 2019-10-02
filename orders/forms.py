from django import forms
from personal_cabinet.models import Client
from .models import OrderItem, Order, Cart
from functools import partial, wraps

class IndividualForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['lastname', 'firstname', 'email', 'phone']
		exclude = ['user',]



class EntityForm(forms.ModelForm):
	class Meta:

		model = Client
		fields = ['firstname', 'lastname', 'firm_name', 'email', 'phone', 'INN', 'KPP']



class CartItemsFormSet(forms.BaseFormSet):
	def add_fields(self, form, index):
		super().add_fields(form, index)
		form.fields['update_frequency'] = forms.ChoiceField()