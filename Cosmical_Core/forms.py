from django import forms
from .models import MessageModel



class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageModel
        fields = ['body', 'image']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'})
        }