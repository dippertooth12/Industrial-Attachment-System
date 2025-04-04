from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Student, Organization
from .serializers import StudentSerializer, OrganizationRegistrationSerializer
from .models import Student,Organization, StudentPreferenceField, OrgpreferenceField

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

@api_view(['POST'])
def register_organization(request):
    serializer = OrganizationRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Organization registered successfully"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_organization(request):
    email = request.data.get("contact_email")
    password = request.data.get("password")
    try:
        organization = Organization.objects.get(contact_email=email)
        if check_password(password, organization.password):
            return Response({"message": "Organization login successful"}, status=200)
        else:
            return Response({"error": "Invalid credentials"}, status=400)
    except Organization.DoesNotExist:
        return Response({"error": "Organization not found"}, status=404)
    
@api_view(['GET'])
def match_organizations_for_student(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        student_fields = StudentPreferenceField.objects.filter(preference__student=student)

        matches = []

        for pref_field in student_fields:
            org_fields = OrgpreferenceField.objects.filter(preferred_field=pref_field.field)

            for org_field in org_fields:
                org_pref = org_field.preference

                # Time overlap check
                if (pref_field.preference.available_from <= org_pref.end_date and
                    pref_field.preference.available_to >= org_pref.start_date):

                    matches.append({
                        "organization": org_pref.organization.org_name,
                        "field": org_field.preferred_field,
                        "start": org_pref.start_date,
                        "end": org_pref.end_date,
                        "positions": org_pref.positions_available,
                    })

        return Response({"matches": matches})
    
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)
