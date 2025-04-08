from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=20,unique=True,primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    year_of_study = models.IntegerField()
    student_email = models.EmailField(unique=True)#Email with uniqueness
    student_contact_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)

class Industry(models.Model):
    industry_id = models.AutoField(primary_key=True)
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



class PreferredField(models.Model):
    field_id = models.AutoField(primary_key=True)
    preference = models.ForeignKey(OrganisationPreference, on_delete=models.CASCADE, related_name='preferred_fields')
    field_name = models.CharField(max_length=100)


class RequiredSkill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    preference = models.ForeignKey(OrganisationPreference, on_delete=models.CASCADE, related_name='required_skills')
    skill_name = models.CharField(max_length=100)