# Generated by Django 2.2.28 on 2024-11-16 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_auto_20241115_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='option_1',
            new_name='option_1_value',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='option_2',
            new_name='option_2_value',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='option_3',
            new_name='option_3_value',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='option_4',
            new_name='option_4_value',
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_ans',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]