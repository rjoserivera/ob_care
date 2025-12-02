from django import forms
from partosApp.models import RegistroParto
from matronaApp.models import FichaObstetrica


class RegistroPartoBaseForm(forms.ModelForm):
    
    class Meta:
        model = RegistroParto
        fields = [
            'ficha',
            'fecha_hora_admision',
            'fecha_hora_parto',
        ]
        widgets = {
            'ficha': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_hora_admision': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_hora_parto': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'ficha': 'Ficha Obstétrica',
            'fecha_hora_admision': 'Fecha y Hora de Admisión',
            'fecha_hora_parto': 'Fecha y Hora del Parto',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['ficha'].queryset = FichaObstetrica.objects.filter(
            activa=True
        ).select_related('paciente__persona')
        
        self.fields['fecha_hora_parto'].required = False
