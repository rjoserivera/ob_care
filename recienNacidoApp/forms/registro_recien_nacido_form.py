"""
Formulario para Registro de Recién Nacido
recienNacidoApp/forms/registro_recien_nacido_form.py
"""
from django import forms
from django.core.exceptions import ValidationError
from recienNacidoApp.models import RegistroRecienNacido
from partosApp.models import RegistroParto


class RegistroRecienNacidoForm(forms.ModelForm):
    """
    Formulario completo para registrar al recién nacido
    Incluye: datos básicos, apego y acompañamiento
    """
    
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'registro_parto',
            # Datos del RN
            'sexo',
            'peso',
            'talla',
            'ligadura_tardia_cordon',
            'apgar_1_minuto',
            'apgar_5_minutos',
            'fecha_nacimiento',
            # Apego
            'tiempo_apego',
            'apego_canguro',
            # Acompañamiento
            'acompanamiento_preparto',
            'acompanamiento_parto',
            'acompanamiento_rn',
            'motivo_no_acompanado',
            'persona_acompanante',
            'acompanante_secciona_cordon',
        ]
        
        widgets = {
            # Relación con parto
            'registro_parto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            
            # Datos del RN
            'sexo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Peso en gramos (500-8000)',
                'min': 500,
                'max': 8000,
                'required': True
            }),
            'talla': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Talla en cm (30-70)',
                'min': 30,
                'max': 70,
                'required': True
            }),
            'ligadura_tardia_cordon': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'apgar_1_minuto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Puntaje 0-10',
                'min': 0,
                'max': 10,
                'required': True
            }),
            'apgar_5_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Puntaje 0-10',
                'min': 0,
                'max': 10,
                'required': True
            }),
            'fecha_nacimiento': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            
            # Apego
            'tiempo_apego': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutos de apego',
                'min': 0
            }),
            'apego_canguro': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Acompañamiento
            'acompanamiento_preparto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'acompanamiento_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'acompanamiento_rn': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'motivo_no_acompanado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'persona_acompanante': forms.Select(attrs={
                'class': 'form-select'
            }),
            'acompanante_secciona_cordon': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        labels = {
            'registro_parto': 'Registro de Parto',
            'sexo': 'Sexo del Recién Nacido',
            'peso': 'Peso al Nacer',
            'talla': 'Talla al Nacer',
            'ligadura_tardia_cordon': 'Ligadura Tardía del Cordón (> 1 minuto)',
            'apgar_1_minuto': 'Apgar al Minuto',
            'apgar_5_minutos': 'Apgar a los 5 Minutos',
            'fecha_nacimiento': 'Fecha y Hora de Nacimiento',
            'tiempo_apego': 'Tiempo de Apego Piel con Piel',
            'apego_canguro': 'Apego Canguro',
            'acompanamiento_preparto': 'Acompañamiento en Preparto',
            'acompanamiento_parto': 'Acompañamiento en Parto',
            'acompanamiento_rn': 'Acompañamiento del RN',
            'motivo_no_acompanado': 'Motivo de Parto NO Acompañado',
            'persona_acompanante': 'Persona Acompañante',
            'acompanante_secciona_cordon': 'Acompañante Secciona Cordón',
        }
        
        help_texts = {
            'peso': 'Peso en gramos (rango válido: 500-8000 g)',
            'talla': 'Talla en centímetros (rango válido: 30-70 cm)',
            'apgar_1_minuto': 'Evaluación al primer minuto (0-10)',
            'apgar_5_minutos': 'Evaluación a los 5 minutos (0-10)',
            'tiempo_apego': 'Duración en minutos del contacto piel con piel',
            'motivo_no_acompanado': 'Solo si no hubo acompañamiento',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar QuerySet de registro_parto si es necesario
        # Por ejemplo, solo mostrar partos sin recién nacido registrado aún
        if not self.instance.pk:
            self.fields['registro_parto'].queryset = RegistroParto.objects.filter(
                recien_nacidos__isnull=True
            )
    
    def clean_peso(self):
        """Validar peso del recién nacido"""
        peso = self.cleaned_data.get('peso')
        
        if peso:
            if peso < 500:
                raise ValidationError('El peso es demasiado bajo. Verificar.')
            if peso > 8000:
                raise ValidationError('El peso es demasiado alto. Verificar.')
        
        return peso
    
    def clean_talla(self):
        """Validar talla del recién nacido"""
        talla = self.cleaned_data.get('talla')
        
        if talla:
            if talla < 30:
                raise ValidationError('La talla es demasiado baja. Verificar.')
            if talla > 70:
                raise ValidationError('La talla es demasiado alta. Verificar.')
        
        return talla
    
    def clean(self):
        """Validaciones generales del formulario"""
        cleaned_data = super().clean()
        
        # Validar Apgar
        apgar_1 = cleaned_data.get('apgar_1_minuto')
        apgar_5 = cleaned_data.get('apgar_5_minutos')
        
        if apgar_1 is not None and apgar_5 is not None:
            # Normalmente el Apgar a los 5 minutos debería ser igual o mayor
            if apgar_5 < apgar_1 - 2:
                self.add_error('apgar_5_minutos', 
                    'El Apgar a los 5 minutos es significativamente menor. Verificar.')
        
        # Validar acompañamiento
        tiene_acomp = any([
            cleaned_data.get('acompanamiento_preparto'),
            cleaned_data.get('acompanamiento_parto'),
            cleaned_data.get('acompanamiento_rn')
        ])
        
        motivo = cleaned_data.get('motivo_no_acompanado')
        persona = cleaned_data.get('persona_acompanante')
        
        if not tiene_acomp and not motivo:
            self.add_error('motivo_no_acompanado',
                'Debe indicar el motivo si no hubo acompañamiento.')
        
        if tiene_acomp and not persona:
            self.add_error('persona_acompanante',
                'Debe indicar quién acompañó.')
        
        return cleaned_data
