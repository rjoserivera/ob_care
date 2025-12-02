from django import forms
from django.core.exceptions import ValidationError
from ingresoPartoApp.models import FichaParto


class TamizajeVIHForm(forms.ModelForm):
    
    class Meta:
        model = FichaParto
        fields = [
            'numero_aro',
            'vih_tomado_prepartos',
            'vih_tomado_sala',
            'vih_orden_toma'
        ]
        
        widgets = {
            'numero_aro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número ARO'
            }),
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_vih_prepartos'
            }),
            'vih_tomado_sala': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_vih_sala'
            }),
            'vih_orden_toma': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        
        labels = {
            'numero_aro': 'Número ARO (Alto Riesgo Obstétrico)',
            'vih_tomado_prepartos': 'VIH tomado en Prepartos',
            'vih_tomado_sala': 'VIH tomado en Sala',
            'vih_orden_toma': 'Orden de Toma (1°, 2° o 3°)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['numero_aro'].required = False
        self.fields['vih_orden_toma'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        
        vih_prepartos = cleaned_data.get('vih_tomado_prepartos')
        vih_sala = cleaned_data.get('vih_tomado_sala')
        vih_orden = cleaned_data.get('vih_orden_toma')
        
        if (vih_prepartos or vih_sala) and not vih_orden:
            raise ValidationError({
                'vih_orden_toma': 'Debe especificar el orden de toma si se realizó el test de VIH.'
            })
        
        return cleaned_data
