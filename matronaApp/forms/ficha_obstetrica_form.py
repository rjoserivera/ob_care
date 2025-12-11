"""
matronaApp/forms/ficha_obstetrica_form.py
FORMULARIO ACTUALIZADO - Con campos de acompañante, VIH y cantidad de bebés
"""

from django import forms
from django.utils import timezone
from ..models import FichaObstetrica, CatalogoConsultorioOrigen


class FichaObstetricaForm(forms.ModelForm):
    """
    Formulario para crear/editar Ficha Obstétrica
    ACTUALIZADO con nuevos campos
    """
    
    class Meta:
        model = FichaObstetrica
        fields = [
            # Acompañante
            'tiene_acompanante',
            'nombre_acompanante',
            'rut_acompanante',
            
            # Datos Generales
            'plan_de_parto',
            'visita_guiada',
            'imc',
            'consultorio_origen',
            
            # Historia Obstétrica
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'nacidos_vivos',
            
            # Embarazo Actual
            'cantidad_bebes',
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'peso_actual',
            'talla_actual',
            
            # Exámenes VIH
            'vih_1_realizado',
            'vih_1_fecha',
            'vih_1_resultado',
            'vih_2_realizado',
            'vih_2_fecha',
            'vih_2_resultado',
            
            # Patologías
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_sistemia',
            'infeccion_ovular',
            'otras_patologias',
            
            # Control Prenatal
            'control_prenatal',
            'numero_controles',
        ]
        
        widgets = {
            # Acompañante
            'tiene_acompanante': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_tiene_acompanante',
                'onchange': 'toggleAcompanante()'
            }),
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del acompañante'
            }),
            'rut_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9'
            }),
            
            # Datos Generales
            'plan_de_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'visita_guiada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'imc': forms.NumberInput(attrs={
                'class': 'form-control readonly-field',
                'readonly': 'readonly',
                'step': '0.01'
            }),
            'consultorio_origen': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # Historia Obstétrica
            'numero_gestas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'numero_partos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'partos_vaginales': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'partos_cesareas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'numero_abortos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'nacidos_vivos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            
            # Embarazo Actual
            'cantidad_bebes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5'
            }),
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control readonly-field',
                'type': 'date',
                'readonly': 'readonly'
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control readonly-field',
                'readonly': 'readonly'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control readonly-field',
                'readonly': 'readonly'
            }),
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Kg'
            }),
            'talla_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'metros (ej: 1.65)'
            }),
            
            # Exámenes VIH
            'vih_1_realizado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'onchange': 'toggleVIH1()'
            }),
            'vih_1_fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'vih_1_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vih_2_realizado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'onchange': 'toggleVIH2()'
            }),
            'vih_2_fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'vih_2_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # Patologías
            'preeclampsia_severa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'eclampsia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sepsis_infeccion_sistemia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'infeccion_ovular': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'otras_patologias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa otras patologías si las hay...'
            }),
            
            # Control Prenatal
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'numero_controles': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar consultorios desde la BD
        self.fields['consultorio_origen'].queryset = CatalogoConsultorioOrigen.objects.filter(activo=True)
        self.fields['consultorio_origen'].empty_label = "Seleccione consultorio..."
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar acompañante
        tiene_acompanante = cleaned_data.get('tiene_acompanante')
        nombre_acompanante = cleaned_data.get('nombre_acompanante')
        rut_acompanante = cleaned_data.get('rut_acompanante')
        
        if tiene_acompanante:
            if not nombre_acompanante:
                self.add_error('nombre_acompanante', 'Debe ingresar el nombre del acompañante')
            if not rut_acompanante:
                self.add_error('rut_acompanante', 'Debe ingresar el RUT del acompañante')
        
        # Validar VIH 1
        vih_1_realizado = cleaned_data.get('vih_1_realizado')
        if vih_1_realizado:
            if not cleaned_data.get('vih_1_fecha'):
                self.add_error('vih_1_fecha', 'Debe ingresar la fecha del examen VIH 1')
            if not cleaned_data.get('vih_1_resultado'):
                self.add_error('vih_1_resultado', 'Debe seleccionar el resultado del VIH 1')
        
        # Validar VIH 2
        vih_2_realizado = cleaned_data.get('vih_2_realizado')
        if vih_2_realizado:
            if not cleaned_data.get('vih_2_fecha'):
                self.add_error('vih_2_fecha', 'Debe ingresar la fecha del examen VIH 2')
            if not cleaned_data.get('vih_2_resultado'):
                self.add_error('vih_2_resultado', 'Debe seleccionar el resultado del VIH 2')
        
        return cleaned_data