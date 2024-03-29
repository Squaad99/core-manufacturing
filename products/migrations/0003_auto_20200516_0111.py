# Generated by Django 3.0.5 on 2020-05-15 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_auto_20200515_0120'),
        ('products', '0002_auto_20200515_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialForProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.IntegerField(default=0)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.Material')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='comment',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='Kommentar'),
        ),
        migrations.AlterField(
            model_name='product',
            name='extra_cost',
            field=models.FloatField(blank=True, default=0, max_length=20, verbose_name='Extra kostnad'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Titel'),
        ),
        migrations.DeleteModel(
            name='MaterialForProject',
        ),
        migrations.AddField(
            model_name='materialforproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
