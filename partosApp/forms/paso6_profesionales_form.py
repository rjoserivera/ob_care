from django import forms
from partosApp.models import RegistroParto


class ProfesionalesForm(forms.ModelForm):
    
    class Meta:
        model = RegistroParto
        fields = [
            'profesional_responsable',
            'alumno',
            'causa_cesarea',
            'observaciones',
            'uso_sala_saip',
        ]
        
        widgets = {
            'profesional_responsable': forms.Select(attrs={'class': 'form-select'}),
            'alumno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del alumno'}),
            'causa_cesarea': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Causa de cesárea si aplica'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones generales'}),
            'uso_sala_saip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'profesional_responsable': 'Profesional Responsable',
            'alumno': 'Alumno',
            'causa_cesarea': 'Causa de Cesárea',
            'observaciones': 'Observaciones',
            'uso_sala_saip': 'Uso de Sala SAIP',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['alumno'].required = False
        self.fields['causa_cesarea'].required = False
        self.fields['observaciones'].required = False
