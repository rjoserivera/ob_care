# matronaApp/forms/ficha_obstetrica_form.py
"""
Formulario para crear/editar Ficha Obstétrica
Incluye patologías como checkboxes SÍ/NO
"""

from django import forms
from django.core.exceptions import ValidationError
from matronaApp.models import FichaObstetrica, MedicamentoFicha  # ✅ CORRECTO
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
                'placeholder': 'Resultado de VDRL',
            }),
            
            'vdrl_tratamiento_atb': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tratamiento con antibiótico',
            }),
            
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'hepatitis_b_resultado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Positivo/Negativo',
            }),
            
            'hepatitis_b_derivacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Derivación si es necesaria',
            }),
            
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observaciones adicionales',
            }),
            
            'antecedentes_relevantes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Antecedentes médicos relevantes',
            }),
            
            'matrona_responsable': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
    
    def clean(self):
        """Validaciones adicionales"""
        cleaned_data = super().clean()
        
        # Validar que la edad gestacional sea coherente
        semanas = cleaned_data.get('edad_gestacional_semanas')
        dias = cleaned_data.get('edad_gestacional_dias')
        
        if semanas is not None and (semanas < 0 or semanas > 42):
            raise ValidationError("La edad gestacional debe estar entre 0 y 42 semanas.")
        
        if dias is not None and (dias < 0 or dias > 6):
            raise ValidationError("Los días deben estar entre 0 y 6.")
        
        # Validar fechas
        fum = cleaned_data.get('fecha_ultima_regla')
        fp = cleaned_data.get('fecha_probable_parto')
        
        if fum and fp and fum > fp:
            raise ValidationError("La fecha de última regla no puede ser posterior al parto probable.")
        
        return cleaned_data


class MedicamentoFichaForm(forms.ModelForm):
    """Formulario para agregar medicamentos a una ficha"""
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'nombre_medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_termino',
            'indicaciones',
        ]
        
        widgets = {
            'nombre_medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento',
            }),
            
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg',
            }),
            
            'via_administracion': forms.Select(attrs={
                'class': 'form-select',
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
            
            'indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indicaciones y observaciones',
            }),
        }