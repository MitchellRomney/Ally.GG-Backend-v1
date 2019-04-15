# Generated by Django 2.1.7 on 2019-04-14 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_auto_20190414_0920'),
    ]

    operations = [
        migrations.CreateModel(
            name='SummonerSpell',
            fields=[
                ('version', models.CharField(max_length=255)),
                ('key', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('summonerSpellId', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('tooltip', models.CharField(max_length=255)),
                ('maxrank', models.IntegerField()),
                ('cooldown', models.IntegerField()),
                ('cooldownBurn', models.CharField(max_length=255)),
                ('cost', models.IntegerField()),
                ('costBurn', models.CharField(max_length=255)),
                ('costType', models.CharField(max_length=255)),
                ('summonerLevel', models.IntegerField()),
                ('maxammo', models.CharField(max_length=255)),
                ('range', models.IntegerField()),
                ('rangeBurn', models.CharField(max_length=255)),
                ('image_full', models.CharField(max_length=255)),
                ('image_sprite', models.CharField(max_length=255)),
                ('image_group', models.CharField(max_length=255)),
                ('image_x', models.IntegerField()),
                ('image_y', models.IntegerField()),
                ('image_w', models.IntegerField()),
                ('image_h', models.IntegerField()),
                ('resource', models.CharField(max_length=255)),
            ],
        ),
    ]
