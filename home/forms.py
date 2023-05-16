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
                'class': 'form-control'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'acompanante': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'parentesco': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'telefono_acompanante': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'ocupacion': forms.Select(
                choices=OCUPACION_OPCIONES,
                attrs={
                'class': 'form-control'
            }),
            'profesion': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'seguridad_social': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'diagnostico': forms.Select(
                choices=[get_diagnosis_options()],
                attrs={
                'class': 'form-control'
            }),
            'motivo_consulta': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'cronologia_de_patologia': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'actividad_fisica': forms.CheckboxInput(attrs={
                'class': ''
            }),
            'tipo_actividad_fisica': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'frecuencia_actividad_fisica': forms.Select(
                choices=FRECUENCIA_ACTIVIDAD_FISICA_OPCIONES, 
                attrs={
                    'class': 'form-control'
                }
            ),
            'conclusion': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'adjuntar_documento': forms.FileInput(attrs={
                'class': 'form-control'
            })
            
        }

class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = '__all__'
        
class EvolutionForm(forms.ModelForm):
    class Meta: 
        model = Evolucion
        fields = '__all__'
        widgets = {
            'paciente': forms.HiddenInput(
                attrs={
                    'class': 'form-control',
                    'required': False
                }
            ),
            'evolucion': forms.Textarea(
                attrs={
                    'class': 'form-control'
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
                    'class': 'form-control'
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'categoria': forms.Select(
                choices=get_category_options(),
                attrs={
                    'class': 'form-control'
                }
            ),
            'subcategoria': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'tipo_resultado': forms.Select(
                choices=TEST_RESPONSE_TYPE,
                attrs={
                    'class': 'form-control'
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
                    'class': 'form-control'
                }
            ),
            'test': forms.Select(
                choices=get_test_options(),
                attrs={
                    'class': 'form-control'
                }
            ),
            'resultado': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            )
        }