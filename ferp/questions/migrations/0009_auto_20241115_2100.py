# Generated by Django 2.2.28 on 2024-11-15 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20241115_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='qn_area',
            field=models.TextField(),
        ),
    ]