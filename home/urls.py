from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.patient_list, name="patients"),
    path('paciente/crear', views.create_patient, name='create_patient'),
    path('paciente/actualizar/<int:id>', views.update_patient, name="update_patient"),
    path('paciente/eliminar/<int:id>', views.delete_patient, name="delete_patient"),
    
    path('diagnosiso/crear', views.create_diagnosis, name='create_diagnosis'),
    path('diagnosiso/lista', views.get_diagnosis_list),
    path('test/crear', views.create_test, name="create_test"),
    path('paciente/lista', views.get_patient_list, name='get_patient_list'),
    
    # Used to populate the Diagnosis table in the database
    # path('populate', views.populatate_database, name="populate_database"),
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]