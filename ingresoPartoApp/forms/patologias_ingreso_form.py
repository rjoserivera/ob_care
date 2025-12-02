from django import forms
from ingresoPartoApp.models import FichaParto


class PatologiasIngresoForm(forms.ModelForm):
    
    class Meta:
        model = FichaParto
        fields = [
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_grave',
            'infeccion_ovular',
            'otra_patologia'
        ]
        
        widgets = {
            'preeclampsia_severa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'eclampsia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sepsis_infeccion_grave': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'infeccion_ovular': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'otra_patologia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especifique otra patología si aplica'
            })
        }
        
        labels = {
            'preeclampsia_severa': 'Preeclampsia Severa',
            'eclampsia': 'Eclampsia',
            'sepsis_infeccion_grave': 'Sepsis o Infección Sistémica Grave',
            'infeccion_ovular': 'Infección Ovular o Corioamnionitis',
            'otra_patologia': 'Otra Patología'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otra_patologia'].required = False
