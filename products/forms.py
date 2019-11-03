from django import forms
from orders.models import CartItem
from .models import IndividualResearchFeedback
from validate_email import validate_email
from django.utils.encoding import smart_text
import re


class CartItemCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        model = CartItem
        fields = '__all__'


class ContactField(forms.Field):
    def validate(self, value):
        super(ContactField, self).validate(value)
        if validate_email(value):
            pass
        elif re.compile("^([0-9\(\)\/\+ \-]*)$").search(smart_text(value)):
            pass
        else:
            raise forms.ValidationError(u'Введите действительный номер телефона или email.', code='invalid')


class IndividualResearchFeedbackForm(forms.ModelForm):
    contact_details = ContactField(widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона или E-mail'}))

    class Meta:
        model = IndividualResearchFeedback
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}),
        }
