# Generated by Django 2.2.28 on 2024-10-19 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=50)),
                ('text_book_1', models.CharField(max_length=50)),
                ('text_book_2', models.CharField(max_length=50)),
                ('ref_book_1', models.CharField(max_length=50)),
                ('ref_book_2', models.CharField(max_length=50)),
                ('subject_type', models.CharField(max_length=10)),
                ('theory_full_mark', models.IntegerField()),
                ('practical_full_mark', models.IntegerField()),
            ],
        ),
    ]
