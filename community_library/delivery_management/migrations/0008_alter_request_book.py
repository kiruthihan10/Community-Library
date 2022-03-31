# Generated by Django 3.2.8 on 2022-03-30 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_management', '0003_auto_20220330_1827'),
        ('delivery_management', '0007_auto_20220330_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_management.book'),
        ),
    ]