# Generated by Django 3.0.6 on 2020-06-01 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20200601_2336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='web_address',
        ),
        migrations.AddField(
            model_name='customer',
            name='comment',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='Kommentar'),
        ),
    ]
