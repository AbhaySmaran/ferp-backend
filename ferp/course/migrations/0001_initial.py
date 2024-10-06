# Generated by Django 2.2.28 on 2024-10-06 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=100)),
                ('no_of_sem', models.IntegerField()),
                ('course_duration', models.IntegerField()),
            ],
        ),
    ]
