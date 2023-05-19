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
            'cedula': forms.TextInput(),
            'nombre': forms.TextInput(),
            'apellidos': forms.TextInput(),
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date'
            }),
            'telefono': forms.TextInput(),
            'email': forms.EmailInput(),
            'acompanante': forms.TextInput(),
            'parentesco': forms.TextInput(),
            'telefono_acompanante': forms.TextInput(),
            'ocupacion': forms.Select(
                choices=OCUPACION_OPCIONES,
                ),
            'profesion': forms.TextInput(),
            'seguridad_social': forms.TextInput(),
            'diagnostico': forms.Select(
                choices=[get_diagnosis_options()],
                ),
            'motivo_consulta': forms.Textarea(attrs={
                'rows': "3"
            }),
            'cronologia_de_patologia': forms.Textarea(attrs={
                'rows': "3"
            }),
            'actividad_fisica': forms.CheckboxInput(),
            'tipo_actividad_fisica': forms.TextInput(),
            'frecuencia_actividad_fisica': forms.Select(
                choices=FRECUENCIA_ACTIVIDAD_FISICA_OPCIONES
            ),
            'conclusion': forms.Textarea(attrs={
                'rows': "3"    
            }),
            'adjuntar_documento': forms.FileInput()
            
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
                    'id': 'id_test_nombre',
                    'class': 'form-control',
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