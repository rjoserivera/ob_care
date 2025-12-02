from django import forms
from partosApp.models import RegistroParto


class InformacionPartoForm(forms.ModelForm):
    
    class Meta:
        model = RegistroParto
        fields = [
            'libertad_movimiento',
            'tipo_regimen',
            'tipo_parto',
            'alumbramiento_dirigido',
            'clasificacion_robson',
            'posicion_materna_parto',
        ]
        
        widgets = {
            'libertad_movimiento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_regimen': forms.Select(attrs={'class': 'form-select'}),
            'tipo_parto': forms.Select(attrs={'class': 'form-select'}),
            'alumbramiento_dirigido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'clasificacion_robson': forms.Select(attrs={'class': 'form-select'}),
            'posicion_materna_parto': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'libertad_movimiento': 'Libertad de Movimiento',
            'tipo_regimen': 'Tipo de Régimen',
            'tipo_parto': 'Tipo de Parto',
            'alumbramiento_dirigido': 'Alumbramiento Dirigido',
            'clasificacion_robson': 'Clasificación de Robson',
            'posicion_materna_parto': 'Posición Materna durante el Parto',
        }
