# Generated by Django 2.1.7 on 2019-04-14 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_rune_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rune',
            name='version',
            field=models.CharField(null=True, max_length=255),
        ),
    ]
