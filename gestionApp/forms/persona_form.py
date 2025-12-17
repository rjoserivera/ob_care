# gestionApp/forms/persona_form.py
"""
Formulario para gestión de Personas
CORREGIDO: Agregado campo Email
"""

from django import forms
from django.core.exceptions import ValidationError
from ..models import Persona


class PersonaForm(forms.ModelForm):
    """
    Formulario para registrar y editar Personas
    """
    
    class Meta:
        model = Persona
        fields = [
            'Rut',
            'Nombre',
            'Apellido_Paterno',
            'Apellido_Materno',
            'Fecha_nacimiento',
            'Sexo',
            'Nacionalidad',
            'Pueblos_originarios',
            'Telefono',
            'Email',  # ✅ AGREGADO
            'Direccion',
            'Inmigrante',
            'Privada_de_Libertad',
        ]
        
        widgets = {
            # Identificación
            'Rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9',
                'pattern': '[0-9]{7,8}-[0-9Kk]',
            }),
            
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la persona',
            }),
            
            'Apellido_Paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido paterno',
            }),
            
            'Apellido_Materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido materno',
            }),
            
            # Fecha de nacimiento
            'Fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            
            # Selects
            'Sexo': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            'Nacionalidad': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            'Pueblos_originarios': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            # Contacto
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678',
                'type': 'tel',
            }),
            
            # ✅ EMAIL AGREGADO
            'Email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com',
            }),
            
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa',
            }),
            
            # Checkboxes
            'Inmigrante': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'Privada_de_Libertad': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar formato de fecha para edición
        if self.instance and self.instance.pk:
            if self.instance.Fecha_nacimiento:
                self.initial['Fecha_nacimiento'] = self.instance.Fecha_nacimiento.strftime('%Y-%m-%d')


class BuscarPersonaForm(forms.Form):
    """
    Formulario para buscar persona por RUT
    """
    rut = forms.CharField(
        max_length=12,
        label='RUT',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 12345678-9',
            'autofocus': True,
        })
    )