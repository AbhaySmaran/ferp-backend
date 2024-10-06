# Generated by Django 2.2.28 on 2024-10-06 18:25

from django.db import migrations, models
import django.db.models.deletion
import students.models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20241006_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='batch',
            field=models.CharField(max_length=20),
        ),
        migrations.CreateModel(
            name='student_documents',
            fields=[
                ('doc_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('document_name', models.CharField(max_length=100)),
                ('document_file', models.FileField(upload_to=students.models.document_upload_to)),
                ('uploaded_on', models.DateField(auto_now_add=True)),
                ('uploaded_by', models.CharField(blank=True, max_length=50)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('attendance_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('month', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('attandance_status', models.CharField(max_length=10)),
                ('uploaded_on', models.DateField(auto_now_add=True)),
                ('uploaded_by', models.CharField(blank=True, max_length=50)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
            ],
        ),
    ]
