from django.db import models
from api.models import User, Role, StaffCategory,Department
from course.models import Course
# Create your models here.

from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default = 2)
    st_cat = models.ForeignKey(StaffCategory, on_delete=models.CASCADE, default = 2 )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=50, null=True, blank=True)
    lateral = models.CharField(max_length=3, blank=True, null=True)
    batch = models.CharField(max_length=20, blank=True, null=True)
    college = models.CharField(max_length=100, blank=True, null=True)
    hostel = models.CharField(max_length=3, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    transport = models.CharField(max_length=3 , blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    caste = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    last_exam_passed = models.CharField(max_length=100, blank=True, null=True)
    board = models.CharField(max_length=100, blank=True, null=True)
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    year_passing = models.IntegerField(blank=True, null=True)
    total_marks = models.IntegerField(blank=True, null=True)
    marks_secured = models.IntegerField(blank=True, null=True)
    cgpa_or_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, default='Active')
    registered_on = models.DateField(auto_now_add=True)
    registered_by = models.CharField(max_length=100, blank=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
