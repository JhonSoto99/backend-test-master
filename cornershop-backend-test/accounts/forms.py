"""
Signup forms.
"""

# Django
from django import forms

# Models
from .models import User


class SignupForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        min_length=2,
        max_length=50,
        required=True
    )
    last_name = forms.CharField(
        label='Last Name',
        min_length=2,
        max_length=50,
        required=True
    )
    email = forms.CharField(
        label='Email',
        max_length=100,
        min_length=6,
        required=True
    )
    password = forms.CharField(
        label='Password',
        min_length=5,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'off'}
        ),
        required=True
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        email_taken = User.objects.filter(email=email).exists()
        if email_taken:
            raise forms.ValidationError('Email is already in use.')
        return email
