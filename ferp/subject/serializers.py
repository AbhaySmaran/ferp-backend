from rest_framework import serializers
from students.models import Student
from .models import *

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['batch']


class SubjectAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectAssignment
        fields = ['batch', 'sem', 'subject_T', 'sub_T_Teacher', 'subject_P', 'sub_P_Teacher']