# Generated by Django 2.2.28 on 2024-10-19 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0004_subjectassignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectassignment',
            name='sem',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
