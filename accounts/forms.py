from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    ACCOUNT_TYPE_CHOICES = [
        ('parent', 'Parent'),
        ('student', 'Student'),
    ]

    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES,
        label='I am registering as'
    )

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'account_type',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'password1',
            'password2',
        ]


class ParentRegistrationForm(RegistrationForm):
    pass


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)