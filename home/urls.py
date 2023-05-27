from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='home'),
    path('pacientes', views.patient_list, name="patients"),
    path('paciente/crear', views.create_patient, name='create_patient'),
    path('paciente/actualizar/<int:id>', views.update_patient, name="update_patient"),
    
    path('diagnostico/crear', views.create_diagnostic, name='create_diagnostic'),
    path('diagnostico/lista', views.get_diagnosis_list),
    path('test/crear', views.create_test, name="create_test"),
    path('paciente/lista', views.get_patient_list, name='get_patient_list'),
    path('example', views.example, name='example'),
    
    # Used to populate the Diagnostic table in the database
    # path('populate', views.populatate_database, name="populate_database"),
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]