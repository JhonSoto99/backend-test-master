"""
Orders tests model.
"""

# Django
from django.test import TestCase
from django.utils import timezone

# Models
from menus.models import Menu, DishMenu, Dish
from orders.models import Order
from accounts.models import User


class CreateOrderTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='jhon@gmail.com', password='123pdnffhb543')
        self.dish = Dish.objects.create(description="fish, salad")
        self.menu = Menu.objects.create(availability_date=timezone.localtime(), name='tofay Menu')
        self.menu_dish = DishMenu.objects.create(menu=self.menu, dish=self.dish)

    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            menu_dish=self.menu_dish,
            date=timezone.localtime(),
            observations="Observations for food"
        )
        self.assertIsNotNone(order.uuid)
