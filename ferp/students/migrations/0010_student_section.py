# Generated by Django 2.2.28 on 2024-10-23 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_auto_20241019_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='section',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
