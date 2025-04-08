from django.urls import path
from .views import (
    register_student,
    login_student,
    create_student_preference,
    get_industries,
    get_skills,
    register_organisation,
    login_organisation,
    add_preferred_field,
    add_required_skill,
    list_organisation_preferences,
    create_organisation_preference,
    create_logbook_entry,
    get_org_id_by_name,
)
from django.views.generic import TemplateView

urlpatterns = [
    # Student Routes
    path('register/student/', register_student, name='register_student'),
    path('login/student/', login_student, name='login_student'),
    path('student-preference/', create_student_preference, name='create_student_preference'),

    # Organisation Routes
    path('register-organisation/', register_organisation, name='register_organisation'),
    path('login-organisation/', login_organisation, name='login_organisation'),
    path('organisation/<int:org_id>/preferences/', list_organisation_preferences, name='list_organisation_preferences'),
    path('organisation/<int:org_id>/preferences/create/', create_organisation_preference, name='create_organisation_preference'),
    path('organisation/preferences/preferred-field/', add_preferred_field, name='add_preferred_field'),
    path('organisation/preferences/required-skill/', add_required_skill, name='add_required_skill'),

    # Master Data Routes
    path('industries/', get_industries, name='get_industries'),
    path('skills/', get_skills, name='get_skills'),

    # Optional frontend entry point
    path('dashboard/', TemplateView.as_view(template_name="index.html"), name='dashboard'),
    path('logbook/', create_logbook_entry, name='logbook'),
    path('get-org-id-by-name/', get_org_id_by_name, name='get_org_id_by_name'),
]
    
