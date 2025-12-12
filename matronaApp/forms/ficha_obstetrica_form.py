"""
matronaApp/forms/ficha_obstetrica_form.py
Formularios para Ficha Obstétrica y Medicamentos
ACTUALIZADO: Incluye TODOS los campos del modelo
"""

from django import forms
from ..models import FichaObstetrica, MedicamentoFicha, CatalogoConsultorioOrigen, CatalogoViaAdministracion


class FichaObstetricaForm(forms.ModelForm):
    """Formulario para crear/editar Ficha Obstétrica"""
    
    class Meta:
        model = FichaObstetrica
        fields = [
            # ============================================
            # SECCIÓN 1: ACOMPAÑANTE
            # ============================================
            'tiene_acompanante',
            'nombre_acompanante',
            'rut_acompanante',
            'parentesco_acompanante',
            'telefono_acompanante',
            
            # ============================================
            # SECCIÓN 2: CONTACTO DE EMERGENCIA
            # ============================================
            'nombre_contacto_emergencia',
            'telefono_emergencia',
            'parentesco_contacto_emergencia',
            
            # ============================================
            # SECCIÓN 3: DATOS GENERALES
            # ============================================
            'plan_de_parto',
            'visita_guiada',
            'consultorio_origen',
            
            # ============================================
            # SECCIÓN 4: MEDIDAS ANTROPOMÉTRICAS
            # ============================================
            'peso_actual',
            'talla_actual',
            'imc',
            
            # ============================================
            # SECCIÓN 5: HISTORIA OBSTÉTRICA
            # ============================================
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'nacidos_vivos',
            
            # ============================================
            # SECCIÓN 6: EMBARAZO ACTUAL
            # ============================================
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'cantidad_bebes',
            'control_prenatal',
            'numero_controles',
            
            # ============================================
            # SECCIÓN 7: EXÁMENES VIH
            # ============================================
            'vih_1_realizado',
            'vih_1_fecha',
            'vih_1_resultado',
            'vih_2_realizado',
            'vih_2_fecha',
            'vih_2_resultado',
            
            # ============================================
            # SECCIÓN 8: PATOLOGÍAS
            # ============================================
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_sistemia',
            'infeccion_ovular',
            'otras_patologias',
        ]
        
        widgets = {
            # ============================================
            # ACOMPAÑANTE
            # ============================================
            'tiene_acompanante': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_tiene_acompanante'
            }),
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del acompañante',
                'maxlength': '200'
            }),
            'rut_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9',
                'maxlength': '12'
            }),
            'parentesco_acompanante': forms.Select(attrs={
                'class': 'form-select'
            }),
            'telefono_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678',
                'maxlength': '20'
            }),
            
            # ============================================
            # CONTACTO DE EMERGENCIA
            # ============================================
            'nombre_contacto_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'maxlength': '200'
            }),
            'telefono_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678',
                'maxlength': '20'
            }),
            'parentesco_contacto_emergencia': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # ============================================
            # DATOS GENERALES
            # ============================================
            'plan_de_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'visita_guiada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'consultorio_origen': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # ============================================
            # MEDIDAS ANTROPOMÉTRICAS
            # ============================================
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '30',
                'max': '200',
                'placeholder': 'Ej: 65.5'
            }),
            'talla_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '100',
                'max': '220',
                'placeholder': 'Ej: 165'
            }),
            'imc': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'readonly': 'readonly',
                'style': 'background-color: #e8f5e9;'
            }),
            
            # ============================================
            # HISTORIA OBSTÉTRICA
            # ============================================
            'numero_gestas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '20'
            }),
            'numero_partos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'partos_vaginales': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'partos_cesareas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'numero_abortos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'nacidos_vivos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            
            # ============================================
            # EMBARAZO ACTUAL
            # ============================================
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'readonly': 'readonly',
                'style': 'background-color: #e8f5e9;'
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '45',
                'readonly': 'readonly',
                'style': 'background-color: #e8f5e9;'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6',
                'readonly': 'readonly',
                'style': 'background-color: #e8f5e9;'
            }),
            'cantidad_bebes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5'
            }),
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'numero_controles': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            
            # ============================================
            # EXÁMENES VIH
            # ============================================
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
            
            # ============================================
            # PATOLOGÍAS
            # ============================================
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
                'placeholder': 'Describa otras patologías si las hay...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ============================================
        # CAMPOS OPCIONALES
        # ============================================
        campos_opcionales = [
            'nombre_acompanante',
            'rut_acompanante',
            'parentesco_acompanante',
            'telefono_acompanante',
            'nombre_contacto_emergencia',
            'telefono_emergencia',
            'parentesco_contacto_emergencia',
            'consultorio_origen',
            'peso_actual',
            'talla_actual',
            'imc',
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'vih_1_fecha',
            'vih_1_resultado',
            'vih_2_fecha',
            'vih_2_resultado',
            'otras_patologias',
            'numero_controles',
        ]
        
        for campo in campos_opcionales:
            if campo in self.fields:
                self.fields[campo].required = False
        
        # ============================================
        # QUERYSET PARA CONSULTORIO
        # ============================================
        if 'consultorio_origen' in self.fields:
            try:
                self.fields['consultorio_origen'].queryset = CatalogoConsultorioOrigen.objects.filter(activo=True)
                self.fields['consultorio_origen'].empty_label = "Seleccione consultorio..."
            except:
                pass
    
    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        
        # Calcular IMC si hay peso y talla
        peso = cleaned_data.get('peso_actual')
        talla = cleaned_data.get('talla_actual')
        
        if peso and talla and talla > 0:
            talla_metros = float(talla) / 100
            imc = float(peso) / (talla_metros ** 2)
            cleaned_data['imc'] = round(imc, 2)
        
        # Validar que partos = partos_vaginales + partos_cesareas
        numero_partos = cleaned_data.get('numero_partos', 0) or 0
        partos_vaginales = cleaned_data.get('partos_vaginales', 0) or 0
        partos_cesareas = cleaned_data.get('partos_cesareas', 0) or 0
        
        if partos_vaginales + partos_cesareas != numero_partos:
            # Auto-corregir en lugar de error
            cleaned_data['numero_partos'] = partos_vaginales + partos_cesareas
        
        return cleaned_data


class MedicamentoFichaForm(forms.ModelForm):
    """Formulario para crear/editar Medicamentos en Ficha"""
    
    class Meta:
        model = MedicamentoFicha
        fields = [
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
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_termino': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '2',
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
        if 'via_administracion' in self.fields:
            try:
                self.fields['via_administracion'].queryset = CatalogoViaAdministracion.objects.filter(activo=True)
                self.fields['via_administracion'].empty_label = "Seleccione vía..."
            except:
                pass