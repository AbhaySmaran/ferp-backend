# Generated by Django 2.2.28 on 2024-10-06 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20241006_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
