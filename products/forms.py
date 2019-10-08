from django import forms
from orders.models import OrderItem


class ResearchBuyForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ResearchBuyForm, self).__init__(*args, **kwargs)
		self.fields['research'].required = False
	class Meta(object):
		model = OrderItem
		fields = '__all__'
		exclude = ['price', 'order']
		widgets = {
			'update_frequency': forms.RadioSelect(attrs={'class': 'checkbox__input'}),
			'duration': forms.RadioSelect(attrs={'class': 'Duration_choice'})
		}
		error_messages = {
			'update_frequency': {
				'required': ('Выберите частоту исследования')
			},
			'duration': {
				'required': ('Выберите срок подписки')
			}
		}