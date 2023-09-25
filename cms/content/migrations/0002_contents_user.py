# Generated by Django 4.2.4 on 2023-09-25 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_usertoken'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contents',
            name='user',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='user_auth.rootuser'),
            preserve_default=False,
        ),
    ]
