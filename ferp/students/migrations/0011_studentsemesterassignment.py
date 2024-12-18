# Generated by Django 2.2.28 on 2024-10-30 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_student_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentSemesterAssignment',
            fields=[
                ('student_sem_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('semester', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
            ],
        ),
    ]
