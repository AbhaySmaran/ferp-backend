from django.urls import path
from .views import *

urlpatterns=[
    # path('user/login/',UserLoginView.as_view()),
    path('users/',UserListView.as_view()),
    path('users/<int:id>/', UserUpdateView.as_view()),
    path('user/<int:id>/', UserView.as_view()),
    path('user/register/',UserRegisterView.as_view()),
    # path('user/profile/',UserProfileView.as_view()),
    path('roles/',RoleListView.as_view()),
    path('categories/',StaffCategoryListView.as_view()),
    path('dept/',DepartmentListView.as_view()),
    path('upload_csv/', CSVUploadAPIView.as_view(), name='upload_csv'),
    path('uplodCSV/', BulkUserUploadView.as_view()),
]