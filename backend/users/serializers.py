from  rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Student,Industry,Skill,Organisation,OrganisationPreference,PreferredField,RequiredSkill,PreferredIndustry,StudentPreference,DesiredSkill

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
        fields = ['industry_id', 'industry_name']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_id', 'name']

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class OrganisationPreferenceSerializer(serializers.ModelSerializer):
    preferred_fields = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    required_skills = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    organisation_name = serializers.CharField(source='organisation.org_name', read_only=True)
    preferred_fields_names = serializers.SerializerMethodField(read_only=True)
    required_skills_names = serializers.SerializerMethodField(read_only=True)
    
    organisation = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(),
        pk_field=serializers.IntegerField()
    )

    class Meta:
        model = OrganisationPreference
        fields = [
            'pref_id',
            'organisation',
            'organisation_name',
            'pref_education_level',
            'positions_available',
            'start_date',
            'end_date',
            'preferred_fields',
            'required_skills',
            'preferred_fields_names',
            'required_skills_names',
        ]

    def create(self, validated_data):
        preferred_fields_data = validated_data.pop('preferred_fields', [])
        required_skills_data = validated_data.pop('required_skills', [])

        preference = OrganisationPreference.objects.create(**validated_data)

        for field_name in preferred_fields_data:
         PreferredField.objects.create(preference=preference, field_name=field_name)

        for skill_name in required_skills_data:
            RequiredSkill.objects.create(preference=preference, skill_name=skill_name)

        return preference

    def get_preferred_fields_names(self, obj):
        return [field.field_name for field in obj.preferred_fields.all()]

    def get_required_skills_names(self, obj):
        return [skill.skill_name for skill in obj.required_skills.all()]    

class StudentPreferenceSerializer(serializers.ModelSerializer):
    preferred_industries = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    desired_skills = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    industry_names = serializers.SerializerMethodField()
    skill_names = serializers.SerializerMethodField()

    class Meta:
        model = StudentPreference
        fields = [
            'student_pref_id',
            'student',
            'pref_location',
            'available_from',
            'available_to',
            'preferred_industries',
            'desired_skills',
            'industry_names',
            'skill_names',
        ]

    def create(self, validated_data):
        industries = validated_data.pop('preferred_industries', [])
        skills = validated_data.pop('desired_skills', [])

        preference = StudentPreference.objects.create(**validated_data)

        for industry_id in industries:
            try:
                industry = Industry.objects.get(pk=industry_id)
                PreferredIndustry.objects.create(student_pref=preference, industry=industry)
            except Industry.DoesNotExist:
                continue

        for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            DesiredSkill.objects.create(student_pref=preference, skill=skill)

        return preference

    def get_industry_names(self, obj):
        return [pi.industry.industry_name for pi in obj.preferredindustry_set.all()]

    def get_skill_names(self, obj):
        return [ds.skill.name for ds in obj.desiredskill_set.all()]
    
class PreferredFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferredField
        fields = '__all__'


class RequiredSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredSkill
        fields = '__all__'
   