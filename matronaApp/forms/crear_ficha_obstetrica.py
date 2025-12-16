# forms.py - Formularios para Ficha Obstétrica
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    FichaObstetrica, 
    RegistroDilatacion, 
    MedicamentoAsociado,
    Consultorio,
    Medicamento
)


class FichaObstetricaForm(forms.ModelForm):
    """Formulario principal para crear/editar ficha obstétrica"""
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'tipo_ingreso',
            'tipo_paciente',
            'clasificacion_aro',
            'tiene_discapacidad',
            'discapacidad',
            'tiene_acompanante',
            'nombre_acompanante',
            'rut_acompanante',
            'parentesco_acompanante',
            'telefono_acompanante',
            'nombre_contacto_emergencia',
            'telefono_emergencia',
            'parentesco_contacto_emergencia',
            'plan_de_parto',
            'visita_guiada',
            'consultorio_origen',
            'peso_actual',
            'talla_actual',
            'imc',
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
            'cantidad_bebes',
            'control_prenatal',
            'numero_controles',
            'vih_1_realizado',
            'vih_1_fecha',
            'vih_1_resultado',
            'vih_2_fecha',
            'vih_2_resultado',
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_sistemia',
            'infeccion_ovular',
            'otras_patologias',
            'dilatacion_inicial',
            'tipo_parto',
        ]

        widgets = {
            # Checkboxes
            'tiene_acompanante': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'tieneAcompanante'
            }),
            'plan_de_parto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'visita_guiada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'control_prenatal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'preeclampsia_severa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'eclampsia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sepsis_infeccion_sistemia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'infeccion_ovular': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Campos de texto
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del acompañante'
            }),
            'rut_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9'
            }),
            'telefono_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            }),
            'nombre_contacto_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'telefono_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            }),
            
            # Selects
            'parentesco_acompanante': forms.Select(attrs={'class': 'form-select'}),
            'parentesco_contacto_emergencia': forms.Select(attrs={'class': 'form-select'}),
            'consultorio_origen': forms.Select(attrs={'class': 'form-select'}),
            'vih_2_resultado': forms.Select(attrs={'class': 'form-select'}),
            'tipo_parto': forms.RadioSelect(),
            
            # Numéricos
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ej: 65.5'
            }),
            'talla_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ej: 165'
            }),
            'imc': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'readonly': True,
                'style': 'background-color: #e8f5e9;'
            }),
            'numero_gestas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
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
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'style': 'background-color: #e8f5e9;'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'style': 'background-color: #e8f5e9;'
            }),
            'cantidad_bebes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5'
            }),
            'numero_controles': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'dilatacion_inicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'placeholder': '0-10'
            }),
            
            # Fechas
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'readonly': True,
                'style': 'background-color: #e8f5e9;'
            }),
            'vih1_fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'vih2_fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            
            # Textarea
            'otras_patologias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa otras patologías si las hay...'
            }),
        }
    
    def clean(self):
        """Validaciones personalizadas"""
        cleaned_data = super().clean()
        
        # Validar datos del acompañante si viene con uno
        tiene_acompanante = cleaned_data.get('tiene_acompanante')
        if tiene_acompanante:
            if not cleaned_data.get('nombre_acompanante'):
                self.add_error('nombre_acompanante', 'Debe ingresar el nombre del acompañante')
            if not cleaned_data.get('rut_acompanante'):
                self.add_error('rut_acompanante', 'Debe ingresar el RUT del acompañante')
            if not cleaned_data.get('parentesco_acompanante'):
                self.add_error('parentesco_acompanante', 'Debe seleccionar el parentesco')
        
        # Validar coherencia en historia obstétrica
        partos_vaginales = cleaned_data.get('partos_vaginales', 0)
        partos_cesareas = cleaned_data.get('partos_cesareas', 0)
        numero_partos = cleaned_data.get('numero_partos', 0)
        
        if partos_vaginales + partos_cesareas > numero_partos:
            self.add_error('numero_partos', 
                'El número de partos debe ser igual o mayor a la suma de partos vaginales y cesáreas')
        
        # Validar cantidad de bebés
        cantidad_bebes = cleaned_data.get('cantidad_bebes', 1)
        if cantidad_bebes < 1 or cantidad_bebes > 5:
            self.add_error('cantidad_bebes', 'La cantidad de bebés debe ser entre 1 y 5')
        
        return cleaned_data
    
    def clean_rut_acompanante(self):
        """Valida el formato del RUT del acompañante"""
        rut = self.cleaned_data.get('rut_acompanante')
        if rut:
            # Limpiar el RUT
            rut = rut.replace('.', '').replace('-', '').upper()
            if len(rut) < 8 or len(rut) > 9:
                raise ValidationError('El RUT no tiene un formato válido')
            # Formatear: 12345678-9
            rut = f"{rut[:-1]}-{rut[-1]}"
        return rut


class RegistroDilatacionForm(forms.ModelForm):
    """Formulario para registrar dilatación cervical"""
    
    class Meta:
        model = RegistroDilatacion
        fields = ['valor_dilatacion', 'observacion']
        
        widgets = {
            'valor_dilatacion': forms.NumberInput(attrs={
                'class': 'dilatacion-input',
                'min': '1',
                'max': '10',
                'step': '1'
            }),
            'observacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Observación (opcional)',
                'style': 'width: 150px; display: inline-block;'
            }),
        }
    
    def clean_valor_dilatacion(self):
        valor = self.cleaned_data.get('valor_dilatacion')
        if valor < 1 or valor > 10:
            raise ValidationError('La dilatación debe estar entre 1 y 10 cm')
        return valor


class MedicamentoAsociadoForm(forms.ModelForm):
    """Formulario para asociar medicamentos a la ficha"""
    
    class Meta:
        model = MedicamentoAsociado
        fields = ['medicamento', 'cantidad', 'dosis', 'fecha_inicio', 'fecha_termino', 'observaciones']
        
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ej: 10'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg c/8hrs'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_termino': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales...'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_termino = cleaned_data.get('fecha_termino')
        
        if fecha_inicio and fecha_termino:
            if fecha_termino < fecha_inicio:
                self.add_error('fecha_termino', 'La fecha de término no puede ser anterior a la fecha de inicio')
        
        return cleaned_data


# Formset para múltiples medicamentos
MedicamentoFormSet = forms.inlineformset_factory(
    FichaObstetrica,
    MedicamentoAsociado,
    form=MedicamentoAsociadoForm,
    extra=1,
    can_delete=True
)

# Formset para múltiples registros de dilatación
DilatacionFormSet = forms.inlineformset_factory(
    FichaObstetrica,
    RegistroDilatacion,
    form=RegistroDilatacionForm,
    extra=0,
    can_delete=True
)


class IniciarPartoForm(forms.Form):
    """Formulario para validar e iniciar el proceso de parto"""
    
    tipo_parto = forms.ChoiceField(
        choices=FichaObstetrica.TIPO_PARTO_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'parto-option-input'}),
        required=True
    )
    confirmar = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Confirmo que deseo iniciar el proceso de parto'
    )
    
    def __init__(self, *args, ficha=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ficha = ficha
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_parto = cleaned_data.get('tipo_parto')
        
        if not self.ficha:
            raise ValidationError('No se encontró la ficha obstétrica')
        
        # Validar para parto vaginal
        if tipo_parto == 'VAGINAL':
            if not self.ficha.puede_parto_vaginal():
                raise ValidationError(
                    'No se puede iniciar parto vaginal. La dilatación debe ser de al menos 8 cm.'
                )
        
        # Validar para cesárea (puede ser por estancamiento o indicación médica)
        if tipo_parto == 'CESAREA':
            # La cesárea siempre está permitida cuando hay indicación
            pass
        
        return cleaned_data
