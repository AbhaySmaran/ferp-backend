from django.shortcuts import render
from students.models import Student
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
# Create your views here.
class DistinctBatchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Get distinct batch values
        distinct_batches = Student.objects.values_list('batch', flat=True).distinct()
        return Response(distinct_batches)
    

# class SubjectAssignmentView():
#     def get(self, request, *args, **kwargs):
#         # Get distinct batch values
#         distinct_batches = Student.objects.values_list('batch', flat=True).distinct()

        
#         return Response(distinct_batches)