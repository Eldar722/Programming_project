from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Message

class NewUserForm(UserCreationForm):
    CHOICES = [
        ('option1', 'Работодатель'),
        ('option2', 'Стажировщик'),
    ]
    custom_choice = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select,
        label="Выберите пункт"
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "custom_choice")

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['employee', 'content']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }