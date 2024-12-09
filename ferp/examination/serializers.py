from .models import *
from rest_framework import serializers

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

    def create(self,validated_data):
        return Exam.objects.create(**validated_data)
    
    
