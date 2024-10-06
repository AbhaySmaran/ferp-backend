from api.models import User
from rest_framework import serializers

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    # password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = ['email', 'password', 'role']
        extra_kwargs = {'role': {'read_only': True}}





from django.shortcuts import render
from api.models import User
from .serializers import *
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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



from django.urls import path
from .views import *
urlpatterns = [
    path("user/login/", UserLoginView.as_view()),
]






# @api_view(['POST'])
# def upload_students_csv(request):

#     if 'file' not in request.FILES:
#         print("file not uploaded")
#         return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

#     file = request.FILES['file']
#     # print(file)
#     file_name = default_storage.save(file.name, file)
#     file_path = default_storage.path(file_name)
#     # print(file_path)
#     try:
#         with open(file_path, 'r') as f:
#             csv_reader = csv.DictReader(f)
#             students = []
#             # print(row)
#             for row in csv_reader:
#                 # print(row)
#                 student_data = {
#                     # "user":row['user'],
#                     # "student_id": row['Stident_ID'],
#                     "first_name": row['First_Name'],
#                     "last_name": row['Last_Name'],
#                     "username": row['UserName'],
#                     "email": row['Email'],
#                     "password": row['Password'],
#                     "role": row['Role'],
#                     "staff_category": row['Staff_Category'],
#                     "course": row['course'],
#                     "photo": row['Photo'],
#                     "roll_number": row['Roll_Number'],
                    
#                     "lateral": row['Lateral'],
#                     "batch": row['Batch'],
#                     "college": row['College'],
#                     "hostel": row['Hostel'],
#                     "dob": row['DOB'],
#                     "transport": row['Transport'],
#                     "gender": row['Gender'],
#                     "blood_group": row['Blood_Group'],
#                     "caste": row['Caste'],
#                     "religion": row['Religion'],
#                     "mother_tongue": row['Mother_Tongue'],
#                     "nationality": row['Nationality'],
#                     "last_exam_passed": row['Last_Exam_Passed'],
#                     "board": row['Board'],
#                     "institute_name": row['Institute_Name'],
#                     "year_passing": row['Year_Passing'],
#                     "total_marks": row['Total_Marks'],
#                     "marks_secured": row['Markes_Secured'],
#                     "cgpa_or_percentage": row['CGPA_OR_Percentage'],
#                     "status": row['Status'],
#                 }
#                 print(student_data)
#                 serializer = StudentRegisterSerializer(data=student_data)

#                 if serializer.is_valid():
#                     print("file is valid")
#                     students.append(serializer)

#                 else:
#                     print(serializer.errors)  # This will print the validation errors
#                     return Response({"error": "Invalid data in CSV"}, status=status.HTTP_400_BAD_REQUEST)

#             for student_serializer in students:
#                 student_serializer.save()

#         return Response({"success": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)