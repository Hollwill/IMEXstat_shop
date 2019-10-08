from django import forms
from .models import Feedback


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}),
			'contact_details': forms.TextInput(attrs={'placeholder': 'Введите номер телефона или E-mail'}),
		}