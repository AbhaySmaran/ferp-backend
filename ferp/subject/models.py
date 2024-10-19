from django.db import models

# Create your models here.


class Subject(models.Model):
    subject_id = models.AutoField(primary_key = True)
    subject_name = models.CharField(max_length=50, blank=True, null=True)
    text_book_1 = models.CharField(max_length=50, blank=True, null=True)
    text_book_2  = models.CharField(max_length=50, blank=True, null=True)
    ref_book_1 = models.CharField(max_length=50, blank=True, null=True)
    ref_book_2 = models.CharField(max_length=50, blank=True, null=True)
    subject_type = models.CharField(max_length=10, blank=True, null=True)
    theory_full_mark = models.IntegerField(blank=True, null=True)
    practical_full_mark = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.subject_name


class SubjectAssignment(models.Model):
    batch = models.CharField(max_length=50)
    sem = models.IntegerField()
    subject_T  = models.CharField(max_length=30, blank=True, null=True)
    sub_T_Teacher = models.CharField(max_length=30, blank=True, null=True)
    subject_P = models.CharField(max_length=30, blank=True, null=True)
    sub_P_Teacher = models.CharField(max_length=30, blank=True, null=True)

    