from api.models import User
from rest_framework import serializers

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    # password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = ['email', 'password', 'role']
        extra_kwargs = {'role': {'read_only': True}}