from django.contrib import admin
from .models import (Category, Patient, Test, PatientTest, 
                     Evolution, Diagnosis, PatientDiagnosis, AttachedFile
)

class EvolutionInline(admin.TabularInline):
    model = Evolution
    extra = 0
    
class PatientTestInline(admin.TabularInline):
    model = PatientTest
    extra = 0

class PatientDiagnosisInline(admin.TabularInline):
    model = PatientDiagnosis
    extra = 0
  
class AttachedFileInline(admin.TabularInline):
    model = AttachedFile
    extra = 0
   
class PatientAdmin(admin.ModelAdmin):
    inlines = [PatientDiagnosisInline, PatientTestInline, EvolutionInline, AttachedFileInline]
    fieldsets = (
        ('Datos demográficos', {
            'fields': (
                'cedula', 
                'nombre', 
                'apellidos', 
                'fecha_nacimiento', 
                'telefono', 
                'email', 
                'ocupacion', 
                'profesion', 
                'seguridad_social'
            ),
            'classes': ['collapse']
        }),
        ('Datos del acompañante', {'fields': (
            'acompanante', 
            'parentesco', 
            'telefono_acompanante'
        ),
            'classes': ['collapse']
        }), 
        ('Hábitos del paciente', {'fields': (
            'actividad_fisica', 
            'frecuencia_actividad_fisica', 
            'tipo_actividad_fisica'
        ),
            'classes': ['collapse']
        }),
        ('Historia clínica', {'fields': ( 
            'motivo_consulta', 
            'cronologia_de_patologia', 
            'conclusion',
        ),
            'classes': ['collapse']
        })
    )

admin.site.register(Patient, PatientAdmin)
admin.site.register([Category, Test, PatientTest, Evolution, Diagnosis, PatientDiagnosis, AttachedFile])