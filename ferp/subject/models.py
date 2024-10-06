from django.db import models

# Create your models here.


class Subject(models.Model):
    subject_id = models.AutoField(primary_key = True)
    subject_name = models.CharField(max_length=50)
    text_book_1 = models.CharField(max_length=50)
    text_book_2  = models.CharField(max_length=50)
    ref_book_1 = models.CharField(max_length=50)
    ref_book_2 = models.CharField(max_length=50)
    subject_type = models.CharField(max_length=10)
    theory_full_mark = models.IntegerField()
    practical_full_mark = models.IntegerField()

    def __str__(self):
        return self.subject_name