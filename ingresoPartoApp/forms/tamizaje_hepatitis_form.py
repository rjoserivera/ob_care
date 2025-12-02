from django import forms
from ingresoPartoApp.models import FichaParto


class TamizajeHepatitisForm(forms.ModelForm):
    
    class Meta:
        model = FichaParto
        fields = [
            'hepatitis_b_tomado',
            'derivacion_gastro'
        ]
        
        widgets = {
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'derivacion_gastro': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'hepatitis_b_tomado': '¿Se tomó examen de Hepatitis B?',
            'derivacion_gastro': '¿Requiere derivación a Gastro-Hepatólogo?'
        }
