"""
Menus views.
"""

# Django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def not_found_view(request):
    """
    Page not found view.
    """
    return render(request, 'backend_test/errors/404.html')


def server_error_view(request):
    """
    Internal server error view.
    """
    return render(request, 'backend_test/errors/500.html')
