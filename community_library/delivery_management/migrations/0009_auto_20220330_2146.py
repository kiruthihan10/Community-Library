# Generated by Django 3.2.8 on 2022-03-30 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_management', '0003_auto_20220330_1827'),
        ('user_management', '0002_auto_20220330_1834'),
        ('delivery_management', '0008_alter_request_book'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='request',
            unique_together={('user', 'book')},
        ),
        migrations.AddIndex(
            model_name='request',
            index=models.Index(fields=['book'], name='book_request_index'),
        ),
    ]