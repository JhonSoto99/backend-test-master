# Django
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Models
from .models import *

# Forms
from .forms import *

# Celery
from .tasks import send_menu_to_slack


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    queryset = model.objects.all()
    template_name = 'menus/list.html'

    def get_queryset(self):
        queryset = super(MenuListView, self).get_queryset()
        return queryset


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    queryset = model.objects.all()
    template_name = 'menus/dishes/list.html'

    def get_queryset(self):
        queryset = super(DishListView, self).get_queryset()
        return queryset


class MenuCreateView(LoginRequiredMixin, CreateView):
    model = Menu
    form_class = MenuForm
    template_name = 'menus/create.html'


    def form_valid(self, form, **kwargs):
        """
        Validate and save
        """
        if form.is_valid():
            menu = Menu(**form.cleaned_data)
            menu.save()


            return HttpResponseRedirect(reverse(
                'menus:add_dish_menu', args = {menu.uuid}
            ))


class DishMenuCreateView(LoginRequiredMixin, CreateView):
    model = DishMenu
    form_class = DishMenuForm
    template_name = 'menus/add_dish.html'


    def form_valid(self, form, **kwargs):
        """
        Validate and save
        """
        if form.is_valid():
            menu_id = self.kwargs['menu_id']
            menu = Menu.objects.get(pk=menu_id)
            dish = form.cleaned_data['dish']

            menu_dishes_taken = DishMenu.objects.filter(
                menu_id=menu.uuid,
                dish_id=dish.uuid
            ).exists()

            if not menu_dishes_taken:
                menu_dishes = DishMenu(menu=menu, **form.cleaned_data)
                menu_dishes.save()

            return HttpResponseRedirect(reverse('menus:list'))


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'menus/dishes/create.html'


    def form_valid(self, form, **kwargs):
        """
        Validate and save
        """
        if form.is_valid():
            dish = Dish(**form.cleaned_data)
            dish.save()

            return HttpResponseRedirect(reverse('menus:list_dish'))


def check_exists_menu_of_day(request):
    """
    Method for verifying if there is
    a menu available to be offered to users
    """
    try:
        menu = Menu.objects.latest('availability_date')
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('menus:not_available'))

    if not menu.is_menu_today:
        return HttpResponseRedirect(reverse('menus:not_available'))

    return HttpResponseRedirect(reverse('menus:menu_of_day', args=(
        menu.uuid,
    )))


def not_available_view(request):
    """
    Menu not available.
    """
    return render(request, 'menus/not_available.html')


class MenuOfDayTemplateView(LoginRequiredMixin, TemplateView):
    model = Menu
    template_name = 'menus/menu_of_day.html'


    def dispatch(self, request, *args, **kwargs):
        try:
            menu = self.model.objects.latest('availability_date')
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('not_found'))

        if not menu.is_menu_today:
            return HttpResponseRedirect(reverse('menus:not_available'))


        return super(MenuOfDayTemplateView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(MenuOfDayTemplateView, self).get_context_data(object_list=None, **kwargs)

        context['menu']  = self.model.objects.latest('availability_date')
        return context


@login_required
def menu_send_notification(request, menu_id):
    """
    Send notification menu
    View that serves to notify the menu of the day.
    """
    try:
        menu = Menu.objects.get(pk=menu_id)
        if menu.is_menu_today:
            send_menu_to_slack.delay()
            msg = f'A notification will be sent to the slack channel for the menu {menu.name}.'
            messages.info(
                request,
                msg
            )
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))

    return HttpResponseRedirect(reverse('menus:list'))


@login_required
def remove_dish_menu(request, menu_dish_id):
    """
    It allows us to remove a dish from a menu
    """
    menu_dish = DishMenu.objects.get(pk=menu_dish_id)

    menu_dish.delete()

    return HttpResponseRedirect(reverse('menus:list'))
