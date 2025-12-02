from django import forms
from django.utils import timezone
from ingresoPartoApp.models import FichaParto
from matronaApp.models import FichaObstetrica


class FichaPartoCompletaForm(forms.ModelForm):
    
    class Meta:
        model = FichaParto
        fields = [
            'ficha_obstetrica',
            'tipo_paciente',
            'origen_ingreso',
            'fecha_ingreso',
            'hora_ingreso',
            'plan_de_parto',
            'visita_guiada',
            'control_prenatal',
            'consultorio_origen',
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_grave',
            'infeccion_ovular',
            'otra_patologia',
            'numero_aro',
            'vih_tomado_prepartos',
            'vih_tomado_sala',
            'vih_orden_toma',
            'sgb_pesquisa',
            'sgb_resultado',
            'antibiotico_sgb',
            'vdrl_resultado',
            'tratamiento_sifilis',
            'hepatitis_b_tomado',
            'derivacion_gastro',
            'activa'
        ]
        
        widgets = {
            'ficha_obstetrica': forms.Select(attrs={'class': 'form-select'}),
            'tipo_paciente': forms.Select(attrs={'class': 'form-select'}),
            'origen_ingreso': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_ingreso': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'plan_de_parto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'visita_guiada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'control_prenatal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'consultorio_origen': forms.TextInput(attrs={'class': 'form-control'}),
            'preeclampsia_severa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'eclampsia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sepsis_infeccion_grave': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'infeccion_ovular': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'otra_patologia': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_aro': forms.TextInput(attrs={'class': 'form-control'}),
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_tomado_sala': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_orden_toma': forms.Select(attrs={'class': 'form-select'}),
            'sgb_pesquisa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sgb_resultado': forms.Select(attrs={'class': 'form-select'}),
            'antibiotico_sgb': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vdrl_resultado': forms.Select(attrs={'class': 'form-select'}),
            'tratamiento_sifilis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'derivacion_gastro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['ficha_obstetrica'].queryset = FichaObstetrica.objects.filter(
            activa=True
        ).select_related('paciente__persona')
        
        campos_opcionales = [
            'consultorio_origen', 'otra_patologia', 'numero_aro',
            'vih_orden_toma', 'sgb_resultado', 'vdrl_resultado'
        ]
        
        for campo in campos_opcionales:
            if campo in self.fields:
                self.fields[campo].required = False
