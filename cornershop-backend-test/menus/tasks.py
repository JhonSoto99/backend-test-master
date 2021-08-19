"""
Tasks Menus.
"""

import requests

# Django
from django.conf import settings
from django.utils import timezone
from django.contrib.sites.models import Site

from celery import Celery

app = Celery("backend_test")
app.config_from_object(settings)
app.autodiscover_tasks()


@app.task(bind=True)
def send_menu_to_slack(task=None):
    """
    Check if there is a menu of the day available for today
    and it is sent to the established channel.
    """

    # Models
    from menus.models import Menu
    site = Site.objects.get_current()

    today = timezone.localtime().strftime('%Y-%m-%d')
    menu_available = Menu.objects.filter(availability_date=today).exists()

    if menu_available:
        menu = Menu.objects.get(availability_date=today)
        if menu.is_enabled:
            menu_dishes = menu.dishmenu_set.all()
            message = "Hello! \n I share with you today's menu \n\n"

            for menu_dish in menu_dishes:
                message += '* {}\n'.format(
                    menu_dish.dish.description,
                )


            url = f"{site.domain}/menus/{menu.uuid}/"

            message += f"\n\nTo place your order visit the following link: {url}"

            response = requests.post(
                settings.SLACK_CHANNEL,
                json={
                    "text": message
                }
            )

            print(response.status_code, response.text)

