from django import forms
from personal_cabinet.models import Client
from .models import OrderItem, Order, Cart

class IndividualForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['lastname', 'firstname', 'email', 'phone']
		exclude = ['user',]



class EntityForm(forms.ModelForm):
	class Meta:

		model = Client
		fields = ['firstname', 'lastname', 'firm_name', 'email', 'phone', 'INN', 'KPP']

class CartResearchForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['research'].widget.attrs.update({'style': 'display:none;'})
	class Meta(object):
		model = OrderItem
		fields = '__all__'
		exclude = ['price', 'order']
		widgets = {
			'update_frequency': forms.RadioSelect(attrs={'class': 'checkbox__input'}),
			'duration': forms.RadioSelect()
		}



Formset = forms.formset_factory(CartResearchForm)
'''Formset = formset_factory(CartResearchForm, extra=len(some_objects)
some_formset = FormSet(initial=[{'id': 'x.id'} for x in some_objects])'''