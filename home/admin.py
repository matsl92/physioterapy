from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (Categoria, Paciente, Test, PacienteTest, 
                     Evolucion, Diagnostico, Membership, Person, Group,
                     Image, Product
)

class PatientAdmin(admin.ModelAdmin):
    
    fieldsets2 = (
        (
            'Datos demográficos', {
                'fields': [
                    'cedula', 
                    'nombre', 
                    'apellidos', 
                    'fecha_nacimiento', 
                    'telefono', 
                    'email', 
                    'ocupacion', 
                    'profesion', 
                    'seguridad_social'
                    ],
                'classes': [
                    'collapse'
                ]
            } 
        ),
        (
            'Datos del acompañante', {
                'fields': [
                    'acompanante', 
                    'parentesco', 
                    'telefono_acompanante'
                    ],
                'classes': [
                    'collapse',
                    'wide'
                ]
            } 
        ),
        (
            'Hábitos del paciente', {
                'fields': [
                    'actividad_fisica', 
                    'frecuencia_actividad_fisica', 
                    'tipo_actividad_fisica'
                ]
            } 
        ),
        (
            'Historia clínica', {
                'fields': [
                    'diagnostico', 
                    'motivo_consulta', 
                    'cronologia_de_patologia', 
                    'conclusion',
                    'adjuntar_documento'
                ]
            }
        )
    )
    
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
            )
        }
        ),
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
            'diagnostico', 
            'motivo_consulta', 
            'cronologia_de_patologia', 
            'conclusion',
            'adjuntar_documento'
        )})
    )

# admin.site.register(Paciente, PatientAdmin)

admin.site.register([Categoria, Test, PacienteTest, Evolucion, Diagnostico])

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1
    
class PersonAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]


class GroupAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]
    
admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)

class ImageInline(GenericTabularInline):
    model = Image
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    
admin.site.register(Product, ProductAdmin)


class EvolutionInline(admin.TabularInline):
    model = Evolucion
    extra = 1
    
class PatientAdmin(admin.ModelAdmin):
    inlines = [EvolutionInline]
    
admin.site.register(Paciente, PatientAdmin)