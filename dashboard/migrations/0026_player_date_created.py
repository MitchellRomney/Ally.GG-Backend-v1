# Generated by Django 2.1.7 on 2019-04-29 09:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0025_match_bots'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
