from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status  # Import status for better readability
from .models import Student
from .serializers import StudentSerializer
from django.contrib.auth.hashers import check_password
from .serializers import LogbookSerializer
from .serializers import OrganisationSerializer
from .models import Organisation
from .models import Location
from .models import Industry

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
    

@api_view(['POST'])
def register_organisation(request):
    try:
        data = request.data
        required_fields = ['org_name', 'industry_name', 'town', 'street', 'plot_number', 'contact_number', 'contact_email', 'password']
        
        for field in required_fields:
            if field not in data:
                return Response({"error": f"{field} is a required field"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Organisation email exists
        if Organisation.objects.filter(contact_email=data['contact_email']).exists():
            return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Organisation name exists
        if Organisation.objects.filter(org_name=data['org_name']).exists():
            return Response({"error": "Organisation already registered"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Organisation contact number exists
        if Organisation.objects.filter(contact_number=data['contact_number']).exists():
            return Response({"error": "Organisation contact already registered"}, status=status.HTTP_400_BAD_REQUEST)

        location = Location.objects.create(
            town=data['town'],
            street=data['street'],
            plot_no=data['plot_number']
        )


        # Check/Create the industry
        industry_name = data.get('industry_name')
        industry, _ = Industry.objects.get_or_create(industry_name=industry_name)

        # Prepare organization data
        org_data = {
            'org_name': data['org_name'],
            'industry': industry.pk,
            'town': data['town'],
            'street': data['street'],
            'plot_number': data['plot_number'],
            'contact_number': data['contact_number'],
            'contact_email': data['contact_email'],
            'password': data['password'],  # The password will be hashed automatically in the serializer
        }

        # Validate and save the organization data
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

        # Use check_password to compare the entered password with the stored hash
        if check_password(password, organisation.password):
            return Response({"message": "Organisation login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    except Organisation.DoesNotExist:
        return Response({"error": "Organisation not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_logbook_entry(request):
    try:
        data = request.data

        # Define the required fields
        required_fields = ['student_id', 'org_id', 'week_number', 'log_entry']
        for field in required_fields:
            if field not in data:
                return Response({"error": f"{field} is a required field."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Student exists by 'student_id' (not 'id')
        if not Student.objects.filter(student_id=data['student_id']).exists():
            return Response({"error": "Student ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Organisation exists by 'org_id' (not 'id')
        if not Organisation.objects.filter(org_id=data['org_id']).exists():  # Changed to 'org_id'
            return Response({"error": "Organisation ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and save the logbook entry
        serializer = LogbookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



