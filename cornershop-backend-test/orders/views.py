"""
Orders Views.
"""

# Django
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.views.generic.list import ListView

# Models
from .models import *
from menus.models import DishMenu

# Forms
from .forms import *


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderMenuForm
    template_name = 'orders/create.html'


    def form_valid(self, form, **kwargs):
        """
        Validate and save
        """
        if form.is_valid():
            menu_dish = DishMenu.objects.get(pk=self.kwargs['menu_dish_id'])
            order = Order(
                user=self.request.user,
                menu_dish=menu_dish,
                date=timezone.now(),
                observations=form.cleaned_data['observations']
            )
            order.save()


            return HttpResponseRedirect(reverse('orders:list'))


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    queryset = model.objects.all()
    template_name = 'orders/list.html'

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user_id=self.request.user.id)

        return queryset