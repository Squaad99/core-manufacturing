# Generated by Django 3.0.5 on 2020-05-21 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200516_0111'),
        ('projects', '0003_auto_20200522_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='comment',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='Kommentar'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Titel'),
        ),
        migrations.CreateModel(
            name='ProductForProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0, max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]
