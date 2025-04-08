from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Student, Organisation, OrganisationPreference, PreferredField, RequiredSkill

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

        # Get the organization instance
        organisation = validated_data['organisation']
        
        # Create the preference with the organization's org_id
        preference = OrganisationPreference.objects.create(
            organisation_id=organisation.org_id,
            **validated_data
        )

        for field_id in preferred_fields_data:
            try:
                field = PreferredField.objects.get(id=field_id)
                preference.preferred_fields.add(field)
            except PreferredField.DoesNotExist:
                continue

        for skill_id in required_skills_data:
            try:
                skill = RequiredSkill.objects.get(id=skill_id)
                preference.required_skills.add(skill)
            except RequiredSkill.DoesNotExist:
                continue

        return preference

    def get_preferred_fields_names(self, obj):
        return [field.field_name for field in obj.preferred_fields.all()]

    def get_required_skills_names(self, obj):
        return [skill.skill_name for skill in obj.required_skills.all()]    
    
class PreferredFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferredField
        fields = '__all__'


class RequiredSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredSkill
        fields = '__all__'