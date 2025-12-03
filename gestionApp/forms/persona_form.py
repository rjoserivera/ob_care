# gestionApp/persona_form.py
"""
Formulario para registrar/editar Persona
Solo datos básicos (sin ser paciente aún)
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Persona, Nacionalidad, PuebloOriginario, Sexo
from datetime import date


class PersonaForm(forms.ModelForm):
    """
    Formulario para registrar/editar una Persona
    Datos básicos solamente
    Se vuelve Paciente cuando se crea una Ficha Obstétrica
    """
    
    class Meta:
        model = Persona
        fields = [
            'Rut',
            'Nombre',
            'Apellido_Paterno',
            'Apellido_Materno',
            'Fecha_nacimiento',
            'sexo',
            'nacionalidad',
            'pueblo_originario',
            'Telefono',
            'Direccion',
            'Inmigrante',
            'Discapacidad',
            'Tipo_de_Discapacidad',
            'Privada_de_Libertad',
            'Trans_Masculino',
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
            
            # Datos básicos
            'Fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            
            'sexo': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            'nacionalidad': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            'pueblo_originario': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            # Contacto
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678',
                'type': 'tel',
            }),
            
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa',
            }),
            
            # Situaciones especiales
            'Inmigrante': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'Discapacidad': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'Tipo_de_Discapacidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especificar tipo de discapacidad',
            }),
            
            'Privada_de_Libertad': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'Trans_Masculino': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
    
    def clean(self):
        """Validaciones"""
        cleaned_data = super().clean()
        
        # Validar fecha de nacimiento
        fecha_nac = cleaned_data.get('Fecha_nacimiento')
        if fecha_nac and fecha_nac > date.today():
            raise ValidationError("❌ La fecha de nacimiento no puede ser en el futuro.")
        
        # Validar edad mínima
        if fecha_nac:
            from dateutil.relativedelta import relativedelta
            edad = relativedelta(date.today(), fecha_nac).years
            if edad < 10:
                raise ValidationError("❌ La persona debe tener al menos 10 años.")
        
        # Validar que si marcó discapacidad, especifique tipo
        if cleaned_data.get('Discapacidad') and not cleaned_data.get('Tipo_de_Discapacidad'):
            raise ValidationError({
                'Tipo_de_Discapacidad': 'Debe especificar el tipo de discapacidad.'
            })
        
        return cleaned_data


class BuscarPersonaForm(forms.Form):
    """
    Formulario para buscar una persona existente
    """
    
    query = forms.CharField(
        max_length=100,
        required=True,
        label='Buscar por RUT o Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese RUT o nombre',
            'autocomplete': 'off',
        })
    )
    
    def clean_query(self):
        """Validar que tenga al menos 2 caracteres"""
        query = self.cleaned_data.get('query', '').strip()
        if len(query) < 2:
            raise ValidationError("❌ Ingrese al menos 2 caracteres para buscar.")
        return query