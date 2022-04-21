from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from dataclasses import fields
from django import forms
from . models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( 'comment_body',)
        widgets = {
            'comment_body':forms.Textarea(attrs={'class':'forms-control'}),
        }
class EmailForm(forms.Form):
    recipient = forms.EmailField()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
