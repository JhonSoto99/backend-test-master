"""
Accounts test model.
"""

from django.test import TestCase

# Model
from .models import User


class CreateUserTestCase(TestCase):

    def setUp(self):
        self.jhon = {
            'email': 'jhon@gmail.com',
            'password': 'AS355GG675',
            'first_name': 'Jhon',
            'last_name': 'Soto'
        }

    def test_create_user(self):
        user_jhon = User.objects.create(**self.jhon)
        self.assertIsNotNone(user_jhon.id)

