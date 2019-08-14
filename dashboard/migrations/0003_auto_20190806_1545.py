# Generated by Django 2.2.3 on 2019-08-06 05:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_remove_player_currentplatformid'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
