"""
matronaApp/forms/ficha_obstetrica_form.py
ACTUALIZADO: Con campo tipo_ingreso
"""

from django import forms
from ..models import (
    FichaObstetrica, 
    MedicamentoFicha, 
    CatalogoConsultorioOrigen, 
    CatalogoViaAdministracion,
    CatalogoMedicamento,
    CatalogoTipoPaciente,
    CatalogoDiscapacidad,
    CatalogoARO
)
from decimal import Decimal, ROUND_HALF_UP



class FichaObstetricaForm(forms.ModelForm):
    """Formulario para crear/editar Ficha Obstétrica"""
    
    class Meta:
        model = FichaObstetrica
        fields = [
            # ============================================
            # SECCIÓN 1: TIPO DE INGRESO Y PACIENTE
            # ============================================
            'tipo_ingreso',
            'tipo_paciente',
            'clasificacion_aro',
            'tiene_discapacidad',
            'discapacidad',
            
            # ============================================
            # SECCIÓN 2: ACOMPAÑANTE
            # ============================================
            'tiene_acompanante',
            'nombre_acompanante',
            'rut_acompanante',
            'parentesco_acompanante',
            'telefono_acompanante',
            
            # ============================================
            # SECCIÓN 3: CONTACTO DE EMERGENCIA
            # ============================================
            'nombre_contacto_emergencia',
            'telefono_emergencia',
            'parentesco_contacto_emergencia',
            
            # ============================================
            # SECCIÓN 4: DATOS GENERALES
            # ============================================
            'plan_de_parto',
            'visita_guiada',
            'consultorio_origen',
            
            # ============================================
            # SECCIÓN 5: MEDIDAS ANTROPOMÉTRICAS
            # ============================================
            'peso_actual',
            'talla_actual',
            'imc',
            
            # ============================================
            # SECCIÓN 6: HISTORIA OBSTÉTRICA
            # ============================================
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'nacidos_vivos',
            
            # ============================================
            # SECCIÓN 7: EMBARAZO ACTUAL
            # ============================================
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'cantidad_bebes',
            'control_prenatal',
            'numero_controles',
            
            # ============================================
            # SECCIÓN 8: EXÁMENES VIH
            # ============================================
            'vih_1_realizado',
            'vih_1_fecha',
            'vih_1_resultado',
            'vih_2_realizado',
            'vih_2_fecha',
            'vih_2_resultado',
            
            # ============================================
            # SECCIÓN 9: PATOLOGÍAS
            # ============================================
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_sistemia',
            'infeccion_ovular',
            'otras_patologias',
        ]
        
        widgets = {
            # ============================================
            # TIPO DE INGRESO (NUEVO - RadioSelect para mejor UX)
            # ============================================
            'tipo_ingreso': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'tipo_paciente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'clasificacion_aro': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tiene_discapacidad': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_tiene_discapacidad', # ID para control JS
                'onchange': 'toggleDiscapacidad()'
            }),
            'discapacidad': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_discapacidad_select'
            }),
            
            # ============================================
            # ACOMPAÑANTE
            # ============================================
            'tiene_acompanante': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_tiene_acompanante',
                'onchange': 'toggleAcompanante()'
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
                'placeholder': 'Ej: 65.5',
                'onchange': 'calcularIMC()'
            }),
            'talla_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '100',
                'max': '220',
                'placeholder': 'Ej: 165',
                'onchange': 'calcularIMC()'
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
            # VIH
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
                'rows': 3,
                'placeholder': 'Describa otras patologías si las hay...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Campos opcionales
        campos_opcionales = [
            'nombre_acompanante', 'rut_acompanante', 'parentesco_acompanante',
            'telefono_acompanante', 'nombre_contacto_emergencia', 
            'telefono_emergencia', 'parentesco_contacto_emergencia',
            'consultorio_origen', 'peso_actual', 'talla_actual', 'imc',
            'fecha_ultima_regla', 'fecha_probable_parto',
            'edad_gestacional_semanas', 'edad_gestacional_dias',
            'vih_1_fecha', 'vih_1_resultado', 'vih_2_fecha', 'vih_2_resultado',
            'fecha_ultima_regla', 'fecha_probable_parto',
            'edad_gestacional_semanas', 'edad_gestacional_dias',
            'vih_1_fecha', 'vih_1_resultado', 'vih_2_fecha', 'vih_2_resultado',
            'otras_patologias', 'tipo_paciente', 'discapacidad', 'clasificacion_aro',
        ]

        
        for campo in campos_opcionales:
            if campo in self.fields:
                self.fields[campo].required = False
        
        # Queryset para consultorio
        if 'consultorio_origen' in self.fields:
            try:
                self.fields['consultorio_origen'].queryset = CatalogoConsultorioOrigen.objects.filter(activo=True)
                self.fields['consultorio_origen'].empty_label = "Seleccione consultorio..."
            except:
                pass

        # Queryset para Clasificación ARO
        if 'clasificacion_aro' in self.fields:
            try:
                self.fields['clasificacion_aro'].queryset = CatalogoARO.objects.filter(activo=True)
                self.fields['clasificacion_aro'].empty_label = "Seleccione clasificación ARO..."
            except:
                pass
        
        # Queryset para Tipo Paciente
        if 'tipo_paciente' in self.fields:
            try:
                self.fields['tipo_paciente'].queryset = CatalogoTipoPaciente.objects.filter(activo=True)
                self.fields['tipo_paciente'].empty_label = "Seleccione Tipo de Paciente..."
            except:
                pass

        # Queryset para Discapacidad
        if 'discapacidad' in self.fields:
            try:
                self.fields['discapacidad'].queryset = CatalogoDiscapacidad.objects.filter(activo=True)
                self.fields['discapacidad'].empty_label = "Seleccione Discapacidad (Si aplica)..."
                self.fields['discapacidad'].required = False
            except:
                pass





    
    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        
        # Calcular IMC si hay peso y talla
        peso = cleaned_data.get('peso_actual')
        talla = cleaned_data.get('talla_actual')
        
        if peso and talla and talla > 0:
            try:
                # Usar Decimal para mantener precisión y evitar errores de validación
                talla_metros = Decimal(str(talla)) / Decimal('100')
                peso_decimal = Decimal(str(peso))
                # Calcular IMC
                imc = peso_decimal / (talla_metros ** 2)
                # Redondear explícitamente a 2 decimales (hacia arriba si es .5)
                cleaned_data['imc'] = imc.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            except Exception as e:
                # Fallback en caso de error de conversión (maniobra defensiva)
                pass
        
        # Validar datos del acompañante si viene con uno
        tiene_acompanante = cleaned_data.get('tiene_acompanante')
        if tiene_acompanante:
            if not cleaned_data.get('nombre_acompanante'):
                self.add_error('nombre_acompanante', 'Debe ingresar el nombre del acompañante')
        
        return cleaned_data


class MedicamentoFichaForm(forms.ModelForm):
    """Formulario para crear/editar Medicamentos en Ficha"""
    
    # Campo de búsqueda para autocompletar
    buscar_medicamento = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar medicamento...',
            'id': 'buscar_medicamento',
            'autocomplete': 'off'
        }),
        label='Buscar en catálogo'
    )
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'medicamento_catalogo',
            'medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'cantidad',
            'fecha_inicio',
            'fecha_termino',
            'indicaciones',
            'activo',
        ]
        
        widgets = {
            'medicamento_catalogo': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_medicamento_catalogo'
            }),
            'medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento (si no está en catálogo)'
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
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
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
                'rows': 2,
                'placeholder': 'Indicaciones especiales...'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Vías de administración
        if 'via_administracion' in self.fields:
            try:
                self.fields['via_administracion'].queryset = CatalogoViaAdministracion.objects.filter(activo=True)
                self.fields['via_administracion'].empty_label = "Seleccione vía..."
            except:
                pass
        
        # Medicamentos del catálogo
        if 'medicamento_catalogo' in self.fields:
            try:
                self.fields['medicamento_catalogo'].queryset = CatalogoMedicamento.objects.filter(activo=True)
                self.fields['medicamento_catalogo'].empty_label = "Seleccione del catálogo (opcional)..."
                self.fields['medicamento_catalogo'].required = False
            except:
                pass
        
        # Campos opcionales
        self.fields['fecha_termino'].required = False
        self.fields['indicaciones'].required = False
        self.fields['medicamento'].required = False  # Porque puede usar catálogo
    
    def clean(self):
        cleaned_data = super().clean()
        
        medicamento_catalogo = cleaned_data.get('medicamento_catalogo')
        medicamento_texto = cleaned_data.get('medicamento')
        
        # Debe tener al menos uno
        if not medicamento_catalogo and not medicamento_texto:
            raise forms.ValidationError(
                'Debe seleccionar un medicamento del catálogo o ingresar el nombre manualmente.'
            )
        
        # Si hay catálogo, copiar nombre al campo texto
        if medicamento_catalogo and not medicamento_texto:
            cleaned_data['medicamento'] = str(medicamento_catalogo)
        
        return cleaned_data
