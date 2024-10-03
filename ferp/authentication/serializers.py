from api.models import User
from rest_framework import serializers

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    # password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = ['email', 'password', 'role']
        extra_kwargs = {'role': {'read_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ["id","user_id","username", "email","first_name","phone", "role", "st_cat","dept","dp_image","signature"]
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def update(self,instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.age = validated_data.get('age', instance.age)
        instance.dp_image = validated_data.get('dp_image', instance.dp_image)

        return instance
