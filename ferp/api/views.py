from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.authentication import SessionAuthentication

# def get_tokens_for_user(user): 
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

# class UserLoginView(APIView):

#     def post(self, request, *args, **kwargs):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.data.get('email')
#             password = serializer.data.get('password')

#             if not email or not password:
#                 return Response({"errors": {"error": ["Email and password required"]}}, status=status.HTTP_400_BAD_REQUEST)
            
#             if not User.objects.filter(email=email).exists():
#                 return Response({"errors": {"error":["User does not exist"]}}, status=status.HTTP_404_NOT_FOUND)      

#             user = authenticate(email=email, password=password)

#             print(serializer.data)
#             print(user)
#             if user is not None :
#                 tokens = get_tokens_for_user(user)
#                 return Response({
#                     "message": "Login successful",
#                     "tokens": tokens,
#                     "role": user.role.role_id
#                 }, status=status.HTTP_200_OK)
#             return Response({"errors": {"error": ["Invalid credentials"]}}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# {"errors": {"error": ["Invalid credentials"]}}
# from django.views.decorators.csrf import csrf_exempt
# from django.middleware.csrf import get_token
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# Exempt the view from CSRF verification for API purposes
# from django.contrib.auth import authenticate, login
# from django.middleware.csrf import get_token

# class UserLoginView(APIView):

#     def post(self, request, *args, **kwargs):
#         serializer = UserLoginSerializer(data=request.data)
#         print(request.data)
#         if serializer.is_valid():
#             email = request.data.get('email')
#             password = request.data.get('password')

#             user = authenticate(email=email, password=password)
#             if user is not None:
#                 login(request, user)  # Log in the user to start the session

#                 # Return CSRF token for frontend
#                 csrf_token = get_token(request)

#                 return Response({
#                     "message": "Login successful",
#                     "csrf_token": csrf_token  # Pass CSRF token for future requests
#                 }, status=status.HTTP_200_OK)
#             return Response({"errors": {"error": ["Invalid credentials"]}}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        # data = request.data
        # print("View",data)
        print("r.data",request.data)
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"msg":"User Created"}, status = status.HTTP_201_CREATED)
        print ("s.data",serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class UserProfileView(APIView):
#     permission_classes=[IsAuthenticated]

#     def get(self,request):
#         serializer = UserProfileSerializer(request.user)
#         return Response(serializer.data)

# class UserUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, id,format = None):
#         user = User.objects.get(id = id)
#         serializer = UserProfileSerializer(user, data = request.data)

class UserListView(APIView):
    def get(self, request, *args, **kwargs):
        Users = User.objects.all()
        serializer = UserSerializer(Users, many=True)
        return Response(serializer.data)

class RoleListView(APIView):
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

class DepartmentListView(APIView):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

class StaffCategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        staff_categories = StaffCategory.objects.all()
        serializer = StaffCategorySerializer(staff_categories, many=True)
        return Response(serializer.data)
    