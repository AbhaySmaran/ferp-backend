from django.shortcuts import render
from students.models import Student
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from django.http import Http404

class SubjectAPIView(APIView):

    
    def get_object(self, pk):
        try:
            return Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            raise Http404

    
    def get(self, request, pk=None):
        if pk:
            subject = self.get_object(pk)
            serializer = SubjectSerializer(subject)
            return Response(serializer.data)
        else:
            subjects = Subject.objects.all()
            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data)

    
    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, pk):
        subject = self.get_object(pk)
        # partial = request.method == 'PATCH'
        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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