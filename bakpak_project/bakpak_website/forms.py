
from django import forms


class emailsForNewsletter(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required': True,
                                                            "size": 40}))


class contactForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required': True,
                                                            "size": 40,
                                                            "placeholder": "Votre mail:"}))
    sujet = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                                                          'size': 40,
                                                          'maxlength': '150',
                                                          "placeholder": "Sujet:"}))

    message = forms.CharField(widget=forms.Textarea(attrs={'required': True,
                                                           'cols': '40',
                                                           'rows': '7',
                                                           'maxlength': '850',
                                                           "placeholder": "Message limité à 350 caractères"
                                                           }))

