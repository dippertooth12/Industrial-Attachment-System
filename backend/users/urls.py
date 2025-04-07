from django.urls import path
from .views import register_student,login_student
from django.views.generic import TemplateView

urlpatterns = [
    path('register-student/', register_student, name='register_student'),
    path('login/', login_student, name='student_login'),#Add the login URL
    path('dashboard/', TemplateView.as_view(template_name="index.html")),
]


from .views import LogbookCreateView

urlpatterns = [
    path('logbook', LogbookCreateView.as_view(), name='logbook-create'),
]


from .views import create_logbook_entry

urlpatterns = [
    path('logbook', create_logbook_entry, name='create-logbook-entry'),
]
