# Generated by Django 2.2.28 on 2024-11-07 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20241107_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions_uploaded', to=settings.AUTH_USER_MODEL),
        ),
    ]
