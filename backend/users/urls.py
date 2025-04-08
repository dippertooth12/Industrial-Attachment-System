from django.urls import path
from .views import register_student,login_student,register_organisation,login_organisation
from django.views.generic import TemplateView
from .views import create_logbook_entry


urlpatterns = [
    path('register-student/', register_student, name='register_student'),
    path('login/', login_student, name='student_login'),#Add the login URL
    path('dashboard/', TemplateView.as_view(template_name="index.html")),
    path('register-organisation/', register_organisation, name='register_organisation'),
    path('login-organisation/', login_organisation, name='login_organisation'),
    path('', create_logbook_entry, name='create-logbook-entry'),
]


