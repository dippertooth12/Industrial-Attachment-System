from  rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Student,Industry,Skill

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['industry_id', 'name']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_id', 'name']
    
   