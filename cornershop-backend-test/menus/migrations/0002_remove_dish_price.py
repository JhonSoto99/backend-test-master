# Generated by Django 3.0.8 on 2021-08-13 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='price',
        ),
    ]
