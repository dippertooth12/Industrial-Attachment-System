from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Student
from .serializers import StudentSerializer
from .models import Student, StudentPreference
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def register_student(request):
    try:
        data = request.data

        # Check if student_id or phone number already exists
        if Student.objects.filter(student_id=data['student_id']).exists():
            return Response({"error": "Student ID already registered"}, status=400)

        if Student.objects.filter(phonenumber=data['phonenumber']).exists():
            return Response({"error": "Phone number already registered"}, status=400)

        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student registered successfully"}, status=201)

        return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
def login_student(request):
    student_id = request.data.get("student_id")
    password = request.data.get("password")
    try:
        student = Student.objects.get(student_id=student_id)
        if check_password(password, student.password):
            return Response({"message": "Student login successful"}, status=200)
        else:
            return Response({"error": "Invalid credentials"}, status=400)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)


    

