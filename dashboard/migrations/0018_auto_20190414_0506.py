# Generated by Django 2.1.7 on 2019-04-14 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_auto_20190414_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rune',
            name='shortDesc',
            field=models.TextField(),
        ),
    ]
