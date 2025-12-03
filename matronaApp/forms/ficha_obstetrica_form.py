# matronaApp/ficha_obstetrica_form.py
"""
Formulario para crear/editar Ficha Obstétrica
Incluye patologías como checkboxes SÍ/NO
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import FichaObstetrica, MedicamentoFicha
from datetime import date


class FichaObstetricaForm(forms.ModelForm):
    """
    Formulario para crear/editar Ficha Obstétrica
    Patologías son campos checkbox (SÍ/NO), no gestión separada
    """
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'numero_ficha',
            'nombre_acompanante',
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'nacidos_vivos',
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'peso_actual',
            'talla',
            # PATOLOGÍAS - CHECKBOXES SÍ/NO
            'vih_tomado',
            'vih_resultado',
            'vih_aro',
            'sgb_pesquisa',
            'sgb_resultado',
            'sgb_antibiotico',
            'vdrl_resultado',
            'vdrl_tratamiento_atb',
            'hepatitis_b_tomado',
            'hepatitis_b_resultado',
            'hepatitis_b_derivacion',
            'observaciones',
            'antecedentes_relevantes',
            'matrona_responsable',
        ]
        
        widgets = {
            # Identificación
            'numero_ficha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número único de ficha',
            }),
            
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del acompañante',
            }),
            
            # Historia obstétrica
            'numero_gestas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            
            'numero_partos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            
            'partos_vaginales': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            
            'partos_cesareas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            
            'numero_abortos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            
            'nacidos_vivos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            
            # Embarazo actual
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '42',
            }),
            
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6',
            }),
            
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'kg',
            }),
            
            'talla': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'cm',
            }),
            
            # PATOLOGÍAS - CHECKBOXES
            'vih_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'vih_resultado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Positivo/Negativo/Sin hacer',
            }),
            
            'vih_aro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de ARO',
            }),
            
            'sgb_pesquisa': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'sgb_resultado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Positivo/Negativo',
            }),
            
            'sgb_antibiotico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Antibiótico usado',
            }),
            
            'vdrl_resultado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resultado VDRL',
            }),
            
            'vdrl_tratamiento_atb': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'hepatitis_b_resultado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resultado Hepatitis B',
            }),
            
            'hepatitis_b_derivacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones generales',
            }),
            
            'antecedentes_relevantes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Antecedentes médicos relevantes',
            }),
            
            'matrona_responsable': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
    
    def clean(self):
        """Validaciones"""
        cleaned_data = super().clean()
        
        fecha_ultima_regla = cleaned_data.get('fecha_ultima_regla')
        fecha_probable_parto = cleaned_data.get('fecha_probable_parto')
        edad_gestacional = cleaned_data.get('edad_gestacional_semanas')
        
        # Validar que no sean en el futuro
        if fecha_ultima_regla and fecha_ultima_regla > date.today():
            raise ValidationError("❌ La FUR no puede ser en el futuro.")
        
        # Validar edad gestacional lógica
        if edad_gestacional and (edad_gestacional < 0 or edad_gestacional > 42):
            raise ValidationError("❌ La edad gestacional debe estar entre 0 y 42 semanas.")
        
        return cleaned_data


class MedicamentoFichaForm(forms.ModelForm):
    """
    Formulario para agregar medicamentos a una ficha obstétrica
    """
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'nombre_medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_termino',
            'observaciones',
        ]
        
        widgets = {
            'nombre_medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento',
            }),
            
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg, 2 comprimidos',
            }),
            
            'via_administracion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Oral, IV, IM',
            }),
            
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 8 horas',
            }),
            
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            
            'fecha_termino': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones',
            }),
        }
    
    def clean(self):
        """Validar fechas"""
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_termino = cleaned_data.get('fecha_termino')
        
        if fecha_inicio and fecha_termino:
            if fecha_termino < fecha_inicio:
                raise ValidationError("❌ Fecha de término no puede ser anterior a inicio.")
        
        return cleaned_data