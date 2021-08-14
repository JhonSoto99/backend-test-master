"""
Orders model.
"""

# Django
from django.db import models
from django.utils import timezone

import uuid


class Order(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )
    menu_dish = models.ForeignKey(
        'menus.Dish',
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text='Date time on which the order was created.'
    )
    observations = models.TextField(
        'Observations',
        null=False,
        help_text='Customizations of my dish (e.g. no tomatoes in the salad).'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return '{}: {}'.format(
            self.user.email,
            self.menu_dish,
        )
