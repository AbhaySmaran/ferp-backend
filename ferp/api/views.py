from rest_framework.response import Response
from rest_framework import status

import csv
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError

from django.core.files.storage import default_storage

from students.models import Student


class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        # data = request.data
        # print("View",data)
        # print("r.data",request.data)
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"msg":"User Created"}, status = status.HTTP_201_CREATED)
        # print ("s.data",serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id, format=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        reset_password = request.data.get('reset_password', False)  # Check for reset_password flag
        context = {'reset_password': reset_password}
        print(request.data)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True, context=context)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if reset_password:
                return Response({"msg": "Password reset successfully."}, status=status.HTTP_200_OK)
            return Response({"msg": "User data updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(APIView):
    def get(self, request, *args, **kwargs):
        Users = User.objects.all()
        serializer = UserSerializer(Users, many=True)
        return Response(serializer.data)

class UserView(APIView):
    def get(self, request, id, format=None):
        user = User.objects.get(id = id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class RoleListView(APIView):
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

class DepartmentListView(APIView):
    def get(self, request,id=None, *args, **kwargs):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        if id is not None:
            dept = Department.objects.get(dept_id=id)
            serializer = DepartmentSerializer(dept)
            return Response(serializer.data)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer = DepartmentSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"Department Added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def put(self, request, id ,format=None):
        dept = Department.objects.get(dept_id=id)
        serializer = DepartmentSerializer(dept, data=request.data, partial=True)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response({"msg": "Data updated"})
        return Response(serializer.errors)

class StaffCategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        staff_categories = StaffCategory.objects.all()
        serializer = StaffCategorySerializer(staff_categories, many=True)
        return Response(serializer.data)
    

# class CSVUploadAPIView(APIView):
#     parser_classes = (MultiPartParser, FormParser)  # To handle file uploads

#     def post(self, request, *args, **kwargs):
#         csv_file = request.FILES.get('csv_file')

#         if not csv_file:
#             return Response({'error': 'No file was provided'}, status=status.HTTP_400_BAD_REQUEST)

#         if not csv_file.name.endswith('.csv'):
#             return Response({'error': 'This is not a CSV file'}, status=status.HTTP_400_BAD_REQUEST)

#         # Read the CSV file
#         try:
#             decoded_file = csv_file.read().decode('utf-8').splitlines()
#             reader = csv.DictReader(decoded_file)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         errors = []
#         for row in reader:
#             try:
#                 # Fetch ForeignKey instances
#                 role = Role.objects.get(id=row['role_id'])
#                 st_cat = StaffCategory.objects.get(id=row['st_cat_id'])
#                 dept = Department.objects.get(id=row['dept_id'])

#                 # Create the user instance
#                 user = User.objects.create(
#                     username=row['username'],
#                     email=row['email'],
#                     role=role,
#                     st_cat=st_cat,
#                     dept=dept,
#                     first_name=row['first_name'],
#                     last_name=row['last_name'],
#                     phone=row['phone'],
#                     dob=row['dob'],
#                     age=int(row['age']),
#                     is_password_renew=bool(row['is_password_renew']),
#                 )
#                 user.set_password(row['password'])  # Set hashed password
#                 user.full_clean()  # Validate the model data
#                 user.save()

#             except ValidationError as ve:
#                 errors.append(f"Error in row {row['username']}: {ve.messages}")
#             except Exception as e:
#                 errors.append(f"Error in row {row['username']}: {str(e)}")

#         if errors:
#             return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'success': 'Users added successfully'}, status=status.HTTP_201_CREATED)


class BulkUserUploadView(APIView):
    def post(self, request, format=None):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        file_path = default_storage.path(file_name)

        try:
            with open(file_path, 'r') as f:
                csv_reader = csv.DictReader(f)
                users = []
                errors = []
                for row in csv_reader:
                    photo = row.get('dp_image', None) 
                    signature = row.get('signature',None)
                    user_data = {
                        "username": row['username'],
                        "email": row['email'],
                        "first_name": row['first_name'],
                        "last_name": row.get('last_name', ''),
                        "password": row['password'],
                        "phone": row.get('phone', ''),
                        "dob": row.get('dob', ''),
                        "age": row.get('age', None),
                        "address": row.get('address', ''),
                        "role": row['role'],
                        "st_cat": row.get('st_cat', None),
                        "dept": row.get('dept', None),
                        
                    }

                    if photo:
                        user_data['dp_image'] = photo
                    if signature:
                        user_data['signature'] = signature
                    serializer = UserUploadSerializer(data=user_data)
                    if serializer.is_valid():
                        users.append(serializer)
                    else:
                        errors.append(serializer.errors)
                
                if errors:
                    return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
                
                for user_serializer in users:
                    user_serializer.save()

            return Response({"success": "Users uploaded successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class StatisticsAPIView(APIView):
    
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        total_students = Student.objects.all().count()       
        total_faculty = User.objects.filter(role__role='faculty').count()      
        total_students_in_hostel = Student.objects.filter(hostel='yes').count()
        male_students = Student.objects.filter(gender = 'Male').count()
        female_students = Student.objects.filter(gender = 'Female').count()
        hostel1_students = Student.objects.filter(hostel_name = 'hostel1').count()
        hostel2_students = Student.objects.filter(hostel_name = 'hostel2').count()

        # Create the data dictionary
        data = {
            'total_students': total_students,
            'total_faculty': total_faculty,
            'total_students_in_hostel': total_students_in_hostel,
            'male_students' : male_students,
            'female_students' : female_students,
            'hostel1_students' : hostel1_students,
            'hostel2_students' : hostel2_students
        }

        # Serialize the data
        serializer = StatisticsSerializer(data)
        return Response(serializer.data)



class FacultyUserListView(APIView):
    def get(self, request):
        # Get the "faculty" role instance
        faculty_role = Role.objects.filter(role='faculty').first()  # Adjust to match the role field
        if faculty_role:
            faculty_users = User.objects.filter(role=faculty_role)
            serializer = FacultyUserSerializer(faculty_users, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Faculty role not found"}, status=400)