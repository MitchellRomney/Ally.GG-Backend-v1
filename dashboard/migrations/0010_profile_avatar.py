# Generated by Django 2.1.7 on 2019-04-02 04:59

from django.db import migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_match_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=s3direct.fields.S3DirectField(blank=True, null=True),
        ),
    ]
