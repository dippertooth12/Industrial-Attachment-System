from  rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Student
from .models import Organisation
from .models import Logbook

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LogbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logbook
        fields = ['student_id', 'org_id', 'week_number', 'log_entry', 'submitted_at']
        # Note: logbook_id is not included as it's automatically generated


