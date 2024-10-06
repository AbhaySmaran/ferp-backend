# Generated by Django 2.2.28 on 2024-10-06 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20241002_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='authority',
            new_name='HOD',
        ),
        migrations.RemoveField(
            model_name='department',
            name='dept_abbr',
        ),
        migrations.AddField(
            model_name='department',
            name='dept_contact',
            field=models.CharField(default='78839337', max_length=15),
        ),
    ]