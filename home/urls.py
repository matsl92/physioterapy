from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='home'),
    path('paciente/lista', views.patient_list, name="patient_list"),
    path('paciente/crear', views.create_patient, name='create_patient'),
    path('paciente/actualizar/<int:id>', views.update_patient, name="update_patient"),
    
    path('diagnostico/crear', views.create_diagnostic, name='create_diagnostic'),
    
    path('example', views.example, name='example'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]