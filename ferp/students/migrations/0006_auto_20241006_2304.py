# Generated by Django 2.2.28 on 2024-10-06 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20241006_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='hostel_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='room_no',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='hostel',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]