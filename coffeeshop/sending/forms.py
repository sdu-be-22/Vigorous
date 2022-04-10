from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Text something...",
                "class": "textarea is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = Message
        exclude = ("user", )
