"""
Accounts urls
"""

# Django
from django.conf.urls import url

from .views import *

app_name = "web_accounts"

urlpatterns = [
    url(r'^login/', login_view, name="login"),
    url(r'^signup/', signup_view, name="signup"),
    url(r'^logout/', logout_view, name="logout"),
]

