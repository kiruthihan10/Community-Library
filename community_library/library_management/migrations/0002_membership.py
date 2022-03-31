# Generated by Django 3.2.8 on 2022-03-30 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
        ('library_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('banned', models.BooleanField(default=0)),
                ('lib', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_management.library')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.reader')),
            ],
        ),
    ]
