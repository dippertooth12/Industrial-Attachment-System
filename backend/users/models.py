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
    student_pref_id = models.CharField(primary_key=True, max_length=20)
    student= models.ForeignKey(Student, on_delete=models.CASCADE)
    pref_location = models.CharField(max_length=100)
    available_from = models.DateField()
    available_to = models.DateField()

class Industry(models.Model):
    industry_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)   

class PreferredIndustry(models.Model):
    student_pref = models.ForeignKey(StudentPreference, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student_pref', 'industry')
        
class Skill(models.Model):
    skill_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)

class DesiredSkill(models.Model):
    student_pref = models.ForeignKey(StudentPreference, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student_pref', 'skill')
