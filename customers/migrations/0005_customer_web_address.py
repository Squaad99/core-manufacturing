# Generated by Django 3.0.6 on 2020-06-01 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_auto_20200601_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='web_address',
            field=models.URLField(blank=True, max_length=100, verbose_name='Websida'),
        ),
    ]
