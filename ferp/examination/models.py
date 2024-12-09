from django.db import models
from api.models import User

# Create your models here.
class Exam(models.Model):
    id = models.BigAutoField(primary_key=True)
    exam_type= models.CharField(max_length=20)
    exam_date = models.DateField()
    exam_duration = models.FloatField()
    marks_for_correct_ans = models.FloatField()
    is_negative_marking = models.BooleanField()
    negative_mark_per_qn = models.IntegerField(default=0)
    exam_created_by = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
    exam_for = models.PositiveSmallIntegerField()
    batch = models.CharField(max_length=50, blank=True)
    exam_year = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        # Automatically set exam_year to the year of exam_date
        if self.exam_date:
            self.exam_year = self.exam_date.year
        super().save(*args, **kwargs)