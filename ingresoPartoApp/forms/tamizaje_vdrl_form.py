from django import forms
from ingresoPartoApp.models import FichaParto


class TamizajeVDRLForm(forms.ModelForm):
    
    class Meta:
        model = FichaParto
        fields = [
            'vdrl_resultado',
            'tratamiento_sifilis'
        ]
        
        widgets = {
            'vdrl_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tratamiento_sifilis': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'vdrl_resultado': 'Resultado VDRL durante embarazo',
            'tratamiento_sifilis': 'Tratamiento antibiótico por sífilis al momento del parto'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vdrl_resultado'].required = False
