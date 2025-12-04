"""
partosApp/forms/registro_parto.py
Formularios para Registro de Partos (9 PASOS)
CORREGIDO: Usando SOLO campos que existen en el modelo RegistroParto
"""

from django import forms
from ..models import RegistroParto


class RegistroPartoBaseForm(forms.ModelForm):
    """PASO 1: Informacion basica del parto"""
    class Meta:
        model = RegistroParto
        fields = [
            'fecha_hora_admision',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'tipo_parto',
        ]
        widgets = {
            'fecha_hora_admision': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '20',
                'max': '42'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6'
            }),
            'tipo_parto': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        semanas = cleaned_data.get('edad_gestacional_semanas')
        dias = cleaned_data.get('edad_gestacional_dias')
        if semanas and dias:
            if dias > 6:
                raise forms.ValidationError('Los dias no pueden ser mayores a 6')
        return cleaned_data


class RegistroPartoObstetricoForm(forms.ModelForm):
    """PASO 2: Datos obstetricos"""
    class Meta:
        model = RegistroParto
        fields = [
            'clasificacion_robson',
            'posicion_parto',
            'ofrecimiento_posiciones_alternativas',
            'alumbramiento_dirigido',
            'retira_placenta',
            'estampado_placenta',
        ]
        widgets = {
            'clasificacion_robson': forms.Select(attrs={'class': 'form-select'}),
            'posicion_parto': forms.Select(attrs={'class': 'form-select'}),
            'ofrecimiento_posiciones_alternativas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alumbramiento_dirigido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'retira_placenta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'estampado_placenta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RegistroPartoAlubramientoForm(forms.ModelForm):
    """PASO 3: Alumbramiento y Placenta"""
    class Meta:
        model = RegistroParto
        fields = [
            'revision_utero',
            'restos_placentarios',
            'observaciones',
        ]
        widgets = {
            'revision_utero': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'restos_placentarios': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones del alumbramiento'
            }),
        }


class RegistroPartoPerinealForm(forms.ModelForm):
    """PASO 4: Perine y Complicaciones"""
    class Meta:
        model = RegistroParto
        fields = [
            'estado_perine',
            'trauma',
            'hemorragia_postparto',
            'alteracion_coagulacion',
            'transfusion_sanguinea',
            'esterilizacion',
            'tipo_esterilizacion',
            'fecha_hora_esterilizacion',
        ]
        widgets = {
            'estado_perine': forms.Select(attrs={'class': 'form-select'}),
            'trauma': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hemorragia_postparto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alteracion_coagulacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'transfusion_sanguinea': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'esterilizacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_esterilizacion': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora_esterilizacion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }


class RegistroPartoAnestesiaForm(forms.ModelForm):
    """PASO 5: Anestesia y Analgesia"""
    class Meta:
        model = RegistroParto
        fields = [
            'anestesia_neuroaxial',
            'anestesia_general',
            'anestesia_local',
            'analgesia_no_farmacologica',
            'metodos_no_farmacologicos',
            'analgesia_endovenosa',
            'oxido_nitroso',
            'peridural_indicada_medico',
            'peridural_solicitada_paciente',
            'peridural_administrada',
            'tiempo_espera_peridural_minutos',
        ]
        widgets = {
            'anestesia_neuroaxial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'anestesia_general': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'anestesia_local': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'analgesia_no_farmacologica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'metodos_no_farmacologicos': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'analgesia_endovenosa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'oxido_nitroso': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'peridural_indicada_medico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'peridural_solicitada_paciente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'peridural_administrada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiempo_espera_peridural_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'minutos',
                'min': '0'
            }),
        }


class RegistroPartoApegoForm(forms.ModelForm):
    """PASO 6: Apego y Acompanamiento"""
    class Meta:
        model = RegistroParto
        fields = [
            'apego_canguro',
            'tiempo_apego_minutos',
            'ligadura_tardia_cordon',
            'acompanamiento_preparto',
            'acompanamiento_parto',
            'acompanamiento_rn',
            'acompanante_secciona_cordon',
            'persona_acompanante',
            'motivo_parto_no_acompanado',
        ]
        widgets = {
            'apego_canguro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiempo_apego_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'minutos',
                'min': '0'
            }),
            'ligadura_tardia_cordon': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acompanamiento_preparto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acompanamiento_parto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acompanamiento_rn': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acompanante_secciona_cordon': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'persona_acompanante': forms.Select(attrs={'class': 'form-select'}),
            'motivo_parto_no_acompanado': forms.Select(attrs={'class': 'form-select'}),
        }


class RegistroPartoProfesionalesForm(forms.ModelForm):
    """PASO 7: Profesionales intervinientes"""
    class Meta:
        model = RegistroParto
        fields = [
            'profesional_responsable_nombre',
            'profesional_responsable_apellido',
            'alumno_nombre',
            'alumno_apellido',
            'causa_cesarea',
        ]
        widgets = {
            'profesional_responsable_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'profesional_responsable_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'alumno_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del alumno'
            }),
            'alumno_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del alumno'
            }),
            'causa_cesarea': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Razon de la cesarea'
            }),
        }


class RegistroPartoLeyDomingaForm(forms.ModelForm):
    """PASO 8: Ley Dominga N 21.372"""
    class Meta:
        model = RegistroParto
        fields = [
            'ley_dominga_recuerdos',
            'ley_dominga_justificacion',
        ]
        widgets = {
            'ley_dominga_recuerdos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Cuales recuerdos se entregan'
            }),
            'ley_dominga_justificacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Si no se entregan, justificar'
            }),
        }


class RegistroPartoObservacionesForm(forms.ModelForm):
    """PASO 9: Observaciones finales"""
    class Meta:
        model = RegistroParto
        fields = [
            'inercia_uterina',
            'manejo_quirurgico_inercia',
            'histerectomia_obstetrica',
            'revision_utero',
            'uso_sala_saip',
            'observaciones',
        ]
        widgets = {
            'inercia_uterina': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'manejo_quirurgico_inercia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'histerectomia_obstetrica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'revision_utero': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'uso_sala_saip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Observaciones finales'
            }),
        }