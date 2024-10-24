from django.db import models

# Create your models here.


class Subject(models.Model):
    subject_id = models.AutoField(primary_key = True)
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=50)
    subject_type = models.CharField(max_length=10)
    text_book_1 = models.CharField(max_length=50, blank=True, null=True)
    text_book_2  = models.CharField(max_length=50, blank=True, null=True)
    ref_book_1 = models.CharField(max_length=50, blank=True, null=True)
    ref_book_2 = models.CharField(max_length=50, blank=True, null=True)
    full_mark = models.IntegerField()
    pass_mark = models.IntegerField()

    def __str__(self):
        return self.subject_name


class SubjectAssignment(models.Model):
    batch = models.CharField(max_length=50)
    sem = models.IntegerField(null=True, blank=True)
    subject_T  = models.CharField(max_length=30, blank=True, null=True)
    sub_T_Teacher = models.CharField(max_length=30, blank=True, null=True)
    subject_P = models.CharField(max_length=30, blank=True, null=True)
    sub_P_Teacher = models.CharField(max_length=30, blank=True, null=True)

    