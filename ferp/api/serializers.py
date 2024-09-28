from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import os

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    # password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = ['email', 'password', 'role']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255)
    class Meta:
        model = User
        fields = ["username", "password","email","first_name","phone", "role", "st_cat","dept","dp_image","signature"]
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    def validate_dp_image(self, file):
        allowed_extensions = ['.jpeg', '.jpg', '.png']
        file_extension = os.path.splitext(file.name)[1].lower()

        errors = []
        if file_extension not in allowed_extensions:
            errors.append("Only JPEG, JPG, and PNG files are allowed.")
        
        if file.size > 10 * 1024 * 1024:  # 15 MB
            errors.append("File size must be less than 10 MB.")
        
        if errors:
            raise serializers.ValidationError(" ".join(errors))
        
        return file

    def validate_signature(self, file):
        allowed_extensions = ['.jpeg', '.jpg', '.png']
        file_extension = os.path.splitext(file.name)[1].lower()

        errors = []
        if file_extension not in allowed_extensions:
            errors.append("Only JPEG, JPG, and PNG files are allowed.")
        
        if file.size > 5 * 1024 * 1024:  # 15 MB
            errors.append("File size must be less than 5 MB.")
        
        if errors:
            raise serializers.ValidationError(" ".join(errors))
        
        return file

class UserProfileView(serializers.ModelSerializer):
    class Mete:
        model = User
        # fields = ["id","user_id","username", "email","first_name","phone", "role", "st_cat","dept","dp_image","signature"]
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role', 'description']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['dept_id', 'dept_name', 'dept_abbr', 'authority']

class StaffCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffCategory
        fields = ['st_cat_id', 'st_cat_name', 'code']