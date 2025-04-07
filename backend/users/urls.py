from django.urls import path
from .views import (
    register_student,
    login_student,
    register_organisation,
    login_organisation,
    create_organisation_preference,
    list_organisation_preferences,
    add_preferred_field,
    add_required_skill,
    get_organisation_by_email
)
from django.views.generic import TemplateView

urlpatterns = [

    # === Student Routes ===
    path('register-student/', register_student, name='register_student'),
    path('login-student/', login_student, name='login_student'),

    # === Organisation Routes ===
    path('register-organisation/', register_organisation, name='register_organisation'),
    path('login-organisation/', login_organisation, name='login_organisation'),
    path('organisation/by-email/<str:email>/', get_organisation_by_email, name='get_organisation_by_email'),

    # === Organisation Preferences ===
    path('organisation/<int:org_id>/preferences/', list_organisation_preferences, name='list_organisation_preferences'),
    path('organisation/<int:org_id>/preferences/create/', create_organisation_preference, name='create_organisation_preference'),

    # === Add Fields/Skills ===
    path('organisation/preferences/preferred-field/', add_preferred_field, name='add_preferred_field'),
    path('organisation/preferences/required-skill/', add_required_skill, name='add_required_skill'),

    # === Dashboard (Frontend SPA entry point) ===
    path('dashboard/', TemplateView.as_view(template_name="index.html")),
]
