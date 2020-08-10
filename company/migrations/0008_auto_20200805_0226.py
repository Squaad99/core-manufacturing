# Generated by Django 3.0.6 on 2020-08-05 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_worktype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worktype',
            name='cost',
            field=models.FloatField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='worktype',
            name='work_type_id',
            field=models.IntegerField(blank=True),
        ),
    ]
