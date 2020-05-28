# Generated by Django 3.0.5 on 2020-05-04 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='material',
            name='comment',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='Kommentar'),
        ),
        migrations.AddField(
            model_name='material',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='material',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
