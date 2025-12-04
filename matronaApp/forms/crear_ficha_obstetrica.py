"""
matronaApp/forms/crear ficha obstetrica.py
Formularios para fichas obstétricas con todos los nuevos campos
Usa FK a catálogos, NO choices
"""

from django import forms
from models import FichaObstetrica, MedicamentoFicha, CatalogoConsultorioOrigen, CatalogoViaAdministracion


class FichaObstetricaForm(forms.ModelForm):
    """Formulario para crear/editar ficha obstétrica"""
    
    class Meta:
        model = FichaObstetrica
        fields = [
            # Sección 1: Identificación
            'nombre_acompanante',
            
            # Sección 2: Datos Generales
            'plan_de_parto',
            'visita_guiada',
            'imc',
            'consultorio_origen',
            
            # Sección 3: Historia Obstétrica
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'nacidos_vivos',
            
            # Sección 4: Embarazo Actual
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'peso_actual',
            'talla_actual',
            
            # Sección 5: Patologías
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_sistemia',
            'infeccion_ovular',
            'otras_patologias',
            
            # Sección 6: Control Prenatal
            'control_prenatal',
            'numero_controles',
        ]
        
        widgets = {
            # Identificación
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del acompañante'
            }),
            
            # Datos Generales
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
                'class': 'form-control'
            }),
            
            # Historia Obstétrica
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
            
            # Embarazo Actual
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '42'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6'
            }),
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'kg',
                'step': '0.1'
            }),
            'talla_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'cm',
                'step': '0.1'
            }),
            
            # Patologías
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
                'placeholder': 'Describa otras patologías si las hay'
            }),
            
            # Control Prenatal
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'numero_controles': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }


class MedicamentoFichaForm(forms.ModelForm):
    """Formulario para asignar medicamentos a una ficha"""
    
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
            'activo',
        ]
        
        widgets = {
            'medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg, 10ml, etc.'
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 6 horas, Cada 8 horas'
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
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }