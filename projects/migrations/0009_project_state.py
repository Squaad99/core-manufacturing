# Generated by Django 3.0.6 on 2020-06-17 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_project_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='state',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
