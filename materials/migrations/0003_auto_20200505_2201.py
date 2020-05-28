

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20200504_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='base_cost',
            field=models.FloatField(max_length=20),
        ),
        migrations.AlterField(
            model_name='material',
            name='comment',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='material',
            name='scalable_cost',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='material',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='material',
            name='unit_cost',
            field=models.FloatField(max_length=20),
        ),
        migrations.AlterField(
            model_name='material',
            name='unit_label',
            field=models.CharField(max_length=100),
        ),
    ]
