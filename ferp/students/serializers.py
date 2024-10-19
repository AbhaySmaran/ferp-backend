from rest_framework import serializers
from .models import *
from api.serializers import *
from django.contrib.auth.hashers import make_password  #For hashing password
# from course.serializers import *

class StudentSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Student
        fields = '__all__'

# class StudentRegisterSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=100)
#     dp_image = serializers.ImageField(required=False, allow_null=True) 
#     class Meta:
#         model = Student
#         fields = ["dp_image","username", 'first_name',"user", 'last_name', 'email', 'password', 'role', 'st_cat','course', 'roll_number',
#                   'lateral', 'batch', 'college', 'hostel', 'dob', 'transport', 'gender', 'blood_group', 'caste','religion',
#                   'mother_tongue', 'nationality', 'last_exam_passed', 'board','institute_name', 'total_marks','year_passing',
#                   'marks_secured', 'cgpa_or_percentage', 'status', 'registered_on', 'registered_by']

#         def create(self, validated_data):
#             student_data = validated_data.copy()
#             student_data.pop('username')
#             student_data.pop('dp_image')
#             return Student.objects.create(**student_data)

class StudentRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)  # This field belongs to the User model
    dp_image = serializers.ImageField(required=False, allow_null=True)  # This field belongs to the User model

    class Meta:
        model = Student
        fields = [
            "dp_image", "username", 'first_name', 'last_name', 'email', 'password', 'role', 
            'st_cat', 'course', 'roll_number', 'lateral', 'batch', 'college', 'hostel', 'dob', 
            'transport', 'gender', 'blood_group', 'caste', 'religion', 'mother_tongue', 'nationality', 
            'last_exam_passed', 'board', 'institute_name', 'total_marks', 'year_passing', 'marks_secured', 
            'cgpa_or_percentage', 'status', 'registered_on', 'registered_by'
        ]

    def create(self, validated_data):
        # Extract fields related to the User model
        username = validated_data.pop('username')
        dp_image = validated_data.pop('dp_image', None)
        # password = validated_data.pop('password')

        # Create User object
        user_data = {
            'username': username,
            'dp_image': dp_image,
            'email': validated_data.get('email'),
            'password': validated_data.get('password'),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name'),
            'role': validated_data.get('role'),
            'st_cat': validated_data.get('st_cat'),
            'dob': validated_data.get('dob'),
        }
        user = User.objects.create_user(**user_data)
        user.save()
        password = validated_data.pop('password')

        # Hash the password before creating the User
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password

        # Now create the Student object, passing the User object as the ForeignKey
        student = Student.objects.create(user=user, **validated_data)
        return student


class BulkStudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "user",'first_name', 'last_name', 'email', 'password', 'role', 
            'st_cat', 'course', 'roll_number', 'lateral', 'batch', 'college', 'hostel', 'dob', 
            'transport', 'gender', 'blood_group', 'caste', 'religion', 'mother_tongue', 'nationality', 
            'last_exam_passed', 'board', 'institute_name', 'total_marks', 'year_passing', 'marks_secured', 
            'cgpa_or_percentage', 'status', 'registered_on', 'registered_by'
        ]

    def create(self, validated_data):
            password = validated_data.pop('password')

        
            hashed_password = make_password(password)
            validated_data['password'] = hashed_password

            # Now create the Student object, passing the User object as the ForeignKey
            student = Student.objects.create(**validated_data)
            return student




class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['attendance_id', 'student', 'month', 'date', 'attandance_status', 'uploaded_on', 'uploaded_by']

    def validate(self, data):
        # Ensure attendance for the same student and date is not logged twice
        if Attendance.objects.filter(student=data['student'], date=data['date']).exists():
            raise serializers.ValidationError("Attendance for these students on this date has already been logged.")
        return data


class StudentViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = '__all__'




class StudentUpdateSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=100)  
    dp_image = serializers.ImageField(required=False, allow_null=True)  
    phone = serializers.CharField(max_length = 15, required=False)
    age = serializers.IntegerField(required=False)
    class Meta:
        model = Student
        fields = [
            "dp_image",'first_name', 'last_name', 'email', 'role', 'password',
            'st_cat', 'course', 'roll_number', 'lateral', 'batch', 'college', 'hostel', 'dob', 
            'transport', 'gender', 'blood_group', 'caste', 'religion', 'mother_tongue', 'nationality', 
            'last_exam_passed', 'board', 'institute_name', 'total_marks', 'year_passing', 'marks_secured', 
            'cgpa_or_percentage', 'status','phone','age'
        ]
        
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        # Handle updating the User model fields
        user = instance.user
        user.username = validated_data.get('username', user.username)
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.email = validated_data.get('email', user.email)
        user.dp_image = validated_data.get('dp_image', user.dp_image)
        user.dob = validated_data.get('dob', user.dob)
        user.phone = validated_data.get('phone', user.phone)
        user.age = validated_data.get('age',user.age)
        # user.status = validated_data.get('status',user.status)

        if 'reset_password' in self.context:
            # Get current date in 'ddmmyy' format
            current_date = datetime.now().strftime('%d%m%y')
            
            user.set_password(current_date)

            # instance.paassword = current_date

            # password = validated_data.pop('password')

            # Hash the password before creating the User
            # hashed_password = make_password(password)
            # validated_data['password'] = hashed_password


        user.save()

        # Update the remaining fields of the Student model
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.course = validated_data.get('course', instance.course)
        instance.roll_number = validated_data.get('roll_number', instance.roll_number)
        instance.lateral = validated_data.get('lateral', instance.lateral)
        instance.batch = validated_data.get('batch', instance.batch)
        instance.college = validated_data.get('college', instance.college)
        instance.hostel = validated_data.get('hostel', instance.hostel)
        instance.transport = validated_data.get('transport', instance.transport)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.blood_group = validated_data.get('blood_group', instance.blood_group)
        instance.caste = validated_data.get('caste', instance.caste)
        instance.religion = validated_data.get('religion', instance.religion)
        instance.mother_tongue = validated_data.get('mother_tongue', instance.mother_tongue)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.last_exam_passed = validated_data.get('last_exam_passed', instance.last_exam_passed)
        instance.board = validated_data.get('board', instance.board)
        instance.institute_name = validated_data.get('institute_name', instance.institute_name)
        instance.total_marks = validated_data.get('total_marks', instance.total_marks)
        instance.year_passing = validated_data.get('year_passing', instance.year_passing)
        instance.marks_secured = validated_data.get('marks_secured', instance.marks_secured)
        instance.cgpa_or_percentage = validated_data.get('cgpa_or_percentage', instance.cgpa_or_percentage)
        instance.status = validated_data.get('status', instance.status)

        


        instance.save()
        return instance



class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['batch']