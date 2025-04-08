from django.db import models

def generate_preference_id(student_id):
    from .models import StudentPreference
    existing = StudentPreference.objects.filter(student__student_id=student_id).count() + 1
    return f"{student_id}_PREF{existing:03d}"

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    year_of_study = models.IntegerField()
    student_email = models.EmailField(unique=True)
    student_contact_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)

class StudentPreference(models.Model):
    student_pref_id = models.CharField(primary_key=True, max_length=30)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pref_location = models.CharField(max_length=100)
    available_from = models.DateField()
    available_to = models.DateField()

    def save(self, *args, **kwargs):
        if not self.student_pref_id:
            self.student_pref_id = generate_preference_id(self.student.student_id)
        super().save(*args, **kwargs)

class Industry(models.Model):
    industry_id = models.CharField(primary_key=True, max_length=20)
    industry_name = models.CharField(max_length=100)
    
class Organisation(models.Model):
    org_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=255)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    plot_number = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    contact_email = models.EmailField()
    password = models.CharField(max_length=255)

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    plot_no = models.CharField(max_length=50)

    class Meta:
        unique_together = ('street', 'plot_no')


class OrganisationPreference(models.Model):
    pref_id = models.AutoField(primary_key=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='preferences')
    pref_education_level = models.CharField(max_length=100)
    positions_available = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

class Skill(models.Model):
    skill_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)

class PreferredField(models.Model):
    field_id = models.AutoField(primary_key=True)
    preference = models.ForeignKey(OrganisationPreference, on_delete=models.CASCADE, related_name='preferred_fields')
    field_name = models.CharField(max_length=100)


class RequiredSkill(models.Model):
    id = models.AutoField(primary_key=True)  # new unique primary key
    preference = models.ForeignKey(OrganisationPreference, on_delete=models.CASCADE, related_name='required_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('preference', 'skill')

#class Industry(models.Model):
    #industry_id = models.CharField(primary_key=True, max_length=20)
    #name = models.CharField(max_length=100)

class PreferredIndustry(models.Model):
    student = models.ForeignKey(StudentPreference, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'industry')

class DesiredSkill(models.Model):
    student_pref = models.ForeignKey(StudentPreference, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student_pref', 'skill')