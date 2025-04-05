from django.urls import path
from .views import register_student, login_student, create_student_preference,get_industries,get_skills
from django.views.generic import TemplateView

urlpatterns = [
    path('register/student/', register_student),
    path('login/student/', login_student),
    path('student-preference/', create_student_preference),
     path('dashboard/', TemplateView.as_view(template_name="index.html")),
     path('industries/', get_industries),
    path('skills/', get_skills),
]
    
