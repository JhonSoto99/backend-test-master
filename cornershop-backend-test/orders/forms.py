"""
Forms Orders
"""

# Django
from django import forms

# Models
from .models import *


class OrderMenuForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'observations'
        ]