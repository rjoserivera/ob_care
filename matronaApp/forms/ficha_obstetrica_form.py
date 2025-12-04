"""
matronaApp/forms/ficha_obstetrica.py
Formularios para FichaObstetrica
CORREGIDO: Solo incluye campos que existen en el modelo
"""

from django import forms
from ..models import FichaObstetrica, MedicamentoFicha, CatalogoViaAdministracion


class FichaObstetricaForm(forms.ModelForm):
    """
    Formulario para crear/editar Ficha Obstétrica
    INCLUYE SOLO los campos que existen en el modelo FichaObstetrica
    """
    
    edad_gestacional_semanas = forms.IntegerField(
        min_value=1,
        max_value=42,
        required=False,
        label='Semanas de Gestación',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0-42'
        })
    )
    
    edad_gestacional_dias = forms.IntegerField(
        min_value=0,
        max_value=6,
        required=False,
        label='Días Adicionales',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0-6'
        })
    )
    
    class Meta:
        model = FichaObstetrica
        fields = [
            # Sección Identificación
            'nombre_acompanante',
            
            # Sección Datos Generales
            'plan_de_parto',
            'visita_guiada',
            'imc',
            'consultorio_origen',
            
            # Sección Historia Obstétrica
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'nacidos_vivos',
            
            # Sección Embarazo Actual
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'peso_actual',
            'talla_actual',
            
            # Sección Patologías
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_sistemia',
            'infeccion_ovular',
            'otras_patologias',
            
            # Sección Control Prenatal
            'control_prenatal',
            'numero_controles',
        ]
        
        widgets = {
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del acompañante'
            }),
            
            'plan_de_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            'visita_guiada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            'imc': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 24.5',
                'step': '0.1'
            }),
            
            'consultorio_origen': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            'numero_gestas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            
            'numero_partos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            
            'partos_vaginales': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            
            'partos_cesareas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            
            'numero_abortos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            
            'nacidos_vivos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kg',
                'step': '0.1'
            }),
            
            'talla_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'cm',
                'step': '0.1'
            }),
            
            'preeclampsia_severa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            'eclampsia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            'sepsis_infeccion_sistemia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            'infeccion_ovular': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            'otras_patologias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describir otras patologías'
            }),
            
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            'numero_controles': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que partos_vaginales + partos_cesareas = numero_partos
        numero_partos = cleaned_data.get('numero_partos')
        partos_vaginales = cleaned_data.get('partos_vaginales')
        partos_cesareas = cleaned_data.get('partos_cesareas')
        
        if numero_partos and partos_vaginales and partos_cesareas:
            if partos_vaginales + partos_cesareas != numero_partos:
                raise forms.ValidationError(
                    'La suma de partos vaginales y cesáreas debe ser igual al número de partos'
                )
        
        return cleaned_data


class MedicamentoFichaForm(forms.ModelForm):
    """
    Formulario para agregar medicamentos a una ficha
    """
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_termino',
            'indicaciones',
        ]
        
        widgets = {
            'medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento'
            }),
            
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg'
            }),
            
            'via_administracion': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 6 horas'
            }),
            
            'fecha_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            
            'fecha_termino': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            
            'indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indicaciones especiales'
            }),
        }


