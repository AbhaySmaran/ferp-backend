from rest_framework import serializers
from students.models import Student

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['batch']