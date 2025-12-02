"""
Formulario para Tratamiento Aplicado por TENS
tensApp/forms/tratamiento_aplicado_form.py
"""
from django import forms
from django.core.exceptions import ValidationError
from tensApp.models import Tratamiento_aplicado
from matronaApp.models import FichaObstetrica, MedicamentoFicha
from gestionApp.models import Paciente, Tens


class TratamientoAplicadoForm(forms.ModelForm):
    """
    Formulario para registro de tratamientos/medicamentos aplicados por TENS
    Incluye: medicamento, dosis, vía, procedimiento, observaciones
    """
    
    class Meta:
        model = Tratamiento_aplicado
        fields = [
            'ficha',
            'paciente',
            'tens',
            'medicamento_ficha',
            'nombre_medicamento',
            'dosis',
            'via_administracion',
            'fecha_aplicacion',
            'hora_aplicacion',
            'se_realizo_lavado_manos',
            'aplicado_exitosamente',
            'motivo_no_aplicacion',
            'observaciones',
            'reacciones_adversas',
        ]
        
        widgets = {
            # Relaciones
            'ficha': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'tens': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'medicamento_ficha': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # Datos del tratamiento
            'nombre_medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Paracetamol 500mg',
                'required': True
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg, 10ml, 2 comprimidos'
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_aplicacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'hora_aplicacion': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            
            # Procedimiento
            'se_realizo_lavado_manos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'aplicado_exitosamente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'motivo_no_aplicacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Completar solo si no se aplicó el tratamiento...'
            }),
            
            # Observaciones
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detalles adicionales sobre la aplicación...'
            }),
            'reacciones_adversas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Cualquier reacción adversa observada...'
            }),
        }
        
        labels = {
            'ficha': 'Ficha Obstétrica',
            'paciente': 'Paciente',
            'tens': 'TENS que Aplica',
            'medicamento_ficha': 'Medicamento de Ficha (Opcional)',
            'nombre_medicamento': 'Nombre del Medicamento/Tratamiento',
            'dosis': 'Dosis Aplicada',
            'via_administracion': 'Vía de Administración',
            'fecha_aplicacion': 'Fecha de Aplicación',
            'hora_aplicacion': 'Hora de Aplicación',
            'se_realizo_lavado_manos': '¿Se realizó lavado de manos?',
            'aplicado_exitosamente': '¿Se aplicó exitosamente?',
            'motivo_no_aplicacion': 'Motivo de NO Aplicación',
            'observaciones': 'Observaciones Generales',
            'reacciones_adversas': 'Reacciones Adversas',
        }
        
        help_texts = {
            'medicamento_ficha': 'Si aplica un medicamento prescrito en la ficha',
            'nombre_medicamento': 'Nombre completo del medicamento o tratamiento',
            'dosis': 'Cantidad exacta administrada',
            'via_administracion': 'Ruta de administración del medicamento',
            'motivo_no_aplicacion': 'Completar SOLO si NO se aplicó exitosamente',
            'reacciones_adversas': 'Efectos adversos o reacciones inesperadas',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar fichas activas
        self.fields['ficha'].queryset = FichaObstetrica.objects.filter(activa=True)
        
        # Filtrar pacientes activos
        self.fields['paciente'].queryset = Paciente.objects.filter(activo=True)
        
        # Filtrar TENS activos
        self.fields['tens'].queryset = Tens.objects.filter(Activo=True)
        
        # Filtrar medicamentos activos de fichas
        self.fields['medicamento_ficha'].queryset = MedicamentoFicha.objects.filter(activo=True)
        self.fields['medicamento_ficha'].required = False
    
    def clean_nombre_medicamento(self):
        """Validar nombre del medicamento"""
        nombre = self.cleaned_data.get('nombre_medicamento')
        
        if nombre:
            nombre = nombre.strip()
            if len(nombre) < 3:
                raise ValidationError('El nombre del medicamento es muy corto.')
        
        return nombre
    
    def clean_dosis(self):
        """Validar dosis"""
        dosis = self.cleaned_data.get('dosis')
        
        if dosis:
            dosis = dosis.strip()
        
        return dosis
    
    def clean(self):
        """Validaciones generales del formulario"""
        cleaned_data = super().clean()
        
        aplicado = cleaned_data.get('aplicado_exitosamente')
        motivo = cleaned_data.get('motivo_no_aplicacion')
        
        # Si no se aplicó, debe haber motivo
        if not aplicado and not motivo:
            self.add_error('motivo_no_aplicacion',
                'Debe indicar el motivo si el tratamiento NO se aplicó exitosamente.')
        
        # Si se aplicó, no debería haber motivo
        if aplicado and motivo:
            self.add_error('motivo_no_aplicacion',
                'No debe indicar motivo si el tratamiento se aplicó exitosamente.')
        
        # Validar que ficha y paciente coincidan
        ficha = cleaned_data.get('ficha')
        paciente = cleaned_data.get('paciente')
        
        if ficha and paciente:
            if ficha.paciente != paciente:
                self.add_error('paciente',
                    'El paciente seleccionado no corresponde a la ficha obstétrica.')
        
        return cleaned_data
