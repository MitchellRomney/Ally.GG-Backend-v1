# Generated by Django 2.1.7 on 2019-04-16 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20190416_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='flexSR_tier',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='flexTT_tier',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='soloQ_tier',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
