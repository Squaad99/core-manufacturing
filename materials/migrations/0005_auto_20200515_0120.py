# Generated by Django 3.0.5 on 2020-05-14 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_auto_20200506_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='unit_label',
            field=models.CharField(default='', max_length=100),
        ),
    ]
