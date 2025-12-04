"""
partosApp/forms/registro_parto.py
Formularios para Registro de Partos (9 PASOS)
COMPLETO: Todos los campos y validaciones necesarias
"""

from django import forms
from django.db.models import Q
from ..models import RegistroParto


class RegistroPartoBaseForm(forms.ModelForm):
    """
    PASO 1: Información básica del parto
    """
    
    class Meta:
        model = RegistroParto
        fields = [
            'fecha_ingreso',
            'hora_ingreso',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'tipo_parto',
        ]
        
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hora_ingreso': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
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
                raise forms.ValidationError('Los días no pueden ser mayores a 6')
        
        return cleaned_data


class RegistroPartoObstetricoForm(forms.ModelForm):
    """
    PASO 2: Datos obstétricos
    """
    
    class Meta:
        model = RegistroParto
        fields = [
            'clasificacion_robson',
            'posicion_materna',
            'dinamica_uterina',
            'rotura_prematura_bolsa',
            'tiempo_ruptura',
            'color_liquido_amniotico',
            'meconial',
        ]
        
        widgets = {
            'clasificacion_robson': forms.Select(attrs={
                'class': 'form-select'
            }),
            'posicion_materna': forms.Select(attrs={
                'class': 'form-select'
            }),
            'dinamica_uterina': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de dinámica uterina'
            }),
            'rotura_prematura_bolsa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tiempo_ruptura': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'color_liquido_amniotico': forms.Select(attrs={
                'class': 'form-select'
            }),
            'meconial': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class RegistroPartoAlubramientoForm(forms.ModelForm):
    """
    PASO 3: Alumbramiento y Placenta
    """
    
    class Meta:
        model = RegistroParto
        fields = [
            'mecanismo_alumbramiento',
            'tiempo_alumbramiento',
            'peso_placenta',
            'condicion_placenta',
            'cordon_completo',
            'numero_vasos_cordon',
            'placenta_retenida',
            'complicaciones_alumbramiento',
            'observaciones_placenta',
        ]
        
        widgets = {
            'mecanismo_alumbramiento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tiempo_alumbramiento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutos',
                'min': '0'
            }),
            'peso_placenta': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'gramos',
                'step': '10'
            }),
            'condicion_placenta': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cordon_completo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'numero_vasos_cordon': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'placenta_retenida': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'complicaciones_alumbramiento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'observaciones_placenta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroPartoPerinealForm(forms.ModelForm):
    """
    PASO 4: Periné, Complicaciones y Esterilización
    """
    
    class Meta:
        model = RegistroParto
        fields = [
            'integridad_perineal',
            'grado_desgarro',
            'desgarros_vaginales',
            'desgarros_cervicales',
            'episiotomia',
            'tipo_episiotomia',
            'hemorragia_mayor_500ml',
            'volumen_sangrado',
            'complicacion_materna',
            'tipo_complicacion_materna',
            'esterilizacion_realizada',
            'tipo_esterilizacion',
            'deseo_esterilizacion',
            'observaciones_perineal',
        ]
        
        widgets = {
            'integridad_perineal': forms.Select(attrs={
                'class': 'form-select'
            }),
            'grado_desgarro': forms.Select(attrs={
                'class': 'form-select'
            }),
            'desgarros_vaginales': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'desgarros_cervicales': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'episiotomia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tipo_episiotomia': forms.Select(attrs={
                'class': 'form-select'
            }),
            'hemorragia_mayor_500ml': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'volumen_sangrado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ml',
                'min': '0'
            }),
            'complicacion_materna': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tipo_complicacion_materna': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'esterilizacion_realizada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tipo_esterilizacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'deseo_esterilizacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observaciones_perineal': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroPartoAnestesiaForm(forms.ModelForm):
    """
    PASO 5: ANESTESIA Y ANALGESIA - COMPLETO ⭐
    Incluye todas las opciones
    """
    
    class Meta:
        model = RegistroParto
        fields = [
            # Anestesia Neuroaxial
            'anestesia_neuroaxial',
            'raquianestesia',
            'epidural',
            'bloqueo_pudendo',
            
            # Anestesia General
            'anestesia_general',
            'induccion_anestesia_general',
            'intubacion_dificil',
            
            # Anestesia Local
            'anestesia_local',
            'tipo_anestesia_local',
            
            # Analgesia No Farmacológica
            'analgesia_no_farmacologica',
            'tipo_analgesia_no_farmacologica',
            
            # Analgesia Endovenosa
            'analgesia_endovenosa',
            'tipo_medicamento_endovenoso',
            
            # Óxido Nitroso
            'oxido_nitroso',
            
            # Peridural
            'peridural',
            'momento_peridural',
            
            # Observaciones
            'complicaciones_anestesia',
            'observaciones_anestesia',
        ]
        
        widgets = {
            'anestesia_neuroaxial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'raquianestesia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'epidural': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bloqueo_pudendo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'anestesia_general': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'induccion_anestesia_general': forms.Select(attrs={'class': 'form-select'}),
            'intubacion_dificil': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'anestesia_local': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_anestesia_local': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especificar tipo'
            }),
            
            'analgesia_no_farmacologica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_analgesia_no_farmacologica': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            
            'analgesia_endovenosa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_medicamento_endovenoso': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especificar medicamento'
            }),
            
            'oxido_nitroso': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'peridural': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'momento_peridural': forms.Select(attrs={'class': 'form-select'}),
            
            'complicaciones_anestesia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describir complicaciones'
            }),
            'observaciones_anestesia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones generales'
            }),
        }


class RegistroPartoApegoForm(forms.ModelForm):
    """
    PASO 6: APEGO Y ACOMPAÑAMIENTO - COMPLETO ⭐
    """
    
    class Meta:
        model = RegistroParto
        fields = [
            # Apego
            'apego_inmediato',
            'tiempo_primer_apego',
            'piel_con_piel',
            'tiempo_piel_con_piel',
            'canguro_inmediato',
            'tiempo_canguro',
            'lactancia_primera_hora',
            'ligadura_cordon_tardia',
            'tiempo_ligadura_cordon',
            
            # Acompañamiento
            'acompañante_presente',
            'tipo_acompañante',
            'acompañante_durante_trabajo_parto',
            'acompañante_durante_parto',
            'acompañante_contacto_rn',
            
            # Observaciones
            'observaciones_apego',
        ]
        
        widgets = {
            'apego_inmediato': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiempo_primer_apego': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'piel_con_piel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiempo_piel_con_piel': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'minutos',
                'min': '0'
            }),
            'canguro_inmediato': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiempo_canguro': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'minutos',
                'min': '0'
            }),
            'lactancia_primera_hora': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ligadura_cordon_tardia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiempo_ligadura_cordon': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'segundos/minutos',
                'min': '0'
            }),
            
            'acompañante_presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo_acompañante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Madre, padre, otro familiar, etc.'
            }),
            'acompañante_durante_trabajo_parto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acompañante_durante_parto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acompañante_contacto_rn': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'observaciones_apego': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroPartoProfesionalesForm(forms.ModelForm):
    """
    PASO 7: Profesionales intervinientes y causas
    """
    
    class Meta:
        model = RegistroParto
        fields = [
            'matrona_responsable',
            'obstetra_presente',
            'neonatologia_presente',
            'otros_profesionales',
            'indice_cardiotocografico',
            'causa_intervencion_obstetrica',
            'episiotomia_razon',
            'cesarea_razon',
            'forceps_razon',
            'vacio_razon',
            'observaciones_profesionales',
        ]
        
        widgets = {
            'matrona_responsable': forms.Select(attrs={
                'class': 'form-select'
            }),
            'obstetra_presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'neonatologia_presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'otros_profesionales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Otros profesionales presentes'
            }),
            'indice_cardiotocografico': forms.Select(attrs={
                'class': 'form-select'
            }),
            'causa_intervencion_obstetrica': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'episiotomia_razon': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'cesarea_razon': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'forceps_razon': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'vacio_razon': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'observaciones_profesionales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroPartoLeyDomingaForm(forms.ModelForm):
    """
    PASO 8: Ley Dominga N° 21.372
    Derechos sexuales y reproductivos en parto
    """
    
    class Meta:
        model = RegistroParto
        fields = [
            'informacion_consentimiento',
            'privacidad_dignidad',
            'acompañante_derecho',
            'libertad_movimiento',
            'libertad_posicion',
            'libertad_beber_comer',
            'contacto_rn',
            'lactancia_facilitada',
            'trato_respetuoso',
            'ausencia_violencia_obstetrica',
            'reclamos_sugerencias',
            'observaciones_ley_dominga',
        ]
        
        widgets = {
            'informacion_consentimiento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacidad_dignidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acompañante_derecho': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'libertad_movimiento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'libertad_posicion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'libertad_beber_comer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contacto_rn': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lactancia_facilitada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'trato_respetuoso': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ausencia_violencia_obstetrica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reclamos_sugerencias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Reclamos o sugerencias'
            }),
            'observaciones_ley_dominga': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroPartoObservacionesForm(forms.ModelForm):
    """
    PASO 9: Observaciones finales
    """
    
    class Meta:
        model = RegistroParto
        fields = [
            'observaciones_generales',
            'incidentes_adversos',
            'notificacion_eventos_adversos',
            'institucion_referencia',
            'razon_referencia',
        ]
        
        widgets = {
            'observaciones_generales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Observaciones generales del parto'
            }),
            'incidentes_adversos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notificacion_eventos_adversos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describir eventos adversos'
            }),
            'institucion_referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Institución si fue referenciada'
            }),
            'razon_referencia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Razón de la referencia'
            }),
        }
