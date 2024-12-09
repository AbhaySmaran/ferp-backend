# Generated by Django 2.2.28 on 2024-11-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20241116_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='option_1_number',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='question',
            name='option_2_number',
            field=models.PositiveSmallIntegerField(default=2),
        ),
        migrations.AddField(
            model_name='question',
            name='option_3_number',
            field=models.PositiveSmallIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='question',
            name='option_4_number',
            field=models.PositiveSmallIntegerField(default=4),
        ),
    ]