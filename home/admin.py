from django.contrib import admin
from .models import (Categoria, Paciente, Test, PacienteTest, Evolucion)

class PatientAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos demográficos', {'fields': (
            'cedula', 
            'nombre', 
            'apellidos', 
            'fecha_nacimiento', 
            'telefono', 
            'email', 
            'ocupacion', 
            'profesion', 
            'seguridad_social'
        )}),
        ('Datos del acompañante', {'fields': (
            'acompanante', 
            'parentesco', 
            'telefono_acompanante'
        )}), 
        ('Hábitos del paciente', {'fields': (
            'actividad_fisica', 
            'frecuencia_actividad_fisica', 
            'tipo_actividad_fisica'
        )}),
        ('Historia clínica', {'fields': (
            'diagnostico_medico', 
            'motivo_consulta', 
            'cronologia_de_patologia', 
            'conclusion'
        )})
    )

admin.site.register(Paciente, PatientAdmin)

admin.site.register([Categoria, Test, PacienteTest, Evolucion])