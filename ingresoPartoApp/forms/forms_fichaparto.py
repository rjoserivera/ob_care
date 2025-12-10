"""
ingresoPartoApp/forms/forms.py
Formulario simplificado para FichaParto
CORREGIDO: Solo campos que existen en el modelo
"""

from django import forms
from ..models import FichaParto


class FichaPartoForm(forms.ModelForm):
    """Formulario para crear/editar ficha de ingreso a parto"""
    
    class Meta:
        model = FichaParto
        fields = [
            # Datos básicos
            'fecha_ingreso',
            'hora_ingreso',
            
            # Exámenes VIH
            'vih_tomado_prepartos',
            'vih_tomado_sala',
            
            # SGB
            'sgb_pesquisa',
            'sgb_resultado',
            
            # VDRL
            'vdrl_resultado',
            
            # Hepatitis B
            'hepatitis_b_tomado',
        ]
        
        widgets = {
            'fecha_ingreso': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'hora_ingreso': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time',
                }
            ),
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_tomado_sala': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sgb_pesquisa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sgb_resultado': forms.Select(attrs={'class': 'form-select'}),
            'vdrl_resultado': forms.Select(attrs={'class': 'form-select'}),
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'fecha_ingreso': 'Fecha de Ingreso',
            'hora_ingreso': 'Hora de Ingreso',
            'vih_tomado_prepartos': 'VIH tomado en Prepartos',
            'vih_tomado_sala': 'VIH tomado en Sala',
            'sgb_pesquisa': 'Pesquisa SGB realizada',
            'sgb_resultado': 'Resultado SGB',
            'vdrl_resultado': 'Resultado VDRL',
            'hepatitis_b_tomado': 'Hepatitis B tomado',
        }
