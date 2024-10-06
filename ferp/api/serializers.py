from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import os
from datetime import datetime

# class UserLoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255)
#     # password = serializers.CharField(write_only=True) 
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'role']
#         extra_kwargs = {'role': {'read_only': True}}

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255)
    class Meta:
        model = User
        fields = ["username", "password","email","first_name","age", "dob","phone", "role", "st_cat","dept","dp_image","signature"]
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        # print(validated_data)
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    # def validate_dp_image(self, file):
    #     allowed_extensions = ['.jpeg', '.jpg', '.png']
    #     file_extension = os.path.splitext(file.name)[1].lower()

    #     errors = []
    #     if file_extension not in allowed_extensions:
    #         errors.append("Only JPEG, JPG, and PNG files are allowed.")
        
    #     if file.size > 10 * 1024 * 1024:  # 15 MB
    #         errors.append("File size must be less than 10 MB.")
        
    #     if errors:
    #         raise serializers.ValidationError(" ".join(errors))
        
    #     return file
    
    def validate_dp_image(self, value):
        if value is None:
            return None  # No file uploaded, it's okay
        return value

    def validate_signature(self, value):
        if value is None:
            return None  # No file uploaded, it's okay
        return value

    # def validate_signature(self,file): 
    #     allowed_extensions = ['.jpeg', '.jpg', '.png']
    #     file_extension = os.path.splitext(file.name)[1].lower()

    #     errors = []
    #     if file_extension not in allowed_extensions:
    #         errors.append("Only JPEG, JPG, and PNG files are allowed.")
        
    #     if file.size > 5 * 1024 * 1024:  # 15 MB
    #         errors.append("File size must be less than 5 MB.")
        
    #     if errors:
    #         raise serializers.ValidationError(" ".join(errors))
        
    #     return file

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # fields = ["id","user_id","username", "email","first_name","phone", "role", "st_cat","dept","dp_image","signature"]
#         fields = '__all__'
#         extra_kwargs = {'password': {'write_only': True}}

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

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    dept = DepartmentSerializer()
    st_cat = StaffCategorySerializer()
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


        

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        # Update basic fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.dp_image = validated_data.get('dp_image', instance.dp_image)
        instance.age = validated_data.get('age', instance.age)
        # Check if reset password action is requested
        if 'reset_password' in self.context:
            # Get current date in 'ddmmyy' format
            current_date = datetime.now().strftime('%d%m%y')
            instance.set_password(current_date)

        instance.save()
        return instance


class UserCSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'st_cat', 'dept', 'first_name', 'last_name', 'phone', 'dob', 'age', 'is_password_renew', 'password']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Ensure password is hashed
        user.save()
        return user


