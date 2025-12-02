"""
Formularios para la aplicación Matrona
Gestión de ingresos de pacientes y fichas obstétricas
"""

from django import forms
from django.core.exceptions import ValidationError
from matronaApp.models import IngresoPaciente, FichaObstetrica, MedicamentoFicha
from gestionApp.models import Paciente, Matrona
from medicoApp.models import Patologias


# ============================================
# FORMULARIO: BUSCAR PACIENTE PARA FICHA
# ============================================

class BuscarPacienteFichaForm(forms.Form):
    """
    Formulario para buscar pacientes antes de crear una ficha obstétrica
    """
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por RUT, nombre o apellido...',
            'autocomplete': 'off'
        }),
        label='Buscar Paciente'
    )


# ============================================
# FORMULARIO: INGRESO DE PACIENTE
# ============================================

class IngresoPacienteForm(forms.ModelForm):
    """
    Formulario para registrar el ingreso de una paciente a la unidad obstétrica
    """
    
    class Meta:
        model = IngresoPaciente
        fields = [
            'paciente',
            'motivo_ingreso',
            'fecha_ingreso',
            'hora_ingreso',
            'edad_gestacional_semanas',
            'derivacion',
            'observaciones',
            'numero_ficha'
        ]
        
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'motivo_ingreso': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describa el motivo del ingreso...',
                'required': True
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'hora_ingreso': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 42,
                'placeholder': 'Semanas'
            }),
            'derivacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hospital o servicio que deriva (opcional)'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
            'numero_ficha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ING-001',
                'required': True
            })
        }
        
        labels = {
            'paciente': 'Paciente',
            'motivo_ingreso': 'Motivo de Ingreso',
            'fecha_ingreso': 'Fecha de Ingreso',
            'hora_ingreso': 'Hora de Ingreso',
            'edad_gestacional_semanas': 'Edad Gestacional (semanas)',
            'derivacion': 'Derivado desde',
            'observaciones': 'Observaciones',
            'numero_ficha': 'Número de Ficha'
        }
    
    def clean_numero_ficha(self):
        """Validar que el número de ficha sea único"""
        numero = self.cleaned_data.get('numero_ficha')
        if IngresoPaciente.objects.filter(numero_ficha=numero).exists():
            raise ValidationError('Este número de ficha ya existe. Por favor use otro.')
        return numero


# ============================================
# FORMULARIO: FICHA OBSTÉTRICA COMPLETA
# ============================================

class FichaObstetricaForm(forms.ModelForm):
    """
    Formulario completo para crear/editar una ficha obstétrica
    """
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'numero_ficha',
            'matrona_responsable',
            'nombre_acompanante',
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
            'talla',
            'patologias',
            'descripcion_patologias',
            'patologias_criticas',
            'vih_tomado',
            'vih_resultado',
            'vih_aro',
            'sgb_pesquisa',
            'sgb_resultado',
            'sgb_antibiotico',
            'vdrl_resultado',
            'vdrl_tratamiento_atb',
            'hepatitis_b_tomado',
            'hepatitis_b_resultado',
            'hepatitis_b_derivacion',
            'observaciones',
            'antecedentes_relevantes'
        ]
        
        widgets = {
            'numero_ficha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: FO-001',
                'required': True
            }),
            'matrona_responsable': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del acompañante'
            }),
            'numero_gestas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Número total de embarazos'
            }),
            'numero_partos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Número de partos previos'
            }),
            'partos_vaginales': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Número de partos vaginales'
            }),
            'partos_cesareas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Número de cesáreas'
            }),
            'numero_abortos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Número de abortos'
            }),
            'nacidos_vivos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Número de nacidos vivos'
            }),
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
                'min': 0,
                'max': 42,
                'placeholder': 'Semanas'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 6,
                'placeholder': 'Días'
            }),
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Kg'
            }),
            'talla': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Metros (ej: 1.65)'
            }),
            'patologias': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'descripcion_patologias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción de patologías detectadas...'
            }),
            'patologias_criticas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Patologías críticas a considerar'
            }),
            'vih_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vih_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vih_aro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Información ARO'
            }),
            'sgb_pesquisa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sgb_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'sgb_antibiotico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Antibiótico administrado'
            }),
            'vdrl_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vdrl_tratamiento_atb': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hepatitis_b_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'hepatitis_b_derivacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observaciones generales del embarazo...'
            }),
            'antecedentes_relevantes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Antecedentes médicos, alergias, cirugías previas...'
            })
        }


# ============================================
# FORMULARIO: FICHA OBSTÉTRICA SIMPLE
# ============================================

class FichaObstetricaSimpleForm(forms.ModelForm):
    """
    Formulario simplificado para crear fichas obstétricas rápidamente
    Solo incluye los campos más esenciales
    """
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'numero_ficha',
            'matrona_responsable',
            'nombre_acompanante',
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'observaciones'
        ]
        
        widgets = {
            'numero_ficha': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: FO-001'
            }),
            'matrona_responsable': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del acompañante (opcional)'
            }),
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
                'min': 0,
                'max': 42
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 6
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }


# ============================================
# FORMULARIO: MEDICAMENTO FICHA
# ============================================

class MedicamentoFichaForm(forms.ModelForm):
    """
    Formulario para agregar medicamentos a una ficha obstétrica
    """
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'nombre_medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_termino',
            'observaciones'
        ]
        
        widgets = {
            'nombre_medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento',
                'required': True
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg',
                'required': True
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 8 horas',
                'required': True
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'fecha_termino': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones sobre el medicamento...'
            })
        }


# ============================================
# FORMULARIO: ASIGNAR PATOLOGÍAS
# ============================================

class AsignarPatologiasFichaForm(forms.Form):
    """
    Formulario para asignar patologías a una ficha obstétrica
    """
    patologias = forms.ModelMultipleChoiceField(
        queryset=Patologias.objects.filter(estado='ACTIVA'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        label='Seleccionar Patologías'
    )
    
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Descripción adicional de las patologías...'
        }),
        required=False,
        label='Descripción'
    )


# ============================================
# FORMULARIO: BUSCAR PATOLOGÍA
# ============================================

class BuscarPatologiaForm(forms.Form):
    """
    Formulario para buscar patologías en el sistema
    """
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar patología por nombre o código...',
            'autocomplete': 'off'
        }),
        label='Buscar Patología'
    )
    
    tipo = forms.ChoiceField(
        choices=[
            ('', 'Todos los tipos'),
            ('CRONICA', 'Crónica'),
            ('AGUDA', 'Aguda'),
            ('GESTACIONAL', 'Gestacional')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Tipo de Patología'
    )


# ============================================
# FORMULARIO: EDICIÓN RÁPIDA DE FICHA
# ============================================

class FichaObstetricaEdicionRapidaForm(forms.ModelForm):
    """
    Formulario para edición rápida de campos críticos de la ficha
    """
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'peso_actual',
            'talla',
            'observaciones'
        ]
        
        widgets = {
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 42
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 6
            }),
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1'
            }),
            'talla': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            })
        }