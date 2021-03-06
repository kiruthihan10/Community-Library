# Generated by Django 3.2.8 on 2022-03-30 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_management', '0005_alter_complaints_on'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='borrowel',
            name='delivery_ma_deadlin_5b8d2a_idx',
        ),
        migrations.RemoveIndex(
            model_name='borrowel',
            name='delivery_ma_book_id_c3712a_idx',
        ),
        migrations.RemoveIndex(
            model_name='borrowel',
            name='delivery_ma_reader__5c83e7_idx',
        ),
        migrations.RemoveIndex(
            model_name='request',
            name='delivery_ma_Date_ap_b26947_idx',
        ),
        migrations.AddIndex(
            model_name='borrowel',
            index=models.Index(fields=['-deadline', 'start_date'], name='Date_difference_index'),
        ),
        migrations.AddIndex(
            model_name='borrowel',
            index=models.Index(fields=['book'], name='borrowel_book_index'),
        ),
        migrations.AddIndex(
            model_name='borrowel',
            index=models.Index(fields=['reader'], name='borrowel_reader_index'),
        ),
        migrations.AddIndex(
            model_name='request',
            index=models.Index(fields=['Date_applied'], name='applied_date_index'),
        ),
    ]
