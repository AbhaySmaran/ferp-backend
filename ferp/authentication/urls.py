from django.urls import path
from .views import *
urlpatterns = [
    path("user/login/", UserLoginView.as_view()),
    path("user/profile/", UserProfileView.as_view()),
]