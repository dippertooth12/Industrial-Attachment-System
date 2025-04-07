from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import Student
from .serializers import StudentSerializer,IndustrySerializer,SkillSerializer
from .models import Student, StudentPreference,Skill,DesiredSkill,PreferredIndustry,Industry,generate_preference_id
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
    
def preference_list(request):
    prefs = StudentPreference.objects.select_related('student').all()
    data = []
    for pref in prefs:
        data.append({
            "id": pref.student_pref_id,
            "student": pref.student.name,
            "pref_location": pref.pref_location,
            "available_from": pref.available_from,
            "available_to": pref.available_to,
        })
    return JsonResponse(data, safe=False)
@api_view(['POST'])
def create_student_preference(request):
    try:
        data = request.data
        student = Student.objects.get(student_id=data['student_id'])

        # Generate ID
        new_id = generate_preference_id(student.student_id)

        pref = StudentPreference.objects.create(
            student_pref_id=new_id,
            student=student,
            pref_location=data['pref_location'],
            available_from=data['available_from'],
            available_to=data['available_to']
        )

        for industry_id in data.get('industries', []):
            industry = Industry.objects.get(industry_id=industry_id)
            PreferredIndustry.objects.create(student_pref=pref, industry=industry)

        for skill_id in data.get('skills', []):
            skill = Skill.objects.get(skill_id=skill_id)
            DesiredSkill.objects.create(student_pref=pref, skill=skill)

        return JsonResponse({'message': 'Preferences saved successfully', 'id': pref.student_pref_id}, status=201)

    except Exception as e:
        return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)
@api_view(['GET'])
def get_industries(request):
    industries = Industry.objects.all()
    serializer = IndustrySerializer(industries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_skills(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


    

