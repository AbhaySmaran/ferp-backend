from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from api.models import User
from .serializers import *
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated

def get_tokens_for_user(user): 
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserLoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            if not email or not password:
                return Response({"errors": {"error": ["Email and password required"]}}, status=status.HTTP_400_BAD_REQUEST)
            
            if not User.objects.filter(email=email).exists():
                return Response({"errors": {"error":["User does not exist"]}}, status=status.HTTP_404_NOT_FOUND)      

            user = authenticate(email=email, password=password)

            print(serializer.data)
            print(user)
            if user is not None :
                tokens = get_tokens_for_user(user)
                return Response({
                    "message": "Login successful",
                    "tokens": tokens,
                    "role": user.role.role_id
                }, status=status.HTTP_200_OK)
            return Response({"errors": {"error": ["Invalid credentials"]}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id,format = None):
        user = User.objects.get(id = id)
        serializer = UserProfileSerializer(user, data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response({"msg": "Data Updated Successfully"}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)