# Generated by Django 2.2.3 on 2019-09-14 01:21

from django.db import migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20190806_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=s3direct.fields.S3DirectField(blank=True, null=True),
        ),
    ]
