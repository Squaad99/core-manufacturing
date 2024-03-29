# Generated by Django 3.0.6 on 2020-08-11 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_auto_20200708_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactperson',
            name='email',
            field=models.EmailField(max_length=50, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='contactperson',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Namn'),
        ),
        migrations.AlterField(
            model_name='contactperson',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Telefon'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='comment',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='Anteckning'),
        ),
    ]
