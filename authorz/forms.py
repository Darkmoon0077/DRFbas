from .models import Feedback
from django import forms

class FeedbackCreateForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('subject', 'email', 'content')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

class ContactForm(forms.Form):
    from_email = forms.EmailField(label='Email', required=True)
    subject = forms.CharField(label='Тема', required=True)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea, required=True)

class LogForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

