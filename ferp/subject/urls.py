from django.urls import path
from .views import *

urlpatterns = [
    path('sub-assign/', DistinctBatchAPIView.as_view(), name='distinct-batch'),
    path('subjects/', SubjectAPIView.as_view(), name='subject-list-create'),  
    path('subjects/<int:pk>/', SubjectAPIView.as_view(), name='subject-detail'), 
]