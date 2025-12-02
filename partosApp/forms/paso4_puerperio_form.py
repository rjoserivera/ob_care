from django import forms
from partosApp.models import RegistroParto


class PuerperioForm(forms.ModelForm):
    
    class Meta:
        model = RegistroParto
        fields = [
            'contacto_piel_piel',
            'lactancia_primera_hora',
            'apego_precoz',
            'sangrado_postparto',
            'hemorragia_postparto',
            'retencion_placentaria',
        ]
        
        widgets = {
            'contacto_piel_piel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lactancia_primera_hora': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'apego_precoz': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sangrado_postparto': forms.Select(attrs={'class': 'form-select'}),
            'hemorragia_postparto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'retencion_placentaria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'contacto_piel_piel': 'Contacto Piel a Piel',
            'lactancia_primera_hora': 'Lactancia en la Primera Hora',
            'apego_precoz': 'Apego Precoz',
            'sangrado_postparto': 'Sangrado Postparto',
            'hemorragia_postparto': 'Hemorragia Postparto',
            'retencion_placentaria': 'Retención Placentaria',
        }
