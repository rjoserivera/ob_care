from django import forms
from django.core.exceptions import ValidationError
from ingresoPartoApp.models import FichaParto


class TamizajeSGBForm(forms.ModelForm):
    
    class Meta:
        model = FichaParto
        fields = [
            'sgb_pesquisa',
            'sgb_resultado',
            'antibiotico_sgb'
        ]
        
        widgets = {
            'sgb_pesquisa': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_sgb_pesquisa'
            }),
            'sgb_resultado': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_sgb_resultado'
            }),
            'antibiotico_sgb': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'sgb_pesquisa': '¿Se realizó pesquisa SGB?',
            'sgb_resultado': 'Resultado SGB',
            'antibiotico_sgb': 'Antibiótico por SGB (NO por RPM)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sgb_resultado'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        
        sgb_pesquisa = cleaned_data.get('sgb_pesquisa')
        sgb_resultado = cleaned_data.get('sgb_resultado')
        
        if sgb_pesquisa and not sgb_resultado:
            raise ValidationError({
                'sgb_resultado': 'Debe ingresar el resultado de la pesquisa SGB.'
            })
        
        return cleaned_data
