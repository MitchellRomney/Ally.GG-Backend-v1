# Generated by Django 2.1.7 on 2019-04-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_auto_20190416_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='accountId',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='puuid',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
