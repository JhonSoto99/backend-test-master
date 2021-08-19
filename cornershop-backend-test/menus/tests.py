"""
Menus tests model.
"""

# Django
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone

# Model
from .models import Menu, Dish, DishMenu

# Views
from .views import MenuListView, DishListView


class CreateMenuTestCase(TestCase):

    def setUp(self):
        self.my_menu = {
            'availability_date': timezone.localtime(),
            'name': 'Monday Menu'
        }

    def test_create_menu(self):
        """
        Verify that the menu was created correctly.
        """
        menu = Menu.objects.create(**self.my_menu)
        self.assertIsNotNone(menu.uuid)

    def test_is_today_menu(self):
        """
        Verify that the menu is availability before 11am
        """
        menu = Menu.objects.create(**self.my_menu)
        if menu.is_menu_today():
            self.assertTrue(menu.is_menu_today())
        else:
            self.assertFalse(menu.is_menu_today())


class CreateDishTestCase(TestCase):

    def setUp(self):
        self.my_dish = {
            'description': 'dish and salad',
        }

    def test_create_dish(self):
        """
        Verify that the dish was created correctly.
        """
        menu = Dish.objects.create(**self.my_dish)
        self.assertIsNotNone(menu.uuid)


class CreateMenuDishTestCase(TestCase):

    def setUp(self):
        self.my_dish = {
            'description': 'Fish, salad',
        }
        self.my_menu = {
            'availability_date': '2021-09-18',
            'name': 'Today Menu'
        }

    def test_create_menu_dish(self):
        """
        Verify that the menu_dish was created correctly.
        """

        dish = Dish.objects.create(**self.my_dish)
        menu = Menu.objects.create(**self.my_menu)
        menu_dish = DishMenu.objects.create(
            menu=menu,
            dish=dish
        )
        self.assertIsNotNone(menu_dish.uuid)


class MenuListViewTestCase(TestCase):
    """
    Test View MenuListView
    """
    longMessage = True
    def test_get(self):
        req = RequestFactory().get('/')
        req.user = User()
        resp = MenuListView.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)


class DishListViewTestCase(TestCase):
    """
    Test View DishListView
    """
    longMessage = True
    def test_get(self):
        req = RequestFactory().get('/')
        req.user = User()
        resp = DishListView.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)




