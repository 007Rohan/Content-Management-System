# Generated by Django 4.2.4 on 2023-09-25 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_usertoken'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='usertoken',
            table='root_users_token',
        ),
    ]
