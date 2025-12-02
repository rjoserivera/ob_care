from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from ingresoPartoApp.models import FichaParto
from matronaApp.models import FichaObstetrica


class DatosGeneralesIngresoForm(forms.ModelForm):
    
    class Meta:
        model = FichaParto
        fields = [
            'ficha_obstetrica',
            'tipo_paciente',
            'origen_ingreso',
            'fecha_ingreso',
            'hora_ingreso',
            'plan_de_parto',
            'visita_guiada',
            'control_prenatal',
            'consultorio_origen'
        ]
        
        widgets = {
            'ficha_obstetrica': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo_paciente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'origen_ingreso': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hora_ingreso': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'plan_de_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_plan_de_parto'
            }),
            'visita_guiada': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_visita_guiada'
            }),
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_control_prenatal'
            }),
            'consultorio_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: CESFAM Los Volcanes'
            })
        }
        
        labels = {
            'ficha_obstetrica': 'Ficha Obstétrica',
            'tipo_paciente': 'Tipo de Paciente',
            'origen_ingreso': 'Origen del Ingreso',
            'fecha_ingreso': 'Fecha de Ingreso',
            'hora_ingreso': 'Hora de Ingreso',
            'plan_de_parto': '¿Tiene Plan de Parto?',
            'visita_guiada': '¿Realizó Visita Guiada?',
            'control_prenatal': '¿Tuvo Control Prenatal?',
            'consultorio_origen': 'Consultorio de Origen'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['ficha_obstetrica'].queryset = FichaObstetrica.objects.filter(
            activa=True
        ).select_related('paciente__persona')
        
        self.fields['consultorio_origen'].required = False
        
        if not self.instance.pk:
            self.fields['fecha_ingreso'].initial = timezone.now().date()
            self.fields['hora_ingreso'].initial = timezone.now().time()
    
    def clean_fecha_ingreso(self):
        fecha = self.cleaned_data.get('fecha_ingreso')
        
        if fecha and fecha > timezone.now().date():
            raise ValidationError('La fecha de ingreso no puede ser futura.')
        
        return fecha
    
    def clean(self):
        cleaned_data = super().clean()
        
        ficha = cleaned_data.get('ficha_obstetrica')
        
        if ficha:
            if FichaParto.objects.filter(ficha_obstetrica=ficha, activa=True).exists():
                if not self.instance.pk or self.instance.ficha_obstetrica != ficha:
                    raise ValidationError({
                        'ficha_obstetrica': 'Esta ficha obstétrica ya tiene un ingreso activo.'
                    })
        
        return cleaned_data
