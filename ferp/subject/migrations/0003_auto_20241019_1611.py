# Generated by Django 2.2.28 on 2024-10-19 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0002_auto_20241019_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='practical_full_mark',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='theory_full_mark',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
