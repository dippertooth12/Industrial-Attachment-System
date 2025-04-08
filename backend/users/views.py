from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import Student
import traceback
from .serializers import StudentSerializer,IndustrySerializer,SkillSerializer,OrganisationSerializer,OrganisationPreferenceSerializer,RequiredSkillSerializer,PreferredFieldSerializer
from .models import Student, StudentPreference,Skill,DesiredSkill,PreferredIndustry,Industry,generate_preference_id,Organisation,Location,OrganisationPreference
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def register_student(request):
    try:
        data = request.data

        # Check if student_id or phone number already exists
        if Student.objects.filter(student_id=data['student_id']).exists():
            return Response({"error": "Student ID already registered"}, status=400)

        if Student.objects.filter(student_contact_number=data['student_contact_number']).exists():
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
    
@api_view(['GET'])    
def preference_list(request):
    prefs = StudentPreference.objects.select_related('student').all()
    data = []
    for pref in prefs:
        data.append({
            "id": pref.student_pref_id,
            "student": pref.student.last_name,
            "pref_location": pref.pref_location,
            "available_from": pref.available_from,
            "available_to": pref.available_to,
        })
    return JsonResponse(data, safe=False)

@api_view(['POST'])
def create_student_preference(request):
    try:
        data = request.data
        print("📦 Received data:", data)

        student = Student.objects.get(student_id=data['student_id'])
        new_id = generate_preference_id(student.student_id)

        pref = StudentPreference.objects.create(
            student_pref_id=new_id,
            student=student,
            pref_location=data['pref_location'],
            available_from=data['available_from'],
            available_to=data['available_to']
        )

        for industry_id in data.get('industries', []):
            print(f"🔍 Looking for industry: {industry_id}")
            industry = Industry.objects.get(industry_id=industry_id)
            PreferredIndustry.objects.create(student=pref, industry=industry)

        for skill_id in data.get('skills', []):
            print(f"🔍 Looking for skill: {skill_id}")
            skill = Skill.objects.get(skill_id=skill_id)
            DesiredSkill.objects.create(student_pref=pref, skill=skill)

        return JsonResponse({'message': 'Preferences saved successfully', 'id': pref.student_pref_id}, status=201)

    except Exception as e:
        traceback.print_exc()  # 🔍 Print full error in terminal
        return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)
    
def get_industries(request):
    data = list(Industry.objects.values("industry_id", "industry_name"))
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def get_skills(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register_organisation(request):
    try:
        data = request.data
        required_fields = ['org_name', 'industry', 'town', 'street', 'plot_number', 'contact_number', 'contact_email', 'password']

        for field in required_fields:
            if field not in data or data[field] == '':
                return Response({"error": f"{field} is a required field"}, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicates
        if Organisation.objects.filter(contact_email=data['contact_email']).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        if Organisation.objects.filter(org_name=data['org_name']).exists():
            return Response({"error": "Organisation already registered"}, status=status.HTTP_400_BAD_REQUEST)

        if Organisation.objects.filter(contact_number=data['contact_number']).exists():
            return Response({"error": "Organisation contact already registered"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the industry_id
        try:
            industry = Industry.objects.get(industry_id=data['industry'])
        except Industry.DoesNotExist:
            return Response({"error": "Invalid industry selected"}, status=status.HTTP_400_BAD_REQUEST)

        # Create location
        Location.objects.create(
            town=data['town'],
            street=data['street'],
            plot_no=data['plot_number']
        )

        # Prepare and save organisation
        org_data = {
            'org_name': data['org_name'],
            'industry': industry.pk,
            'town': data['town'],
            'street': data['street'],
            'plot_number': data['plot_number'],
            'contact_number': data['contact_number'],
            'contact_email': data['contact_email'],
            'password': data['password'],  # will be hashed in serializer
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
                "organisation_id": organisation.org_id  # ✅ This line is needed!
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    except Organisation.DoesNotExist:
        return Response({"error": "Organisation not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_organisation_preference(request, org_id):
    if org_id is None:
        return Response({"error": "Organisation ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        try:
            # Change this line to use org_id instead of id
            organisation = Organisation.objects.get(org_id=org_id)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['organisation'] = organisation.org_id  # Use org_id here

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



    

