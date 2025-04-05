from django.urls import path
from .views import (
    register_student,
    login_student,
)
from django.views.generic import TemplateView

urlpatterns = [
    path('register/student/', register_student),
    path('login/student/', login_student),
     #path('api/student-preference/', create_student_preference),
     path('dashboard/', TemplateView.as_view(template_name="index.html")),
]
    
