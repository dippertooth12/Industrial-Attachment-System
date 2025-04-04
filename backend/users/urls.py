from django.urls import path
from .views import (
    register_student,
    login_student,
    register_organization,
    login_organization,
    match_organizations_for_student
)
from django.views.generic import TemplateView

urlpatterns = [
    path('register/student/', register_student),
    path('login/student/', login_student),
    path('register/organization/', register_organization),
    path('login/organization/', login_organization),
     path('api/match/<str:student_id>/', match_organizations_for_student),
     path('dashboard/', TemplateView.as_view(template_name="index.html")),
]
    
