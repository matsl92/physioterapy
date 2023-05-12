from django import forms
from .models import Paciente

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
                'class': 'form-control'
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
            'ocupacion': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'profesion': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'seguridad_social': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'diagnostico_medico': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'motivo_consulta': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'cronologia_de_patologia': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'actividad_fisica': forms.CheckboxInput(attrs={
                'class': 'form-control'
            }),
            'tipo_actividad_fisica': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'frecuencia_actividad_fisica': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'conclusion': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'adjuntar_documento': forms.FileInput(attrs={
                'class': 'form-control'
            })
            
        }