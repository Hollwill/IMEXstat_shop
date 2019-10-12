from django import forms
from .models import Feedback
#from django.core.validators import validate_email
from validate_email import validate_email
from django.utils.encoding import smart_text
import re

class ContactField(forms.Field):
    def validate(self, value):
        super(ContactField, self).validate(value)
        # Проверяем на соответствие поля "email"у

        if validate_email(value):
            pass
        # Проверяем на соответствие поля телефонному номеру
        elif re.compile("^([0-9\(\)\/\+ \-]*)$").search(smart_text(value)):
            pass
        # Если не соответствует ничему, то вызываем ошибку
        else:
            raise forms.ValidationError(u'Введите действительный номер телефона или email.', code='invalid')
 
class ProfileForm(forms.ModelForm):
	contact_details = ContactField(widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона или E-mail'}))
	class Meta:
		model = Feedback
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}),
		}