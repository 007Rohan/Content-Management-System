# Generated by Django 4.2.4 on 2023-09-25 18:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_role_rootuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='userToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.CharField(blank=True, max_length=255, null=True)),
                ('authToken', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
    ]