from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=20,unique=True,primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    year_of_study = models.IntegerField()
    student_email = models.EmailField(unique=True)#Email with uniqueness
    student_contact_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    
class StudentPreference(models.Model):
    student= models.ForeignKey(Student, on_delete=models.CASCADE)
    availabefrom=models.DateField()
    availabeto=models.DateField()

class StudentPreferenceField(models.Model):
    student_preference = models.ForeignKey(StudentPreference, on_delete=models.CASCADE)
    organisation_name=models.CharField(max_length=100)
    field=models.CharField(max_length=100)



class Organization(models.Model):
    Org_id= models.CharField(max_length=100,unique=True,primary_key=True)
    org_name = models.CharField(max_length=100)
    contact_email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    password = models.CharField(max_length=255)

class OrganizationPreference(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    positions_available=models.CharField(max_length=100)
    prefered_education_level=models.CharField(max_length=100)
    startDate=models.DateField()
    endDate=models.DateField()

class OrgpreferenceField(models.Model):
    preference = models.ForeignKey(OrganizationPreference, on_delete=models.CASCADE)
    prefereed_field=models.CharField(max_length=100)

