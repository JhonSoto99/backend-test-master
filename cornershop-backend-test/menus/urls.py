"""
Menus urls
"""

# Django
from django.conf.urls import url
from django.urls import path

from .views import *

app_name = "web_menus"

urlpatterns = [
    # Menus
    url(r'^list/', MenuListView.as_view(), name="list"),
    url(r'^create/', MenuCreateView.as_view(), name="create"),
    url(r'^menu_of_day/', MenuOfDayTemplateView.as_view(), name="menu_of_day"),

    # Notifications
    path(route='send_notification/<uuid:menu_id>/', view=menu_send_notification, name='send_notification'),

    # Dishes
    url(r'^create_dish/', DishCreateView.as_view(), name="create_dish"),
    url(r'^list_dish/', DishListView.as_view(), name="list_dish"),
    path(route='add_dish_menu/<uuid:menu_id>/', view=DishMenuCreateView.as_view(), name='add_dish_menu'),
    path(route='dishes/<uuid:menu_dish_id>/remove/', view=remove_dish_menu, name='remove_dish_menu'),
]

