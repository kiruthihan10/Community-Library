# Generated by Django 3.2.8 on 2022-03-31 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_auto_20220330_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryman',
            name='cash_balance',
        ),
    ]