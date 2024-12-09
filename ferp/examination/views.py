from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404

class ExamCreationView(APIView):
    def post(self,request):
        data = request.data.copy()
        data['exam_created_by'] = request.user.id
        print(request.data.id)
        serializer = ExamSerializer(data = data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"Exam Created"})
        return Response(serializer.errors)
    
class ExamView(APIView):
    def get(self,request, id=None):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        if id is not None:
            exam = get_object_or_404(Exam,id=id)
            serializer = ExamSerializer(exam)
            return Response(serializer.data)
        return Response(serializer.data)
