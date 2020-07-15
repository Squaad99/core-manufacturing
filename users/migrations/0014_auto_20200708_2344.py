# Generated by Django 3.0.6 on 2020-07-08 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_auto_20200708_2344'),
        ('materials', '0009_auto_20200708_2344'),
        ('time_accounting', '0007_auto_20200708_2344'),
        ('projects', '0013_auto_20200708_2344'),
        ('products', '0007_auto_20200708_2344'),
        ('company', '0003_auto_20200708_2344'),
        ('users', '0013_auto_20200629_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.Company'),
        ),
        migrations.AlterField(
            model_name='projectstate',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.Company'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]