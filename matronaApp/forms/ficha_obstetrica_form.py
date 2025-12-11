"""
matronaApp/forms/ficha_obstetrica_form.py
Formularios para Ficha Obstétrica y Medicamentos
"""

from django import forms
from ..models import FichaObstetrica, MedicamentoFicha, CatalogoConsultorioOrigen, CatalogoViaAdministracion


class FichaObstetricaForm(forms.ModelForm):
    """Formulario para crear/editar Ficha Obstétrica"""
    
    class Meta:
        model = FichaObstetrica
        fields = [
            # Identificación
            'numero_ficha',
            'paciente',
            'matrona_responsable',
            
            # Datos generales
            'plan_de_parto',
            'visita_guiada',
            'imc',
            
            # Acompañante
            'tiene_acompanante',
            'nombre_acompanante',
            'rut_acompanante',
            
            # Exámenes VIH
            'vih_1_realizado',
            'vih_1_fecha',
            'vih_1_resultado',
            'vih_2_realizado',
            'vih_2_fecha',
            'vih_2_resultado',
            
            # Cantidad de bebés
            'cantidad_bebes',
            
            # Consultorio
            'consultorio_origen',
            
            # Historia obstétrica
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'nacidos_vivos',
            
            # Embarazo actual
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'peso_actual',
            'talla_actual',
            
            # Patologías
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_sistemia',
            'infeccion_ovular',
            'otras_patologias',
            
            # Control prenatal
            'control_prenatal',
            'numero_controles',
            
            # Estado
            'activa',
        ]
        
        widgets = {
            'numero_ficha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: FO-2025-001'
            }),
            'paciente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'matrona_responsable': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # Datos generales
            'plan_de_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'visita_guiada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'imc': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ej: 25.50'
            }),
            
            # Acompañante
            'tiene_acompanante': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'tiene_acompanante'
            }),
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del acompañante'
            }),
            'rut_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9'
            }),
            
            # VIH 1
            'vih_1_realizado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vih_1_fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'vih_1_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # VIH 2
            'vih_2_realizado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vih_2_fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'vih_2_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # Cantidad de bebés
            'cantidad_bebes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10'
            }),
            
            # Consultorio
            'consultorio_origen': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # Historia obstétrica
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
            
            # Embarazo actual
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '45',
                'placeholder': 'Semanas'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6',
                'placeholder': 'Días'
            }),
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Kg'
            }),
            'talla_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'cm'
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
            
            # Control prenatal
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'numero_controles': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            
            # Estado
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Campos opcionales
        self.fields['matrona_responsable'].required = False
        self.fields['consultorio_origen'].required = False
        self.fields['nombre_acompanante'].required = False
        self.fields['rut_acompanante'].required = False
        
        # Queryset para consultorio
        self.fields['consultorio_origen'].queryset = CatalogoConsultorioOrigen.objects.filter(activo=True)


class MedicamentoFichaForm(forms.ModelForm):
    """Formulario para crear/editar Medicamentos en Ficha"""
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'ficha',
            'medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_termino',
            'indicaciones',
            'activo',
        ]
        
        widgets = {
            'ficha': forms.Select(attrs={
                'class': 'form-select'
            }),
            'medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg, 10ml, etc.'
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 8 horas'
            }),
            'fecha_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_termino': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indicaciones especiales...'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Campos opcionales
        self.fields['fecha_termino'].required = False
        self.fields['indicaciones'].required = False
        
        # Queryset para vía de administración
        self.fields['via_administracion'].queryset = CatalogoViaAdministracion.objects.filter(activo=True)