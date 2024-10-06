from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import *
from api.serializers import *

# class StudentRegisterView(APIView):
#     def post(self, request, format=None):
#         print(request.data)
#         user_data = {
#             "first_name": request.data.get("first_name"),
#             "last_name": request.data.get("last_name"),
#             "email": request.data.get("email"),
#             "password": request.data.get("password"),
#             "username": request.data.get("username"),
#             "role": request.data.get("role"),
#             "st_cat": request.data.get("st_cat"),
#             "dp_image": request.data.get("dp_image"),
#             "dob": request.data.get('dob')
#         }
#         UserSerializer = UserRegistrationSerializer(data = user_data)
#         if UserSerializer.is_valid():
#             UserSerializer.save()
#             return Response("User Created")

#         StudentSerializer = StudentRegisterSerializer(user=UserSerializer ,data=request.data)
#         if StudentSerializer.is_valid():
#             StudentSerializer.save()
#             return Response({"msg": "Student Registered"})
#         return Response(StudentSerializer.errors, UserSerializer.errors)            
        
    

# class StudentRegisterView(APIView):
#     def post(self, request, format=None):
#         # Extract user-related fields
#         user_data = {
#             "first_name": request.data.get("first_name"),
#             "last_name": request.data.get("last_name"),
#             "email": request.data.get("email"),
#             "password": request.data.get("password"),
#             "username": request.data.get("username"),
#             "role": request.data.get("role"),
#             "st_cat": request.data.get("st_cat"),
#             "dp_image": request.data.get("dp_image"),
#             "dob": request.data.get("dob"),
#         }
        
#         # Create User first
#         user_serializer = UserRegistrationSerializer(data=user_data)
#         if user_serializer.is_valid():
#             user = user_serializer.save()  
            
            
#             student_data = request.data.copy()  
#             student_data['user'] = user.id 
            
#             # Create Student
#             student_serializer = StudentRegisterSerializer(data=student_data)
#             if student_serializer.is_valid():
#                 student_serializer.save()
#                 return Response({"msg": "Student Registered Successfully"}, status=201)
#             else:
#                 return Response(student_serializer.errors, status=400)
#         else:
#             return Response(user_serializer.errors, status=400)
        

class StudentRegisterView(APIView):
    def post(self, request, format=None):
        print(request.data)
        student_serializer = StudentRegisterSerializer(data=request.data)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response({"msg": "Student Registered"})
        return Response(student_serializer.errors)