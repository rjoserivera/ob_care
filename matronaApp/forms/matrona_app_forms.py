# matronaApp/forms/matrona_app_forms.py

from django import forms
from django.core.exceptions import ValidationError

from matronaApp.models import (
    FichaObstetrica,
    MedicamentoFicha,
    AdministracionMedicamento,
    CatalogoViaAdministracion,
)
from gestionApp.models import Paciente, Matrona, Tens


# ======================================================
# FORMULARIO FICHA OBSTÉTRICA
# ======================================================

class FichaObstetricaForm(forms.ModelForm):

    class Meta:
        model = FichaObstetrica
        fields = [
            'paciente',
            'matrona_responsable',
            'numero_ficha',
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
        ]

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'matrona_responsable': forms.Select(attrs={'class': 'form-select'}),

            'numero_ficha': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_acompanante': forms.TextInput(attrs={'class': 'form-control'}),

            'numero_gestas': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_partos': forms.NumberInput(attrs={'class': 'form-control'}),
            'partos_vaginales': forms.NumberInput(attrs={'class': 'form-control'}),
            'partos_cesareas': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_abortos': forms.NumberInput(attrs={'class': 'form-control'}),
            'nacidos_vivos': forms.NumberInput(attrs={'class': 'form-control'}),

            'fecha_ultima_regla': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_probable_parto': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

            'edad_gestacional_semanas': forms.NumberInput(attrs={'class': 'form-control'}),
            'edad_gestacional_dias': forms.NumberInput(attrs={'class': 'form-control'}),

            'peso_actual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_numero_ficha(self):
        numero = self.cleaned_data.get('numero_ficha')
        if FichaObstetrica.objects.filter(numero_ficha=numero).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este número de ficha ya está registrado.")
        return numero


# ======================================================
# FORMULARIO MEDICAMENTO EN FICHA
# ======================================================

class MedicamentoFichaForm(forms.ModelForm):

    via_administracion = forms.ModelChoiceField(
        queryset=CatalogoViaAdministracion.objects.filter(activo=True),
        empty_label="Seleccione vía",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Vía administración"
    )

    class Meta:
        model = MedicamentoFicha
        fields = [
            'ficha',
            'nombre_medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_termino',
            'observaciones',
        ]

        widgets = {
            'ficha': forms.Select(attrs={'class': 'form-select'}),

            'nombre_medicamento': forms.TextInput(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control'}),

            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_fecha_termino(self):
        inicio = self.cleaned_data.get('fecha_inicio')
        termino = self.cleaned_data.get('fecha_termino')

        if inicio and termino and termino < inicio:
            raise ValidationError("La fecha de término no puede ser menor que la fecha de inicio.")

        return termino


# ======================================================
# FORMULARIO ADMINISTRACIÓN DE MEDICAMENTO
# ======================================================

class AdministracionMedicamentoForm(forms.ModelForm):

    class Meta:
        model = AdministracionMedicamento
        fields = [
            'ficha',
            'medicamento_ficha',
            'tens',
            'fecha_hora_administracion',
            'dosis_administrada',
            'observaciones',
        ]

        widgets = {
            'ficha': forms.Select(attrs={'class': 'form-select'}),
            'medicamento_ficha': forms.Select(attrs={'class': 'form-select'}),
            'tens': forms.Select(attrs={'class': 'form-select'}),

            'fecha_hora_administracion': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),

            'dosis_administrada': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
