from django import forms
from partosApp.models import RegistroParto
from matronaApp.models import FichaObstetrica


class RegistroPartoCompletoForm(forms.ModelForm):
    
    class Meta:
        model = RegistroParto
        exclude = ['numero_registro', 'fecha_creacion', 'fecha_modificacion', 'activo', 'ficha_ingreso']
        
        widgets = {
            'ficha': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora_admision': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_hora_parto': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_tomado_sala': forms.Select(attrs={'class': 'form-select'}),
            'edad_gestacional_semanas': forms.NumberInput(attrs={'class': 'form-control'}),
            'edad_gestacional_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'monitor_ttc': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'induccion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aceleracion_correccion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numero_tactos_vaginales': forms.NumberInput(attrs={'class': 'form-control'}),
            'rotura_membrana': forms.Select(attrs={'class': 'form-select'}),
            'tiempo_membranas_rotas': forms.NumberInput(attrs={'class': 'form-control'}),
            'tiempo_dilatacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'tiempo_expulsivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'libertad_movimiento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_regimen': forms.Select(attrs={'class': 'form-select'}),
            'tipo_parto': forms.Select(attrs={'class': 'form-select'}),
            'alumbramiento_dirigido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'clasificacion_robson': forms.Select(attrs={'class': 'form-select'}),
            'posicion_materna_parto': forms.Select(attrs={'class': 'form-select'}),
            'contacto_piel_piel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lactancia_primera_hora': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'apego_precoz': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sangrado_postparto': forms.Select(attrs={'class': 'form-select'}),
            'hemorragia_postparto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'retencion_placentaria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'peridural': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiempo_espera_peridural': forms.NumberInput(attrs={'class': 'form-control'}),
            'analgesia_endovenosa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'anestesia_general': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'anestesia_raquidea': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profesional_responsable': forms.Select(attrs={'class': 'form-select'}),
            'alumno': forms.TextInput(attrs={'class': 'form-control'}),
            'causa_cesarea': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'uso_sala_saip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['ficha'].queryset = FichaObstetrica.objects.filter(
            activa=True
        ).select_related('paciente__persona')
        
        campos_opcionales = [
            'fecha_hora_parto', 'tiempo_membranas_rotas', 'tiempo_dilatacion',
            'tiempo_expulsivo', 'tiempo_espera_peridural', 'alumno',
            'causa_cesarea', 'observaciones', 'numero_tactos_vaginales'
        ]
        
        for campo in campos_opcionales:
            if campo in self.fields:
                self.fields[campo].required = False
