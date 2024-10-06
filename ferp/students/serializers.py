from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password  # For hashing password


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

# class StudentRegisterSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=100)
#     dp_image = serializers.ImageField(required=False, allow_null=True) 
#     class Meta:
#         model = Student
#         fields = ["dp_image","username", 'first_name',"user", 'last_name', 'email', 'password', 'role', 'st_cat','course', 'roll_number',
#                   'lateral', 'batch', 'college', 'hostel', 'dob', 'transport', 'gender', 'blood_group', 'caste','religion',
#                   'mother_tongue', 'nationality', 'last_exam_passed', 'board','institute_name', 'total_marks','year_passing',
#                   'marks_secured', 'cgpa_or_percentage', 'status', 'registered_on', 'registered_by']

#         def create(self, validated_data):
#             student_data = validated_data.copy()
#             student_data.pop('username')
#             student_data.pop('dp_image')
#             return Student.objects.create(**student_data)

class StudentRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)  # This field belongs to the User model
    dp_image = serializers.ImageField(required=False, allow_null=True)  # This field belongs to the User model

    class Meta:
        model = Student
        fields = [
            "dp_image", "username", 'first_name', 'last_name', 'email', 'password', 'role', 
            'st_cat', 'course', 'roll_number', 'lateral', 'batch', 'college', 'hostel', 'dob', 
            'transport', 'gender', 'blood_group', 'caste', 'religion', 'mother_tongue', 'nationality', 
            'last_exam_passed', 'board', 'institute_name', 'total_marks', 'year_passing', 'marks_secured', 
            'cgpa_or_percentage', 'status', 'registered_on', 'registered_by'
        ]

    def create(self, validated_data):
        # Extract fields related to the User model
        username = validated_data.pop('username')
        dp_image = validated_data.pop('dp_image', None)
        # password = validated_data.pop('password')

        # Create User object
        user_data = {
            'username': username,
            'dp_image': dp_image,
            'email': validated_data.get('email'),
            'password': validated_data.get('password'),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name'),
            'role': validated_data.get('role'),
            'st_cat': validated_data.get('st_cat'),
            'dob': validated_data.get('dob'),
        }
        user = User.objects.create_user(**user_data)
        user.save()
        password = validated_data.pop('password')

        # Hash the password before creating the User
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password

        # Now create the Student object, passing the User object as the ForeignKey
        student = Student.objects.create(user=user, **validated_data)
        return student

    