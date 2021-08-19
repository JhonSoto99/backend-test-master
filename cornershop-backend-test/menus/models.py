"""
Menus models.
"""

import uuid

# Django
from django.db import models
from django.utils import timezone

# Settings
from backend_test.settings import RESERVE_LIMIT_HOUR


class Menu(models.Model):
    """
    Menus model.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    availability_date = models.DateTimeField(
        'availability date',
        default=timezone.now,
        help_text='Date the menu will be available.'
    )
    name = models.TextField(
        max_length=80,
        default="Menu for today",
        help_text='Descriptive name.'
    )
    is_enabled = models.BooleanField(
        'Is enabled',
        default=True,
        help_text=(
            'menu status, to check availability'
        )
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-availability_date']

    def __str__(self):
        return self.name

    def is_menu_today(self):
        """
        Check if the menu is of today.
        And reserve limit is current
        """
        today = timezone.localtime().strftime('%Y-%m-%d')
        current_hour = timezone.localtime().strftime('%H')
        return self.availability_date.strftime('%Y-%m-%d') == today and current_hour < RESERVE_LIMIT_HOUR


class Dish(models.Model):
    """
    Dishes model.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    description = models.TextField(
        null=False,
        help_text='Description of the elements of the dish.'
    )
    is_enabled = models.BooleanField(
        'Is enabled',
        default=True,
        help_text=(
            'To distinguish the available dishes.'
        )
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.description


class DishMenu(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('menu', 'dish'),)

    def __str__(self):
        return '{} - {}: ${}'.format(
            self.menu.name,
            self.dish.description,
            self.dish.price
        )
