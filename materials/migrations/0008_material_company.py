# Generated by Django 3.0.6 on 2020-06-07 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_profile_title'),
        ('materials', '0007_auto_20200603_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Company'),
            preserve_default=False,
        ),
    ]
