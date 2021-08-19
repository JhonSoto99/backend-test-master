"""
backend_test url conf
"""

# Django
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

# Views
from accounts import views as accounts_views
from backend_test import views as backend_test_views


urlpatterns = [
    # modules paths
    path('menus/', include(('menus.urls', 'menus'), namespace='menus')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),

    # generals paths
    path(
        route='',
        view=accounts_views.login_view,
        name='login'
    ),
    path(
        route='404',
        view=backend_test_views.not_found_view,
        name='not_found'
    ),
    path(
        route='500',
        view=backend_test_views.server_error_view,
        name='server_error'
    )

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
