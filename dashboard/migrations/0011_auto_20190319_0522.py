# Generated by Django 2.1.7 on 2019-03-19 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20190319_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match_team',
            name='match',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Match'),
        ),
    ]
