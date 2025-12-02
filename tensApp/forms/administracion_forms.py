"""
Formularios para la aplicación TENS
Gestión de administración de medicamentos por TENS
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from matronaApp.models import AdministracionMedicamento, MedicamentoFicha
from gestionApp.models import Tens


class AdministracionMedicamentoForm(forms.ModelForm):
    """
    Formulario para registrar la administración de medicamentos por parte del TENS
    """
    
    class Meta:
        model = AdministracionMedicamento
        fields = [
            'medicamento_ficha',
            'tens',
            'fecha_hora_administracion',
            'se_realizo_lavado',
            'observaciones',
            'reacciones_adversas',
            'administrado_exitosamente',
            'motivo_no_administracion'
        ]
        
        widgets = {
            'medicamento_ficha': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'tens': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_hora_administracion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            'se_realizo_lavado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones sobre la administración del medicamento...'
            }),
            'reacciones_adversas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Registre cualquier reacción adversa observada...'
            }),
            'administrado_exitosamente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'motivo_no_administracion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Complete solo si NO se administró el medicamento...'
            })
        }
        
        labels = {
            'medicamento_ficha': 'Medicamento a Administrar',
            'tens': 'TENS Responsable',
            'fecha_hora_administracion': 'Fecha y Hora de Administración',
            'se_realizo_lavado': '¿Se realizó lavado de manos?',
            'observaciones': 'Observaciones',
            'reacciones_adversas': 'Reacciones Adversas',
            'administrado_exitosamente': '¿Se administró exitosamente?',
            'motivo_no_administracion': 'Motivo de No Administración'
        }
        
        help_texts = {
            'medicamento_ficha': 'Seleccione el medicamento a administrar',
            'tens': 'TENS que administrará el medicamento',
            'fecha_hora_administracion': 'Fecha y hora en que se administra',
            'se_realizo_lavado': 'Marque si se realizó el lavado de manos antes de administrar',
            'observaciones': 'Observaciones sobre el proceso de administración',
            'reacciones_adversas': 'Registre cualquier reacción adversa observada en la paciente',
            'administrado_exitosamente': 'Desmarque solo si NO se pudo administrar',
            'motivo_no_administracion': 'Complete este campo solo si el medicamento NO fue administrado'
        }
    
    def __init__(self, *args, **kwargs):
        """
        Personalizar el formulario al inicializarlo
        """
        # Extraer parámetros adicionales si se pasan
        medicamento_pk = kwargs.pop('medicamento_pk', None)
        ficha_pk = kwargs.pop('ficha_pk', None)
        
        super().__init__(*args, **kwargs)
        
        # Filtrar medicamentos activos
        self.fields['medicamento_ficha'].queryset = MedicamentoFicha.objects.filter(
            activo=True
        ).select_related('ficha__paciente__persona')
        
        # Si se especifica una ficha, filtrar solo medicamentos de esa ficha
        if ficha_pk:
            self.fields['medicamento_ficha'].queryset = self.fields['medicamento_ficha'].queryset.filter(
                ficha_id=ficha_pk
            )
        
        # Si se especifica un medicamento específico, establecerlo como inicial
        if medicamento_pk:
            try:
                medicamento = MedicamentoFicha.objects.get(pk=medicamento_pk, activo=True)
                self.fields['medicamento_ficha'].initial = medicamento
                # Opcionalmente, hacer que el campo sea de solo lectura
                self.fields['medicamento_ficha'].widget.attrs['readonly'] = True
            except MedicamentoFicha.DoesNotExist:
                pass
        
        # Filtrar TENS activos
        self.fields['tens'].queryset = Tens.objects.filter(
            Activo=True
        ).select_related('persona')
        
        # Establecer fecha y hora actual por defecto
        if not self.instance.pk:
            self.fields['fecha_hora_administracion'].initial = timezone.now()
            self.fields['administrado_exitosamente'].initial = True
            self.fields['se_realizo_lavado'].initial = True
    
    def clean(self):
        """
        Validaciones personalizadas del formulario
        """
        cleaned_data = super().clean()
        administrado = cleaned_data.get('administrado_exitosamente')
        motivo = cleaned_data.get('motivo_no_administracion')
        reacciones = cleaned_data.get('reacciones_adversas')
        
        # Si no se administró, el motivo es obligatorio
        if not administrado and not motivo:
            raise ValidationError({
                'motivo_no_administracion': 'Debe especificar el motivo por el cual no se administró el medicamento.'
            })
        
        # Si se administró, no debería haber motivo de no administración
        if administrado and motivo:
            raise ValidationError({
                'motivo_no_administracion': 'No debe especificar un motivo si el medicamento fue administrado exitosamente.'
            })
        
        # Advertencia si hay reacciones adversas pero se marca como exitoso
        if administrado and reacciones:
            # Esto no es un error, solo una advertencia en el sistema
            pass
        
        return cleaned_data
    
    def clean_fecha_hora_administracion(self):
        """
        Validar que la fecha de administración no sea futura
        """
        fecha_hora = self.cleaned_data.get('fecha_hora_administracion')
        
        if fecha_hora:
            ahora = timezone.now()
            # Permitir un pequeño margen de 5 minutos en el futuro (por diferencias de reloj)
            if fecha_hora > ahora + timezone.timedelta(minutes=5):
                raise ValidationError(
                    'La fecha y hora de administración no puede ser en el futuro.'
                )
        
        return fecha_hora


class BuscarMedicamentoPendienteForm(forms.Form):
    """
    Formulario para buscar medicamentos pendientes de administrar
    """
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre del medicamento, paciente o RUT...',
            'autocomplete': 'off'
        }),
        label='Buscar'
    )
    
    solo_pendientes = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Solo mostrar pendientes de hoy'
    )
