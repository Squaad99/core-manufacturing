# Generated by Django 3.0.6 on 2020-06-29 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='dummy',
        ),
    ]
