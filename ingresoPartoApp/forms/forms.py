"""
ingresoPartoApp/forms/forms.py
Formulario para FichaParto - Según modelo real
"""

from django import forms
from ..models import FichaParto


class FichaPartoForm(forms.ModelForm):
    """Formulario para crear/editar ficha de ingreso a parto"""
    
    class Meta:
        model = FichaParto
        fields = [
            # Datos de ingreso
            'fecha_ingreso',
            'hora_ingreso',
            
            # Evaluación inicial
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'dilatacion_cervical_cm',
            'posicion_fetal',
            'altura_presentacion',
            'membranas_rotas',
            'caracteristicas_liquido',
            
            # Evaluación fetal
            'frecuencia_cardiaca_fetal',
            'cardiotocografia_realizada',
            'resultado_ctg',
            
            # Evaluación materna
            'presion_arterial_sistolica',
            'presion_arterial_diastolica',
            'frecuencia_cardiaca_materna',
            'temperatura',
            
            # Laboratorio
            'sgb_pesquisa',
            'sgb_resultado',
            'vih_tomado',
            'vih_resultado',
            'vdrl_resultado',
            'hepatitis_b_tomado',
            
            # Diagnóstico
            'diagnostico_ingreso',
            'observaciones',
        ]
        
        widgets = {
            # Datos de ingreso
            'fecha_ingreso': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'hora_ingreso': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            
            # Evaluación inicial
            'edad_gestacional_semanas': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '20', 'max': '45'}
            ),
            'edad_gestacional_dias': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '0', 'max': '6'}
            ),
            'dilatacion_cervical_cm': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '0', 'max': '10', 'step': '0.5'}
            ),
            'posicion_fetal': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Cefálica'}
            ),
            'altura_presentacion': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: -2'}
            ),
            'membranas_rotas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'caracteristicas_liquido': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Claro'}
            ),
            
            # Evaluación fetal
            'frecuencia_cardiaca_fetal': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '100', 'max': '200', 'placeholder': 'lpm'}
            ),
            'cardiotocografia_realizada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'resultado_ctg': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Resultado CTG'}
            ),
            
            # Evaluación materna
            'presion_arterial_sistolica': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '60', 'max': '250', 'placeholder': 'mmHg'}
            ),
            'presion_arterial_diastolica': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '40', 'max': '150', 'placeholder': 'mmHg'}
            ),
            'frecuencia_cardiaca_materna': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '40', 'max': '200', 'placeholder': 'lpm'}
            ),
            'temperatura': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '35', 'max': '42', 'step': '0.1', 'placeholder': '°C'}
            ),
            
            # Laboratorio
            'sgb_pesquisa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sgb_resultado': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Positivo/Negativo'}
            ),
            'vih_tomado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_resultado': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Resultado VIH'}
            ),
            'vdrl_resultado': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Resultado VDRL'}
            ),
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Diagnóstico
            'diagnostico_ingreso': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Diagnóstico de ingreso...'}
            ),
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Observaciones...'}
            ),
        }
        
        labels = {
            'fecha_ingreso': 'Fecha de Ingreso',
            'hora_ingreso': 'Hora de Ingreso',
            'edad_gestacional_semanas': 'Semanas',
            'edad_gestacional_dias': 'Días',
            'dilatacion_cervical_cm': 'Dilatación (cm)',
            'posicion_fetal': 'Posición Fetal',
            'altura_presentacion': 'Altura Presentación',
            'membranas_rotas': 'Membranas Rotas',
            'caracteristicas_liquido': 'Características Líquido',
            'frecuencia_cardiaca_fetal': 'FCF (lpm)',
            'cardiotocografia_realizada': 'CTG Realizada',
            'resultado_ctg': 'Resultado CTG',
            'presion_arterial_sistolica': 'PA Sistólica',
            'presion_arterial_diastolica': 'PA Diastólica',
            'frecuencia_cardiaca_materna': 'FC Materna',
            'temperatura': 'Temperatura (°C)',
            'sgb_pesquisa': 'SGB Pesquisa',
            'sgb_resultado': 'Resultado SGB',
            'vih_tomado': 'VIH Tomado',
            'vih_resultado': 'Resultado VIH',
            'vdrl_resultado': 'Resultado VDRL',
            'hepatitis_b_tomado': 'Hepatitis B Tomado',
            'diagnostico_ingreso': 'Diagnóstico de Ingreso',
            'observaciones': 'Observaciones',
        }