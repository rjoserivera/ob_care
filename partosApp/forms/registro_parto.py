"""
partosApp/forms/registro_parto.py
Formularios COMPLETOS para Registro de Partos (9 pasos)
"""

from django import forms
from ..models import RegistroParto


class RegistroPartoBaseForm(forms.ModelForm):
    """PASO 1: Información básica del parto"""
    class Meta:
        model = RegistroParto
        fields = ['fecha_hora_admision', 'edad_gestacional_semanas', 'edad_gestacional_dias']
        widgets = {
            'fecha_hora_admision': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'edad_gestacional_semanas': forms.NumberInput(attrs={'class': 'form-control', 'min': '20', 'max': '42'}),
            'edad_gestacional_dias': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '6'}),
        }


class RegistroPartoObstetricoForm(forms.ModelForm):
    """PASO 2: Datos obstétricos"""
    class Meta:
        model = RegistroParto
        fields = ['observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})}


class RegistroPartoAlubramientoForm(forms.ModelForm):
    """PASO 3: Alumbramiento"""
    class Meta:
        model = RegistroParto
        fields = ['observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})}


class RegistroPartoPerinealForm(forms.ModelForm):
    """PASO 4: Estado perineal"""
    class Meta:
        model = RegistroParto
        fields = ['observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})}


class RegistroPartoAnestesiaForm(forms.ModelForm):
    """PASO 5: Anestesia"""
    class Meta:
        model = RegistroParto
        fields = ['observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})}


class RegistroPartoApegoForm(forms.ModelForm):
    """PASO 6: Apego"""
    class Meta:
        model = RegistroParto
        fields = ['observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})}


class RegistroPartoProfesionalesForm(forms.ModelForm):
    """PASO 7: Profesionales"""
    class Meta:
        model = RegistroParto
        fields = ['observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})}


class RegistroPartoLeyDomingaForm(forms.ModelForm):
    """PASO 8: Ley Dominga"""
    class Meta:
        model = RegistroParto
        fields = ['observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})}


class RegistroPartoObservacionesForm(forms.ModelForm):
    """PASO 9: Observaciones"""
    class Meta:
        model = RegistroParto
        fields = ['observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})}


class RegistroPartoComplicacionesForm(forms.ModelForm):
    """Complicaciones"""
    class Meta:
        model = RegistroParto
        fields = ['observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})}