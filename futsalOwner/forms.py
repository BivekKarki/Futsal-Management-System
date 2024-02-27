from django import forms
from django_recaptcha.fields import ReCaptchaField


class OwnerLoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    captcha = ReCaptchaField()