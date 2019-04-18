# Generated by Django 2.1.7 on 2019-04-18 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_auto_20190417_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='gameId',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='profileIconId',
            field=models.BigIntegerField(blank=True, default=0),
        ),
    ]
