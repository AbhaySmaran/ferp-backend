from .views import *
from django.urls  import path

urlpatterns = [
    path('create/',ExamCreationView.as_view()),
    path('view/',ExamView.as_view()),
    path('view/<int:id>/', ExamView.as_view()),
]