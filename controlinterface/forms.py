from django.contrib.auth.forms import AuthenticationForm
from django import forms


class AuthLoginForm(AuthenticationForm):
    pass

LANG_CHOICES = [
    ('en', 'English'),
    ('sw', 'Swahili'),
    ('lu', 'Luganda'),
    ('ru', 'Runyakitara'),
    ('lo', 'Luo'),
]

MS_CHOICES = [
    ('acc', 'Accelerated'),
    ('bab1', 'Baby')
]


class MessageFindForm(forms.Form):
    messageaction = forms.CharField(widget=forms.HiddenInput(), initial="find")
    message_set = forms.ChoiceField(choices=MS_CHOICES)
    sequence_number = forms.IntegerField(min_value=1)
    lang = forms.ChoiceField(choices=LANG_CHOICES)


class SubscriptionFindForm(forms.Form):
    subaction = forms.CharField(widget=forms.HiddenInput(), initial="find")
    msisdn = forms.CharField(label="Cellphone Number")
