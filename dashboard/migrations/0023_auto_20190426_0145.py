# Generated by Django 2.1.7 on 2019-04-26 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_auto_20190418_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='colloq',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
