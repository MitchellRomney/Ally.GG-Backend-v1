# Generated by Django 2.1.7 on 2019-03-29 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_remove_match_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='timestamp',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
