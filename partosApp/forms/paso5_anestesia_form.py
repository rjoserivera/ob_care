from django import forms
from partosApp.models import RegistroParto


class AnestesiaAnalgesiaForm(forms.ModelForm):
    
    class Meta:
        model = RegistroParto
        fields = [
            'peridural',
            'tiempo_espera_peridural',
            'analgesia_endovenosa',
            'anestesia_general',
            'anestesia_raquidea',
        ]
        
        widgets = {
            'peridural': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiempo_espera_peridural': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'analgesia_endovenosa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'anestesia_general': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'anestesia_raquidea': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'peridural': 'Anestesia Peridural',
            'tiempo_espera_peridural': 'Tiempo de Espera Peridural (minutos)',
            'analgesia_endovenosa': 'Analgesia Endovenosa',
            'anestesia_general': 'Anestesia General',
            'anestesia_raquidea': 'Anestesia Raquídea',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tiempo_espera_peridural'].required = False
