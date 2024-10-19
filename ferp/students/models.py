from django.db import models
from api.models import User, Role, StaffCategory,Department
from course.models import Course

from datetime import datetime
import os
import time

class Student(models.Model):
    student_id = models.BigAutoField(primary_key=True)
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
    batch = models.CharField(max_length=20)
    college = models.CharField(max_length=100, blank=True, null=True)
    hostel = models.CharField(max_length=10, null=True, blank=True)
    hostel_name = models.CharField(max_length = 20, null=True, blank=True)
    room_no = models.CharField(max_length = 10, blank=True, null=True)
    dob = models.CharField(max_length=20,blank=True, null=True)
    transport = models.CharField(max_length=3 , blank=True, null=True)
    gender = models.CharField(max_length=10)
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
    cgpa_or_percentage = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=10, default='Active')
    registered_on = models.DateField(auto_now_add=True)
    registered_by = models.CharField(max_length=100, blank=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def document_upload_to(instance, filename):
    timestamp = int(time.time())    
    extension = os.path.splitext(filename)[1]    
    new_filename = f"{instance.document_name}_{timestamp}{extension}"
    return f"document_files/{instance.student.batch}/{instance.student.student_id}/{new_filename}"
    


class student_documents(models.Model):
    doc_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100)
    document_file = models.FileField( upload_to=document_upload_to)
    uploaded_on = models.DateField(auto_now_add=True)
    uploaded_by = models.CharField(max_length = 50, blank=True)

    def __str__(self):
        return self.document_name



class Attendance(models.Model):
    attendance_id = models.BigAutoField(primary_key = True)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    month = models.CharField(max_length = 20)
    date = models.DateField()
    attandance_status = models.CharField(max_length=10)
    uploaded_on = models.DateField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.attendance_id