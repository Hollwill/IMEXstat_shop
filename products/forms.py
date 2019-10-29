from django import forms
from orders.models import OrderItem
from .models import IndividualResearchFeedback
from validate_email import validate_email
from django.utils.encoding import smart_text
import re

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
