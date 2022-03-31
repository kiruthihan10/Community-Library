# Generated by Django 3.2.8 on 2022-03-30 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
        ('library_management', '0002_membership'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='library',
            unique_together={('name', 'address')},
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('lib', 'reader')},
        ),
        migrations.AddIndex(
            model_name='library',
            index=models.Index(fields=['name'], name='library_name_index'),
        ),
        migrations.AddIndex(
            model_name='membership',
            index=models.Index(fields=['reader'], name='member_index'),
        ),
    ]