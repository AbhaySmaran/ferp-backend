from django.urls import path
from .views import *

urlpatterns = [
    path("register/", StudentRegisterView.as_view()),
]