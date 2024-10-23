from rest_framework import serializers
from students.models import Student
from .models import *


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'  # This includes all fields from the model

    def create(self, validated_data):
        # Custom logic for creating a new subject can go here if needed
        return Subject.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update each field manually if you want to add custom behavior
        instance.subject_code = validated_data.get('subject_code', instance.subject_code)
        instance.subject_name = validated_data.get('subject_name', instance.subject_name)
        instance.subject_type = validated_data.get('subject_type', instance.subject_type)
        instance.text_book_1 = validated_data.get('text_book_1', instance.text_book_1)
        instance.text_book_2 = validated_data.get('text_book_2', instance.text_book_2)
        instance.ref_book_1 = validated_data.get('ref_book_1', instance.ref_book_1)
        instance.ref_book_2 = validated_data.get('ref_book_2', instance.ref_book_2)
        instance.full_mark = validated_data.get('full_mark', instance.full_mark)
        instance.pass_mark = validated_data.get('pass_mark', instance.pass_mark)

        # Save the updated instance
        instance.save()
        return instance

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['batch']


class SubjectAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectAssignment
        fields = ['batch', 'sem', 'subject_T', 'sub_T_Teacher', 'subject_P', 'sub_P_Teacher']