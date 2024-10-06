from django.db import models

# Create your models here.
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    no_of_sem = models.IntegerField()
    course_duration = models.IntegerField()


    
