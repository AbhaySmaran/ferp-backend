from api.models import User
from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password
from api.serializers import RoleSerializer, DepartmentSerializer, StaffCategorySerializer

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    # password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = ['email', 'password', 'role']
        extra_kwargs = {'role': {'read_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    dept = DepartmentSerializer()
    st_cat = StaffCategorySerializer()
    class Meta:
        model = User
        # fields = ["id","user_id","username", "email","first_name","phone", "role", "st_cat","dept","dp_image","signature"]
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def update(self,instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.age = validated_data.get('age', instance.age)
        instance.dp_image = validated_data.get('dp_image', instance.dp_image)
        instance.role = validated_data.get('role', instance.role)
        instance.dept = validated_data.get('dept',instance.dept)
        instance.st_cat = validated_data.get('st_cat', instance.st_cat)
        instance.save()
        return instance

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, write_only=True)
    new_password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(["Old password is not correct"])
        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError(['New password and confirm password do not match'])

        password_validation.validate_password(new_password, self.context['request'].user)
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance