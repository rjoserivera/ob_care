"""
matronaApp/forms/ficha_obstetrica_form.py
FORMULARIO CORREGIDO - Consultorio carga dinámicamente
"""

from django import forms
from django.utils import timezone
from ..models import FichaObstetrica, MedicamentoFicha, CatalogoConsultorioOrigen


class FichaObstetricaForm(forms.ModelForm):
    """
    Formulario para crear/editar Ficha Obstétrica
    - Consultorio se carga dinámicamente de la BD
    - Cálculos automáticos de edad gestacional y FPP
    """
    
    # Campos de cálculo
    edad_gestacional_semanas = forms.IntegerField(
        label='Semanas de Gestación (Calculadas)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control readonly-field',
            'readonly': 'readonly',
            'id': 'id_edad_gestacional_semanas'
        })
    )
    
    edad_gestacional_dias = forms.IntegerField(
        label='Días Adicionales (Calculados)',
        required=False,
        min_value=0,
        max_value=6,
        widget=forms.NumberInput(attrs={
            'class': 'form-control readonly-field',
            'readonly': 'readonly',
            'id': 'id_edad_gestacional_dias'
        })
    )
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'nombre_acompanante',
            'plan_de_parto',
            'visita_guiada',
            'imc',
            'consultorio_origen',
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'nacidos_vivos',
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'peso_actual',
            'talla_actual',
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_sistemia',
            'infeccion_ovular',
            'otras_patologias',
            'control_prenatal',
            'numero_controles',
        ]
        
        widgets = {
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del acompañante'
            }),
            'plan_de_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'visita_guiada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'imc': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'consultorio_origen': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_consultorio_origen'
            }),
            'numero_gestas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ej: 2'
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
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_fecha_ultima_regla'
            }),
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control readonly-field',
                'type': 'date',
                'readonly': 'readonly',
                'id': 'id_fecha_probable_parto'
            }),
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'kg'
            }),
            'talla_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'cm'
            }),
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
                'rows': '3',
                'placeholder': 'Describa otras patologías'
            }),
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'numero_controles': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """Inicializar el formulario con consultorios de la BD"""
        super().__init__(*args, **kwargs)
        
        # Cargar consultorios dinámicamente de la BD
        self.fields['consultorio_origen'].queryset = CatalogoConsultorioOrigen.objects.filter(activo=True).order_by('nombre')
        self.fields['consultorio_origen'].empty_label = '-- Seleccione un consultorio --'
    
    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        
        # Validar que numero_gestas >= numero_partos
        gestas = cleaned_data.get('numero_gestas')
        partos = cleaned_data.get('numero_partos')
        if gestas and partos and gestas < partos:
            self.add_error('numero_partos', 'El número de partos no puede ser mayor al número de gestaciones')
        
        # Validar que partos_vaginales + partos_cesareas == numero_partos
        vaginales = cleaned_data.get('partos_vaginales', 0)
        cesareas = cleaned_data.get('partos_cesareas', 0)
        if partos and (vaginales + cesareas) != partos:
            self.add_error('partos_vaginales', f'La suma de partos vaginales ({vaginales}) + cesáreas ({cesareas}) debe ser igual al total ({partos})')
        
        # Validar FUM
        fum = cleaned_data.get('fecha_ultima_regla')
        if fum:
            hoy = timezone.now().date()
            if fum > hoy:
                self.add_error('fecha_ultima_regla', 'La FUM no puede ser una fecha futura')
            
            dias_transcurridos = (hoy - fum).days
            if dias_transcurridos > 294:  # Más de 42 semanas
                self.add_error('fecha_ultima_regla', 'La FUM parece estar muy lejana (más de 42 semanas)')
        
        return cleaned_data


class MedicamentoFichaForm(forms.ModelForm):
    """
    Formulario para agregar medicamentos a una ficha obstétrica
    """
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
        ]
        widgets = {
            'medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Oxitocina, Misoprostol, etc.'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 10 mg'
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 6 horas, Una sola dosis, etc.'
            }),
        }