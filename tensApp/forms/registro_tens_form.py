"""
Formulario para Registro TENS
tensApp/forms/registro_tens_form.py
"""
from django import forms
from django.core.exceptions import ValidationError
from tensApp.models import RegistroTens
from matronaApp.models import FichaObstetrica
from gestionApp.models import Tens


class RegistroTensForm(forms.ModelForm):
    """
    Formulario para registro de signos vitales por TENS
    Incluye: temperatura, presión arterial, frecuencia cardíaca, etc.
    """
    
    class Meta:
        model = RegistroTens
        fields = [
            'ficha',
            'tens_responsable',
            'fecha',
            'temperatura',
            'frecuencia_cardiaca',
            'presion_arterial_sistolica',
            'presion_arterial_diastolica',
            'frecuencia_respiratoria',
            'saturacion_oxigeno',
            'observaciones',
        ]
        
        widgets = {
            'ficha': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'tens_responsable': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'temperatura': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 36.5',
                'step': '0.1',
                'min': '35.0',
                'max': '42.0'
            }),
            'frecuencia_cardiaca': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 80',
                'min': '40',
                'max': '200'
            }),
            'presion_arterial_sistolica': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 120',
                'min': '60',
                'max': '250'
            }),
            'presion_arterial_diastolica': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 80',
                'min': '40',
                'max': '150'
            }),
            'frecuencia_respiratoria': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 16',
                'min': '8',
                'max': '40'
            }),
            'saturacion_oxigeno': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 98',
                'min': '50',
                'max': '100'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales sobre los signos vitales...'
            }),
        }
        
        labels = {
            'ficha': 'Ficha Obstétrica',
            'tens_responsable': 'TENS Responsable',
            'fecha': 'Fecha del Registro',
            'temperatura': 'Temperatura Corporal',
            'frecuencia_cardiaca': 'Frecuencia Cardíaca',
            'presion_arterial_sistolica': 'Presión Arterial Sistólica',
            'presion_arterial_diastolica': 'Presión Arterial Diastólica',
            'frecuencia_respiratoria': 'Frecuencia Respiratoria',
            'saturacion_oxigeno': 'Saturación de Oxígeno',
            'observaciones': 'Observaciones',
        }
        
        help_texts = {
            'temperatura': 'Temperatura en grados Celsius (35.0 - 42.0°C)',
            'frecuencia_cardiaca': 'Latidos por minuto (lpm)',
            'presion_arterial_sistolica': 'Valor superior de presión arterial (mmHg)',
            'presion_arterial_diastolica': 'Valor inferior de presión arterial (mmHg)',
            'frecuencia_respiratoria': 'Respiraciones por minuto (rpm)',
            'saturacion_oxigeno': 'Porcentaje de saturación (SpO2)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar solo fichas activas
        self.fields['ficha'].queryset = FichaObstetrica.objects.filter(activa=True)
        
        # Filtrar solo TENS activos
        self.fields['tens_responsable'].queryset = Tens.objects.filter(Activo=True)
    
    def clean_temperatura(self):
        """Validar temperatura corporal"""
        temperatura = self.cleaned_data.get('temperatura')
        
        if temperatura:
            if temperatura < 35.0:
                raise ValidationError('Temperatura muy baja (hipotermia). Verificar.')
            if temperatura > 42.0:
                raise ValidationError('Temperatura muy alta. Verificar.')
            
            # Advertencias
            if temperatura < 36.0:
                # Hipotermia leve, pero aceptable en algunos casos
                pass
            if temperatura > 38.0:
                # Fiebre, registrar pero no bloquear
                pass
        
        return temperatura
    
    def clean_frecuencia_cardiaca(self):
        """Validar frecuencia cardíaca"""
        fc = self.cleaned_data.get('frecuencia_cardiaca')
        
        if fc:
            if fc < 40:
                raise ValidationError('Frecuencia cardíaca muy baja (bradicardia severa). Verificar.')
            if fc > 200:
                raise ValidationError('Frecuencia cardíaca muy alta. Verificar.')
        
        return fc
    
    def clean_saturacion_oxigeno(self):
        """Validar saturación de oxígeno"""
        sat = self.cleaned_data.get('saturacion_oxigeno')
        
        if sat:
            if sat < 50:
                raise ValidationError('Saturación de oxígeno muy baja. Verificar.')
            if sat > 100:
                raise ValidationError('Saturación de oxígeno no puede ser mayor a 100%.')
        
        return sat
    
    def clean(self):
        """Validaciones generales del formulario"""
        cleaned_data = super().clean()
        
        # Validar presión arterial
        sistolica = cleaned_data.get('presion_arterial_sistolica')
        diastolica = cleaned_data.get('presion_arterial_diastolica')
        
        if sistolica and diastolica:
            if sistolica <= diastolica:
                self.add_error('presion_arterial_sistolica',
                    'La presión sistólica debe ser mayor que la diastólica.')
                self.add_error('presion_arterial_diastolica',
                    'La presión diastólica debe ser menor que la sistólica.')
            
            # Validar rangos
            if sistolica < 80 or sistolica > 200:
                self.add_error('presion_arterial_sistolica',
                    'Presión sistólica fuera del rango esperado (80-200 mmHg).')
            
            if diastolica < 40 or diastolica > 120:
                self.add_error('presion_arterial_diastolica',
                    'Presión diastólica fuera del rango esperado (40-120 mmHg).')
        
        return cleaned_data
