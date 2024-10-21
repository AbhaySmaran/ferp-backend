from django.urls import path
from .views import DistinctBatchAPIView

urlpatterns = [
    path('sub-assign/', DistinctBatchAPIView.as_view(), name='distinct-batch'),
]