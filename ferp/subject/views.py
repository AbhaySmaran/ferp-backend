from django.shortcuts import render
from students.models import Student
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

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


# class DistinctBatchAPIView(APIView):
#     def get(self, request, *args, **kwargs):
       
#         distinct_batches = Student.objects.values_list('batch', flat=True).distinct()

#         for batch in distinct_batches:
            
#             if not SubjectAssignment.objects.filter(batch=batch).exists():
#                 SubjectAssignment.objects.create(batch=batch)

#         return Response({'status': 'success', 'message': 'Distinct batch data added to SubjectAssignment table'})


class DistinctBatchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        distinct_batches = Student.objects.values_list('batch', flat=True).distinct()

        

        for batch in distinct_batches:
            if not SubjectAssignment.objects.filter(batch=batch).exists():               
                SubjectAssignment.objects.create(batch=batch)
                

        assignments = SubjectAssignment.objects.all()
        serializer = SubjectAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)