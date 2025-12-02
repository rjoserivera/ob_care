from django import forms
from medicoApp.models import Patologias


class TogglePatologiaForm(forms.ModelForm):
    
    class Meta:
        model = Patologias
        fields = ['estado']
        
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        
        labels = {
            'estado': 'Estado de la Patología'
        }
