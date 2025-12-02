from django import forms
from partosApp.models import RegistroParto


class TrabajoDePartoForm(forms.ModelForm):
    
    class Meta:
        model = RegistroParto
        fields = [
            'vih_tomado_prepartos',
            'vih_tomado_sala',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'monitor_ttc',
            'induccion',
            'aceleracion_correccion',
            'numero_tactos_vaginales',
            'rotura_membrana',
            'tiempo_membranas_rotas',
            'tiempo_dilatacion',
            'tiempo_expulsivo',
        ]
        
        widgets = {
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_tomado_sala': forms.Select(attrs={'class': 'form-select'}),
            'edad_gestacional_semanas': forms.NumberInput(attrs={'class': 'form-control', 'min': '20', 'max': '42'}),
            'edad_gestacional_dias': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '6'}),
            'monitor_ttc': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'induccion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aceleracion_correccion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numero_tactos_vaginales': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'rotura_membrana': forms.Select(attrs={'class': 'form-select'}),
            'tiempo_membranas_rotas': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.5'}),
            'tiempo_dilatacion': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'tiempo_expulsivo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
        
        labels = {
            'vih_tomado_prepartos': 'VIH tomado en Prepartos',
            'vih_tomado_sala': 'VIH tomado en Sala',
            'edad_gestacional_semanas': 'Edad Gestacional (semanas)',
            'edad_gestacional_dias': 'Edad Gestacional (días)',
            'monitor_ttc': 'Monitor TTC',
            'induccion': 'Inducción',
            'aceleracion_correccion': 'Aceleración o Corrección',
            'numero_tactos_vaginales': 'Número de Tactos Vaginales',
            'rotura_membrana': 'Rotura de Membrana',
            'tiempo_membranas_rotas': 'Tiempo Membranas Rotas (horas)',
            'tiempo_dilatacion': 'Tiempo de Dilatación (minutos)',
            'tiempo_expulsivo': 'Tiempo Expulsivo (minutos)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        campos_opcionales = [
            'tiempo_membranas_rotas', 'tiempo_dilatacion', 
            'tiempo_expulsivo', 'numero_tactos_vaginales'
        ]
        
        for campo in campos_opcionales:
            if campo in self.fields:
                self.fields[campo].required = False
