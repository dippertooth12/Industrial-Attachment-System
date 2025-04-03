from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status  # Import status for better readability
from .models import Student
from .serializers import StudentSerializer
from django.contrib.auth.hashers import check_password


@api_view(['POST'])
def register_student(request):
    try:
        data = request.data

        # Validate required fields exist
        required_fields = ['student_id', 'first_name', 'last_name', 'year_of_study', 'student_email', 'student_contact_number', 'password']
        for field in required_fields:
            if field not in data:
                return Response({"error": f"{field} is a required field."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if student email already exists
        if Student.objects.filter(student_email=data['student_email']).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if student ID already exists
        if Student.objects.filter(student_id=data['student_id']).exists():
            return Response({"error": "Student ID already registered"}, status=status.HTTP_400_BAD_REQUEST)

        # Do NOT hash the password here — let the serializer or model handle it!

        # Create and validate the serializer
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student registered successfully!"}, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])  # Added missing decorator
def login_student(request):
    student_id = request.data.get("student_id")
    password = request.data.get("password")

    try:
        student = Student.objects.get(student_id=student_id)

        # Use check_password to compare the entered password with the stored hash
        if check_password(password, student.password):
            return Response({"message": "Student login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
