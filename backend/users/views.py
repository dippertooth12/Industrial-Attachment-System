from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import (
    Student, Organisation, Industry, Location,
    OrganisationPreference, PreferredField, RequiredSkill
)
from .serializers import (
    StudentSerializer, OrganisationSerializer,
    OrganisationPreferenceSerializer, PreferredFieldSerializer,
    RequiredSkillSerializer
)
from django.contrib.auth.hashers import check_password

# Student Registration
@api_view(['POST'])
def register_student(request):
    try:
        data = request.data
        required_fields = ['student_id', 'first_name', 'last_name', 'year_of_study', 'student_email', 'student_contact_number', 'password']
        for field in required_fields:
            if field not in data:
                return Response({"error": f"{field} is a required field."}, status=status.HTTP_400_BAD_REQUEST)

        if Student.objects.filter(student_email=data['student_email']).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        if Student.objects.filter(student_id=data['student_id']).exists():
            return Response({"error": "Student ID already registered"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student registered successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Student Login
@api_view(['POST'])
def login_student(request):
    student_id = request.data.get("student_id")
    password = request.data.get("password")
    try:
        student = Student.objects.get(student_id=student_id)
        if check_password(password, student.password):
            return Response({"message": "Student login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)


# Organisation Registration
@api_view(['POST'])
def register_organisation(request):
    try:
        data = request.data
        required_fields = ['org_name', 'industry_name', 'town', 'street', 'plot_number', 'contact_number', 'contact_email', 'password']
        for field in required_fields:
            if field not in data:
                return Response({"error": f"{field} is a required field"}, status=status.HTTP_400_BAD_REQUEST)

        if Organisation.objects.filter(contact_email=data['contact_email']).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        if Organisation.objects.filter(org_name=data['org_name']).exists():
            return Response({"error": "Organisation already registered"}, status=status.HTTP_400_BAD_REQUEST)

        if Organisation.objects.filter(contact_number=data['contact_number']).exists():
            return Response({"error": "Organisation contact already registered"}, status=status.HTTP_400_BAD_REQUEST)

        Location.objects.create(
            town=data['town'],
            street=data['street'],
            plot_no=data['plot_number']
        )

        industry, _ = Industry.objects.get_or_create(industry_name=data['industry_name'])

        org_data = {
            'org_name': data['org_name'],
            'industry': industry.pk,
            'town': data['town'],
            'street': data['street'],
            'plot_number': data['plot_number'],
            'contact_number': data['contact_number'],
            'contact_email': data['contact_email'],
            'password': data['password'],
        }

        serializer = OrganisationSerializer(data=org_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Organisation registered successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Organisation Login
@api_view(['POST'])
def login_organisation(request):
    contact_email = request.data.get("contact_email")
    password = request.data.get("password")
    try:
        organisation = Organisation.objects.get(contact_email=contact_email)
        if check_password(password, organisation.password):
            return Response({
                "message": "Organisation login successful",
                "organisation_id": organisation.org_id
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    except Organisation.DoesNotExist:
        return Response({"error": "Organisation not found"}, status=status.HTTP_404_NOT_FOUND)


# Create Organisation Preference
@api_view(['POST'])
def create_organisation_preference(request, org_id):
    if org_id is None:
        return Response({"error": "Organisation ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        try:
            organisation = Organisation.objects.get(id=org_id)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['organisation'] = organisation.id

        serializer = OrganisationPreferenceSerializer(data=data)
        if serializer.is_valid():
            preference = serializer.save()
            return Response({
                "message": "Preference created successfully",
                "id": preference.pref_id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": f"Server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# List Preferences for Specific Organisation
@api_view(['GET'])
def list_organisation_preferences(request, org_id):
    try:
        preferences = OrganisationPreference.objects.filter(organisation_id=org_id)
        serializer = OrganisationPreferenceSerializer(preferences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Add Preferred Field
@api_view(['POST'])
def add_preferred_field(request):
    try:
        serializer = PreferredFieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Preferred field added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Add Required Skill
@api_view(['POST'])
def add_required_skill(request):
    try:
        serializer = RequiredSkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Required skill added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Get Organisation by Email
@api_view(['GET'])
def get_organisation_by_email(request, email):
    try:
        organisation = Organisation.objects.get(contact_email=email)
        serializer = OrganisationSerializer(organisation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Organisation.DoesNotExist:
        return Response({"error": "Organisation not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
