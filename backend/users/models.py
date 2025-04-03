from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=20,unique=True,primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    year_of_study = models.IntegerField()
    student_email = models.EmailField(unique=True)#Email with uniqueness
    student_contact_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    
class Organisation(models.Model):
    orgnaisation_id = models.CharField(max_length=20,unique=True, primary_key=True)

