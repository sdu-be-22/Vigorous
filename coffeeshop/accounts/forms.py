import email
from unicodedata import name
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from shop.models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','email', 'first_name', 'last_name']
    
    # def save(self, commit= True):
    #     user = super(CustomUserCreationForm, self).save(commit=False)
    #     if commit:
    #         user.save()
    #         Customer.objects.create(user=user,name=user.username,email=user.email)
    #     return user