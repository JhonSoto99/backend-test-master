"""
Orders urls
"""

# Django
from django.conf.urls import url
from django.urls import path

from .views import *

app_name = "web_orders"

urlpatterns = [
    path(route='create/<uuid:menu_dish_id>/', view=OrderCreateView.as_view(), name='create'),
    path(route='list/', view=OrderListView.as_view(), name='list'),
]

