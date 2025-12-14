from django import forms
from partosApp.models import RegistroParto
from recienNacidoApp.models import RegistroRecienNacido

class RegistroPartoForm(forms.ModelForm):
    """Formulario para el Registro de Parto (Evento)"""
    # Campos que vienen como ID de usuario pero se guardan como texto
    profesional_responsable_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    tens_responsable_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = RegistroParto
        exclude = ['ficha_parto', 'responsable_atencion', 'fecha_registro']
        # Los campos datetime se manejarán con input type="datetime-local" o "time" y validación manual si es necesario
        
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 3}),
            'otras_complicaciones': forms.Textarea(attrs={'rows': 2}),
            'fecha_hora_esterilizacion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'hora_inicio_parto': forms.TimeInput(attrs={'type': 'time'}),
            'hora_termino_parto': forms.TimeInput(attrs={'type': 'time'}),
        }

class RegistroRecienNacidoForm(forms.ModelForm):
    """Formulario para el Registro de Recién Nacido"""
    # Campos de Staff (ID -> Texto)
    matrona_responsable_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    tens_responsable_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = RegistroRecienNacido
        exclude = ['parto', 'fecha_registro']
        
        widgets = {
            'hora_nacimiento': forms.TimeInput(attrs={'type': 'time'}),
            'otras_complicaciones': forms.Textarea(attrs={'rows': 2}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
            'complicaciones_seleccionadas': forms.CheckboxSelectMultiple(),
        }
