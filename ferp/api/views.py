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
    

class BulkUserUploadView(APIView):
    def post(self, request, format=None):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        file_path = default_storage.path(file_name)

        total_records = 0
        failed_rows = []

        try:
            with open(file_path, 'r') as f:
                csv_reader = csv.DictReader(f)
                users = []

                for row_number, row in enumerate(csv_reader, start=1):
                    photo = row.get('dp_image', None)
                    signature = row.get('signature', None)
                    user_data = {
                        "username": row['Username'],
                        "email": row['Email'],
                        "first_name": row['First Name'],
                        "last_name": row.get('Last Name', ''),
                        "password": row['Password'],
                        "phone": row.get('Phone', ''),
                        "dob": row.get('DOB', ''),
                        "age": row.get('Age', None),
                        "address": row.get('Address', ''),
                        "role": row['Role'],
                        "st_cat": row.get('Staff Category', None),
                        "dept": row.get('Department', None),
                        "gender": row.get('Gender', None)
                    }

                    if photo:
                        user_data['Dp Image'] = photo
                    if signature:
                        user_data['Signature'] = signature

                    serializer = UserUploadSerializer(data=user_data)
                    
                    if serializer.is_valid():
                        users.append(serializer)
                        total_records += 1
                    else:
                        # Log the row number and serializer errors
                        failed_rows.append({
                            "row_number": row_number,
                            "errors": serializer.errors
                        })

                # Save all valid user objects after processing
                for user_serializer in users:
                    user_serializer.save()

            # Create response data with the total records and any failed rows
            response_data = {
                "success": f"Users uploaded successfully. {total_records} records created.",
                "failed_records": failed_rows
            }

            # Add a warning if there are any failed rows
            if failed_rows:
                response_data["warning"] = f"{len(failed_rows)} records failed validation."

            return Response(response_data, status=status.HTTP_201_CREATED)

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