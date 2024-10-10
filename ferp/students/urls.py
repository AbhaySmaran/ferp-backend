from django.urls import path
from .views import *

urlpatterns = [
    path("register/", StudentRegisterView.as_view()),
    path('upload-csv/', upload_students_csv, name='upload-csv'),
    path('students/', StudentListView.as_view()),
    path('students/list/', StudentsView.as_view()),
    path('student/<int:id>/', StudentIndivisulaView.as_view()),
    path('attendance/<int:year>/<int:month>/<int:day>/', AttendanceView.as_view(), name='attendance-log'),
    path('student/update/<int:id>/', StudentUpdateView.as_view(), name='student-update'),
]