from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import *
from api.serializers import *
from django.db import transaction
import csv

from rest_framework import status

from django.http import JsonResponse
from rest_framework.decorators import api_view

from django.core.files.storage import default_storage


class StudentRegisterView(APIView):
    def post(self, request, format=None):
        print(request.data)
        student_serializer = StudentRegisterSerializer(data=request.data)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response({"msg": "Student Registered"})
        return Response(student_serializer.errors)


@api_view(['POST'])
def upload_students_csv(request):
    if 'file' not in request.FILES:
        print("file not uploaded")
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    print(file)
    file_name = default_storage.save(file.name, file)
    file_path = default_storage.path(file_name)

    total_records = 0  # To track the number of successfully created records
    failed_rows = []  # To track rows that failed processing

    try:
        with open(file_path, 'r') as f:
            csv_reader = csv.DictReader(f)
            students = []

            for row_number, row in enumerate(csv_reader, start=1):
                try:
                    # First, create the User object
                    photo = row.get('Photo', None)  # Handle optional Photo field
                    user_data = {
                        "username": row['UserName'],
                        "email": row['Email'],
                        "first_name": row['First_Name'],
                        "last_name": row['Last_Name'],
                        "password": row['Password'],  # Will be hashed in the next step
                        "role": row['Role'],
                        "st_catF":row['Staff_Category'],
                        "dob": row['DOB']
                    }

                    if photo:
                        user_data['dp_image'] = photo
                    # print(user_data)
                    user_serializer = UserRegistrationSerializer(data=user_data)

                    if user_serializer.is_valid():
                        user = user_serializer.save()
                        user.set_password(user_data['password'])  # Hash the password
                        user.save()

                        # Now create the Student object with the User object linked
                        student_data = {
                            "user": user.id, 
                            # "student_id": row['Student_ID'],
                            "email": row["Email"],
                            "first_name": row['First_Name'],
                            "last_name": row['Last_Name'],
                            "email": row['Email'],
                            "password": row['Password'],
                            "role": row['Role'],
                            "staff_category": row['Staff_Category'],
                            "course": row['Course'],
                            "photo": row['Photo'],
                            "roll_number": row['Roll_Number'],
                            "lateral": row['Lateral'],
                            "batch": row['Batch'],
                            "college": row['College'],
                            "hostel": row['Hostel'],
                            "dob": row['DOB'],
                            "transport": row['Transport'],
                            "gender": row['Gender'],
                            "blood_group": row['Blood_Group'],
                            "caste": row['Caste'],
                            "religion": row['Religion'],
                            "mother_tongue": row['Mother_Tongue'],
                            "nationality": row['Nationality'],
                            "last_exam_passed": row['Last_Exam_Passed'],
                            "board": row['Board'],
                            "institute_name": row['Institute_Name'],
                            "year_passing": row['Year_Passing'],
                            "total_marks": row['Total_Marks'],
                            "marks_secured": row['Markes_Secured'],
                            "cgpa_or_percentage": row['CGPA_OR_Percentage'],
                            "status": row['Status'],
                            "section": row['Section'],
                        }
                        # print(student_data)
                        student_serializer = BulkStudentRegisterSerializer(data=student_data)

                       

                        if student_serializer.is_valid():
                            students.append(student_serializer)
                            total_records += 1  # Increment success count
                        else:
                            # Add the row number and error details for failed student data
                            failed_rows.append({
                                "row_number": row_number,
                                "errors": student_serializer.errors
                            })

                    else:
                        # Add the row number and error details for failed user data
                        failed_rows.append({
                            "row_number": row_number,
                            "errors": user_serializer.errors
                        })

                except Exception as e:
                    # Catch any other exceptions and log the row number and error message
                    failed_rows.append({
                        "row_number": row_number,
                        "errors": str(e)
                    })

            # Save all student objects after processing
            for student_serializer in students:
                student_serializer.save()

        # Create the success response including the total number of created records
        response_data = {
            "success": f"Data uploaded successfully. {total_records} records created.",
            "failed_records": failed_rows  # Provide details of rows that failed processing
        }

        # If there are any failed rows, add a warning in the response
        if failed_rows:
            response_data["warning"] = f"{len(failed_rows)} records failed validation."

        return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







# @api_view(['POST'])
# def upload_students_csv(request):
#     if 'file' not in request.FILES:
#         print("file not uploaded")
#         return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

#     file = request.FILES['file']
#     print(file)
#     file_name = default_storage.save(file.name, file)
#     file_path = default_storage.path(file_name)

#     total_records = 0  
#     failed_rows = [] 

#     try:
#         with open(file_path, 'r') as f:
#             csv_reader = csv.DictReader(f)
#             students = []

#             for row in csv_reader:
#                 try:
                    
#                     # First, create the User object
#                     photo = row.get('Photo', "")
#                     print("photo",photo)

#                     user_data = {
#                         "username": row['UserName'],
#                         "email": row['Email'],
#                         "first_name": row['First_Name'],
#                         "last_name": row['Last_Name'],
#                         "password": row['Password'],  # Will be hashed in the next step
#                         "role": row['Role'],
                        
#                         "dob": row['DOB']
#                     }

#                     if photo:
#                         user_data['dp_image'] = photo

#                     print(user_data)
#                     user_serializer = UserRegistrationSerializer(data=user_data)

#                     if user_serializer.is_valid():
#                         user = user_serializer.save()
#                         user.set_password(user_data['password'])  # Hash the password
#                         user.save()
#                         print(user)
#                         print(user.id)
#                         # Now create the Student object with the User object linked
#                         student_data = {
#                             "user": user.id, 
#                             "student_id": row['Student_ID'],
#                             "email": row["Email"],
#                             "first_name": row['First_Name'],
#                             "last_name": row['Last_Name'],
#                             "email": row['Email'],
#                             "password": row['Password'],
#                             "role": row['Role'],
#                             "staff_category": row['Staff_Category'],
#                             "course": row['Course'],
#                             "photo": row['Photo'],
#                             "roll_number": row['Roll_Number'],
#                             "lateral": row['Lateral'],
#                             "batch": row['Batch'],
#                             "college": row['College'],
#                             "hostel": row['Hostel'],
#                             "dob": row['DOB'],
#                             "transport": row['Transport'],
#                             "gender": row['Gender'],
#                             "blood_group": row['Blood_Group'],
#                             "caste": row['Caste'],
#                             "religion": row['Religion'],
#                             "mother_tongue": row['Mother_Tongue'],
#                             "nationality": row['Nationality'],
#                             "last_exam_passed": row['Last_Exam_Passed'],
#                             "board": row['Board'],
#                             "institute_name": row['Institute_Name'],
#                             "year_passing": row['Year_Passing'],
#                             "total_marks": row['Total_Marks'],
#                             "marks_secured": row['Markes_Secured'],
#                             "cgpa_or_percentage": row['CGPA_OR_Percentage'],
#                             "status": row['Status'],
#                         }
#                         print(student_data)
#                         student_serializer = BulkStudentRegisterSerializer(data=student_data)

#                         if student_serializer.is_valid():
#                             print("valid student data")
#                             students.append(student_serializer)
#                             # print(student_serializer)
#                         else:
#                             print(student_serializer.errors)  # Validation errors
#                             return Response({"error": "Invalid student data in CSV"}, status=status.HTTP_400_BAD_REQUEST)
#                     else:
#                         print(user_serializer.errors)  # Validation errors
#                         return Response({"error": "Invalid user data in CSV"}, status=status.HTTP_400_BAD_REQUEST)
#                 except Exception as e:
#                     print(f"Error creating user/student: {str(e)}")
#                     return Response({"error": f"Failed to process row: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

#             # Save all student objects after processing
#             for student_serializer in students:
#                 student_serializer.save()

#         return Response({"success": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)

#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentListView(APIView):
    def get(self, request, format = None):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
        

class StudentsView(APIView):
    def get(self, request, format= None):
        students = Student.objects.all()
        serializer = StudentViewSerializer(students, many = True)
        return Response(serializer.data)

class StudentIndivisulaView(APIView):
    def get(self, request, id, format=None):
        student = Student.objects.get(student_id=id)
        serializer = StudentViewSerializer(student)
        return Response(serializer.data)

        


class AttendanceView(APIView):
    def post(self, request, year, month, day):
        
        
        date_str = f"{year}-{month}-{day}"
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format"})
        
        
        data = request.data.get("attendance_data", [])
        if not data:
            return Response({"error": "No attendance data provided"})

        
        attendance_records = []
        for item in data:
            print(item)
            student_id = item.get("student_id")
            status = item.get("status")
            uploaded_by = item.get("uploaded_by")

            try:
                student = Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                return Response({"error": f"Student with id {student_id} not found"})
            
            
            attendance_record = {
                "student": student.student_id,
                "month": month,
                "date": date,
                "attandance_status": status,
                "uploaded_by": uploaded_by,
                # "uploaded_by": request.user.username if request.user.is_authenticated else "Anonymous"
            }
            print(attendance_record)
            serializer = AttendanceSerializer(data=attendance_record)
            if serializer.is_valid():
                attendance_records.append(serializer.save())
            else:
                print(serializer.errors)
                return Response(serializer.errors)

        return Response({"message": "Attendance successfully logged"})

    def get(self, request, year, month, day):
        
        date_str = f"{year}-{month}-{day}"
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        attendance_records = Attendance.objects.filter(date=date)
        if not attendance_records.exists():
            return Response({"message": "No attendance records found for this date"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class StudentUpdateView(APIView):
    def get_object(self, id):
        try:
            return Student.objects.get(pk=id)
        except Student.DoesNotExist:
            return None

    def put(self, request, id):
        student = Student.objects.get(student_id=id)
        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        reset_password = request.data.get('reset_password', False)  
        context = {'reset_password': reset_password}
        print(request.data)        

        serializer = StudentUpdateSerializer(student, data=request.data, partial=True, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DistinctBatchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        distinct_batches = Student.objects.values_list('batch', flat=True).distinct()
        return Response(distinct_batches)


class StudentsByBatchAPIView(APIView):
    def get(self, request, batch):
       
        students = Student.objects.filter(batch=batch)
        if students.exists():
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No students found for this batch."}, status=status.HTTP_404_NOT_FOUND)
        

class DistinctBatchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        distinct_batches = Student.objects.values_list('batch', flat=True).distinct()
        return Response(distinct_batches)