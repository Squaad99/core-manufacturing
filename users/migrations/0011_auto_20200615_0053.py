# Generated by Django 3.0.6 on 2020-06-14 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_profile_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='cost_per_work_hour',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='currency',
            field=models.CharField(default='SEK', max_length=10),
        ),
        migrations.AlterField(
            model_name='company',
            name='title',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='ProjectState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Company')),
            ],
        ),
    ]
