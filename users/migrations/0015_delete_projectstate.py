# Generated by Django 3.0.6 on 2020-07-08 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20200708_2346'),
        ('users', '0014_auto_20200708_2344'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectState',
        ),
    ]