from django import forms
from .models import (
    Paciente,
    Diagnostico,
    Evolucion,
    Test,
    PacienteTest,
    Categoria,
    FRECUENCIA_ACTIVIDAD_FISICA_OPCIONES,
    OCUPACION_OPCIONES,
    TEST_RESPONSE_TYPE
)

def get_diagnosis_options():
    return Diagnostico.objects.filter(is_active = True)

def get_category_options():
    return Categoria.objects.all()

def get_test_options():
    return Test.objects.all()

class PatientForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'django-patient-form'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'django-patient-form'
            }),
            'acompanante': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'parentesco': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'telefono_acompanante': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'ocupacion': forms.Select(
                choices=OCUPACION_OPCIONES,
                attrs={
                'class': 'django-patient-form'
            }),
            'profesion': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'seguridad_social': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'diagnostico': forms.Select(
                choices=[get_diagnosis_options()],
                attrs={
                'class': 'django-patient-form'
            }),
            'motivo_consulta': forms.Textarea(attrs={
                'rows': "3",
                'class': 'django-patient-form'
            }),
            'cronologia_de_patologia': forms.Textarea(attrs={
                'rows': "3",
                'class': 'django-patient-form'
            }),
            'actividad_fisica': forms.CheckboxInput(attrs={
                'class': 'django-patient-form'
            }),
            'tipo_actividad_fisica': forms.TextInput(attrs={
                'class': 'django-patient-form'
            }),
            'frecuencia_actividad_fisica': forms.Select(
                choices=FRECUENCIA_ACTIVIDAD_FISICA_OPCIONES,
                attrs={
                'class': 'django-patient-form'
            }),
            'conclusion': forms.Textarea(attrs={
                'rows': "3",
                'class': 'django-patient-form'    
            }),
            'adjuntar_documento': forms.FileInput(attrs={
                'class': 'django-patient-form',
            })
            
        }

class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(
                attrs={
                    'class': 'django-diagnostic-form'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'django-diagnostic-form'
                }
            )
        }
        
class EvolutionForm(forms.ModelForm):
    class Meta: 
        model = Evolucion
        fields = '__all__'
        widgets = {
            'paciente': forms.HiddenInput(
                attrs={
                    'required': False,
                    'class': 'django-evolution-form'
                }
            ),
            'evolucion': forms.Textarea(
                attrs={
                    'rows': '3',
                    'class': 'django-evolution-form'
                }
            )
        }
        
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'id': 'id_test_nombre',
                    'class': 'django-test-form'
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'rows': '3',
                    'id': 'id_test_descripcion',
                    'class': 'django-test-form'
                }
            ),
            'categoria': forms.Select(
                choices=get_category_options(),
                attrs={
                    'class': 'django-test-form'
                }
            ),
            'subcategoria': forms.TextInput(),
            'tipo_resultado': forms.Select(
                choices=TEST_RESPONSE_TYPE,
                attrs={
                    'class': 'django-test-form'
                }
            )
        }

class PatientTestForm(forms.ModelForm):
    class Meta:
        model = PacienteTest
        fields = '__all__'
        widgets = {
            'paciente': forms.HiddenInput(
                attrs={
                    'required': False,
                    'class': 'django-patient-test-form'
                }
            ),
            'test': forms.Select(
                choices=get_test_options(),
                attrs={
                    'class': 'django-patient-test-form'
                }
            ),
            'resultado': forms.Textarea(attrs={
                'rows': '3',
                'class': 'django-patient-test-form'
            })
        }