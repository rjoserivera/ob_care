"""
recienNacidoApp/forms/registro_rn.py
Formularios para Registro de Recién Nacido (9 PASOS)
COMPLETO: Todos los campos
"""

from django import forms
from ..models import RegistroRecienNacido, DocumentosParto


class RegistroRecienNacidoDatosForm(forms.ModelForm):
    """
    PASO 1: Datos básicos del recién nacido
    """
    
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'sexo',
            'peso_nacimiento',
            'talla_nacimiento',
            'perimetro_cefalico',
            'perimetro_toracico',
            'perimetro_abdominal',
            'hora_nacimiento',
        ]
        
        widgets = {
            'sexo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'peso_nacimiento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'gramos',
                'step': '10',
                'min': '0'
            }),
            'talla_nacimiento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'cm',
                'step': '0.1',
                'min': '0'
            }),
            'perimetro_cefalico': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'cm',
                'step': '0.1',
                'min': '0'
            }),
            'perimetro_toracico': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'cm',
                'step': '0.1',
                'min': '0'
            }),
            'perimetro_abdominal': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'cm',
                'step': '0.1',
                'min': '0'
            }),
            'hora_nacimiento': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
        }


class RegistroRecienNacidoApgarForm(forms.ModelForm):
    """
    PASO 2: Puntuación Apgar (1, 5 y 10 minutos)
    """
    
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'apgar_1_minuto',
            'apgar_5_minutos',
            'apgar_10_minutos',
            'observaciones_apgar',
        ]
        
        widgets = {
            'apgar_1_minuto': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10'
            }),
            'apgar_5_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10'
            }),
            'apgar_10_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10'
            }),
            'observaciones_apgar': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroRecienNacidoCordónForm(forms.ModelForm):
    """
    PASO 3: Cordón umbilical y ligadura tardía
    """
    
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'numero_vasos_cordon',
            'caracteristicas_cordon',
            'ligadura_cordon_tardia',
            'tiempo_ligadura_cordon',
            'ordene_cordon',
            'color_sangre_cordon_arterial',
            'color_sangre_cordon_venoso',
            'observaciones_cordon',
        ]
        
        widgets = {
            'numero_vasos_cordon': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'caracteristicas_cordon': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de características'
            }),
            'ligadura_cordon_tardia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tiempo_ligadura_cordon': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'segundos/minutos',
                'min': '0'
            }),
            'ordene_cordon': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'color_sangre_cordon_arterial': forms.Select(attrs={
                'class': 'form-select'
            }),
            'color_sangre_cordon_venoso': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observaciones_cordon': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }


class RegistroRecienNacidoApegoForm(forms.ModelForm):
    """
    PASO 4: APEGO - Piel con piel y contacto temprano ⭐
    """
    
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'piel_con_piel',
            'tiempo_piel_con_piel',
            'canguro_realizado',
            'tiempo_canguro',
            'madre_pudo_cargar',
            'primer_contacto_visual',
            'reconocimiento_rn',
            'observaciones_apego',
        ]
        
        widgets = {
            'piel_con_piel': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tiempo_piel_con_piel': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'minutos',
                'min': '0'
            }),
            'canguro_realizado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tiempo_canguro': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'minutos',
                'min': '0'
            }),
            'madre_pudo_cargar': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'primer_contacto_visual': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'reconocimiento_rn': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones sobre reconocimiento'
            }),
            'observaciones_apego': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroRecienNacidoAcompañamientoForm(forms.ModelForm):
    """
    PASO 5: ACOMPAÑAMIENTO - Familia presente ⭐
    """
    
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'madre_presente',
            'padre_presente',
            'otros_acompañantes',
            'acompañante_tipo',
            'acompañante_contacto_inicial',
            'lacatancia_primer_intento',
            'madre_lactancia_dificultad',
            'apoyo_lactancia',
            'observaciones_acompanamiento',
        ]
        
        widgets = {
            'madre_presente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'padre_presente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'otros_acompañantes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Otros acompañantes presentes'
            }),
            'acompañante_tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'acompañante_contacto_inicial': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'lacatancia_primer_intento': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'madre_lactancia_dificultad': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'apoyo_lactancia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Apoyo brindado para lactancia'
            }),
            'observaciones_acompanamiento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroRecienNacidoAlimentacionForm(forms.ModelForm):
    """
    PASO 6: Alimentación - Lactancia o fórmula
    """
    
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'tipo_alimentacion',
            'lactancia_materna',
            'formula_artficial',
            'alimentacion_mixta',
            'succion_efectiva',
            'frecuencia_alimentacion',
            'tolera_alimentacion',
            'problemas_alimentacion',
            'observaciones_alimentacion',
        ]
        
        widgets = {
            'tipo_alimentacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'lactancia_materna': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'formula_artficial': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'alimentacion_mixta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'succion_efectiva': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'frecuencia_alimentacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 3 horas'
            }),
            'tolera_alimentacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'problemas_alimentacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'observaciones_alimentacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroRecienNacidoEvaluacionesForm(forms.ModelForm):
    """
    PASO 7: Evaluaciones - Screening, examen físico, vacunas
    """
    
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'examen_fisico_realizado',
            'hallazgos_examen',
            'screening_congenito',
            'test_audicion',
            'screening_visual',
            'vacuna_bcg',
            'vacuna_hepatitis_b',
            'vitamina_k_administrada',
            'profilaxis_oftalmologica',
            'temperatura_actual',
            'frecuencia_cardiaca',
            'frecuencia_respiratoria',
            'observaciones_evaluacion',
        ]
        
        widgets = {
            'examen_fisico_realizado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hallazgos_examen': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Hallazgos del examen físico'
            }),
            'screening_congenito': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'test_audicion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'screening_visual': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vacuna_bcg': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vacuna_hepatitis_b': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vitamina_k_administrada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'profilaxis_oftalmologica': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'temperatura_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '°C',
                'step': '0.1'
            }),
            'frecuencia_cardiaca': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'lpm',
                'min': '0'
            }),
            'frecuencia_respiratoria': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'rpm',
                'min': '0'
            }),
            'observaciones_evaluacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class RegistroRecienNacidoComplicacionesForm(forms.ModelForm):
    """
    PASO 8: Complicaciones neonatales
    """
    
    class Meta:
        model = RegistroRecienNacido
        fields = [
            'complicaciones_presentes',
            'tipo_complicacion',
            'distres_respiratorio',
            'aspiracion_meconio',
            'hipoglucemia',
            'ictericia',
            'infeccion_neonatal',
            'malformaciones',
            'traumatismo_parto',
            'requerimiento_nicu',
            'motivo_nicu',
            'observaciones_complicaciones',
        ]
        
        widgets = {
            'complicaciones_presentes': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tipo_complicacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describir complicaciones'
            }),
            'distres_respiratorio': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'aspiracion_meconio': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hipoglucemia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'ictericia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'infeccion_neonatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'malformaciones': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'traumatismo_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'requerimiento_nicu': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'motivo_nicu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Motivo de ingreso a NICU'
            }),
            'observaciones_complicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class DocumentosPartoForm(forms.ModelForm):
    """
    PASO 9: Documentos del parto
    """
    
    class Meta:
        model = DocumentosParto
        fields = [
            'numero_folio_atencion',
            'numero_carne_maternidad',
            'numero_registro_civil',
            'certificado_nacimiento',
            'folio_partograma',
            'folio_historia_clinica',
            'documentos_completos',
            'observaciones_documentos',
        ]
        
        widgets = {
            'numero_folio_atencion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de folio'
            }),
            'numero_carne_maternidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de carné'
            }),
            'numero_registro_civil': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de registro civil'
            }),
            'certificado_nacimiento': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'folio_partograma': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'folio_historia_clinica': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'documentos_completos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observaciones_documentos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones sobre documentación'
            }),
        }
