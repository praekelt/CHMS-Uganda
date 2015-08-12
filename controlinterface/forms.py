from django.contrib.auth.forms import AuthenticationForm
from django import forms


class AuthLoginForm(AuthenticationForm):
    pass

LANG_CHOICES = [
    ('en', 'English'),
    ('af', 'Afrikaans'),
    ('zu', 'Zulu'),
    ('xh', 'Xhosa'),
    ('ve', 'Venda'),
    ('tn', 'Tswnana'),
    ('ts', 'Tsonga'),
    ('ss', 'Swazi'),
    ('st', 'Sotho'),
    ('nso', 'Northern Sotho'),
    ('nr', 'Ndebele')
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
