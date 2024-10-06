from django.urls import path
from .views import *

urlpatterns = [
    path("register/", StudentRegisterView.as_view()),
    path('upload-csv/', upload_students_csv, name='upload-csv'),
    path('students/', StudentListView.as_view())
]