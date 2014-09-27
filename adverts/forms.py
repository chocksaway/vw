from django.contrib.auth.models import User
from django import forms

__author__ = 'milesd'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    keywords = forms.CharField()


class Meta:
    model = User
    fields = ('username', 'email', 'password', 'keywords')