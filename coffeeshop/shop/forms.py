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
