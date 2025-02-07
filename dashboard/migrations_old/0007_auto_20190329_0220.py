# Generated by Django 2.1.7 on 2019-03-29 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20190329_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='mapId',
            field=models.IntegerField(blank=True, choices=[(1, "Summoner's Rift - Summer"), (2, "Summoner's Rift - Autumn"), (3, 'The Proving Grounds'), (4, 'Twisted Treeline - Original'), (8, 'The Crystal Scar'), (10, 'Twisted Treeline'), (11, "Summoner's Rift"), (12, 'Howling Abyss'), (14, "Butcher's Bridge"), (16, 'Cosmic Ruins'), (18, 'Valoran City Park'), (19, 'Substructure 43'), (20, 'Crash Site'), (21, 'Nexus Blitz')], null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='seasonId',
            field=models.IntegerField(blank=True, choices=[(0, 'PRESEASON 3'), (1, 'SEASON 3'), (2, 'PRESEASON 2014'), (3, 'SEASON 2014'), (4, 'PRESEASON 2015'), (5, 'SEASON 2015'), (6, 'PRESEASON 2016'), (7, 'SEASON 2016'), (8, 'PRESEASON 2017'), (9, 'SEASON 2017'), (10, 'PRESEASON 2018'), (11, 'SEASON 2018'), (12, 'PRESEASON 2019'), (13, 'SEASON 2019')], null=True),
        ),
    ]
