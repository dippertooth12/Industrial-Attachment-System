from django.urls import path
from .views import register_student,login_student, register_organisation, login_organisation
from django.views.generic import TemplateView

urlpatterns = [
    #Student
    path('register-student/', register_student, name='register_student'),
    path('login/', login_student, name='student_login'),#Add the login URL

    #Organisation
    path('register-organisation/', register_organisation, name='register_organisation'),
    path('login-organisation/', login_organisation, name='login_organisation'),

    #dashboard
    path('dashboard/', TemplateView.as_view(template_name="index.html")),
]