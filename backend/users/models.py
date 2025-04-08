from django.db import models
import random
import string
from django.db.models.signals import pre_save
from django.dispatch import receiver


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

    
def generate_random_logbook_id():
    # Generate a random string of 8 characters (can be changed to your preferred length)
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Logbook(models.Model):
    logbook_id = models.CharField(max_length=8, primary_key=True, default=generate_random_logbook_id, editable=False)
    student_id = models.ForeignKey('Student', to_field='student_id', on_delete=models.CASCADE)
    org_id = models.ForeignKey('Organisation', to_field='org_id', on_delete=models.CASCADE)  # Adjusted if needed
    week_number = models.IntegerField()
    log_entry = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Logbook entry for {self.student_id} Week {self.week_number}"


# Using the pre_save signal to assign the random logbook_id before saving
@receiver(pre_save, sender=Logbook)
def set_logbook_id(sender, instance, **kwargs):
    if not instance.logbook_id:  # If logbook_id is not provided, generate a new one
        instance.logbook_id = generate_random_logbook_id()

