"""
Menu forms.
"""

# Django
from django import forms
from django.utils import timezone

# Models
from .models import *


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = [
            'availability_date',
            'name'
        ]

    def clean_date(self):
        """
        method to validate that there is no menu for today.
        """
        availability_date = self.cleaned_data['availability_date']
        menu = Menu.objects.filter(availability_date=availability_date).exists()
        today = timezone.localtime().strftime('%Y-%m-%d')
        if menu:
            raise forms.ValidationError('There is already a menu for today.')
        if availability_date.strftime('%Y-%m-%d') < today:
            raise forms.ValidationError('You cannot select a date less than today date.')

        return availability_date


class DishForm(forms.ModelForm):

    class Meta:
        model = Dish
        fields = [
            'description'
        ]


class DishMenuForm(forms.ModelForm):

    class Meta:
        model = DishMenu
        fields = [
            'dish'
        ]
