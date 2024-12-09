# Generated by Django 2.2.28 on 2024-11-18 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_year',
            field=models.IntegerField(blank=True),
        ),
    ]