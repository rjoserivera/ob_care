"""
ingresoPartoApp/forms.py
Formularios para ficha de parto al ingreso a sala
Usa FK a catálogos, NO choices
"""

from django import forms
from models import FichaParto


class FichaPartoForm(forms.ModelForm):
    """Formulario completo para ficha de parto"""
    
    class Meta:
        model = FichaParto
        fields = [
            # Sección 1: Datos Generales
            'tipo_paciente',
            'origen_ingreso',
            'fecha_ingreso',
            'hora_ingreso',
            
            # Sección 2: VIH y ARO
            'numero_aro',
            'vih_tomado_prepartos',
            'vih_tomado_sala',
            
            # Sección 3: Exámenes de Madre - SGB
            'sgb_pesquisa',
            'sgb_resultado',
            'sgb_antibiotico',
            
            # Sección 3: Exámenes de Madre - VDRL
            'vdrl_resultado',
            'vdrl_tratamiento_atb',
            
            # Sección 3: Exámenes de Madre - Hepatitis B
            'hepatitis_b_tomado',
            'hepatitis_b_derivacion',
            
            # Sección 4: Control Prenatal
            'control_prenatal',
            'consultorio_origen',
            'numero_controles',
            
            # Sección 5: Trabajo de Parto
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'monitor_ttc',
            'induccion',
            'aceleracion_correccion',
            'numero_tactos_vaginales',
            'rotura_membranas',
            'tiempo_membranas_rotas_horas',
            'tiempo_membranas_rotas_minutos',
            'tiempo_dilatacion_minutos',
            'tiempo_expulsivo_minutos',
            'libertad_movimiento',
            'regimen_trabajo_parto',
        ]
        
        widgets = {
            # Sección 1: Datos Generales
            'tipo_paciente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'origen_ingreso': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hora_ingreso': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            
            # Sección 2: VIH y ARO
            'numero_aro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ARO-12345'
            }),
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vih_tomado_sala': forms.Select(attrs={
                'class': 'form-control'
            }),
            
            # Sección 3: SGB
            'sgb_pesquisa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sgb_resultado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'sgb_antibiotico': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Sección 3: VDRL
            'vdrl_resultado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'vdrl_tratamiento_atb': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Sección 3: Hepatitis B
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hepatitis_b_derivacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Sección 4: Control Prenatal
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'consultorio_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del consultorio'
            }),
            'numero_controles': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            
            # Sección 5: Trabajo de Parto
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '20',
                'max': '42'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6'
            }),
            'monitor_ttc': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'induccion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'aceleracion_correccion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'numero_tactos_vaginales': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'rotura_membranas': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tiempo_membranas_rotas_horas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'tiempo_membranas_rotas_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '59'
            }),
            'tiempo_dilatacion_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'tiempo_expulsivo_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'libertad_movimiento': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'regimen_trabajo_parto': forms.Select(attrs={
                'class': 'form-control'
            }),
        }