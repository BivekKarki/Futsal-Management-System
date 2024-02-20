from django import forms
from django_recaptcha.fields import ReCaptchaField


class LoginForm(forms.Form):
    phone = forms.CharField(label='Phone', max_length=100)  # Change email to phone
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    captcha = ReCaptchaField()
