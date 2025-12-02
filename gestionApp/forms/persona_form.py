# gestionApp/forms/persona_form.py
"""
Formulario corregido para el modelo Persona
Compatible con nombres reales del modelo
"""

from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Sexo, Nacionalidad, PuebloOriginario


class PersonaForm(forms.ModelForm):

    class Meta:
        model = Persona
        fields = [
            'rut',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'fecha_nacimiento',
            'sexo',
            'nacionalidad',
            'pueblo_originario',
            'direccion',
            'telefono',
            'correo',
        ]

        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9',
                'maxlength': '12',
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre',
            }),
            'apellido_paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido paterno',
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido materno',
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-select'}),
            'pueblo_originario': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese dirección',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: +56912345678',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
            }),
        }

        labels = {
            'rut': 'RUT',
            'nombre': 'Nombre',
            'apellido_paterno': 'Apellido Paterno',
            'apellido_materno': 'Apellido Materno',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'sexo': 'Sexo',
            'nacionalidad': 'Nacionalidad',
            'pueblo_originario': 'Pueblo Originario',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'correo': 'Correo Electrónico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sexo'].queryset = Sexo.objects.filter(activo=True)
        self.fields['nacionalidad'].queryset = Nacionalidad.objects.filter(activo=True)
        self.fields['pueblo_originario'].queryset = PuebloOriginario.objects.filter(activo=True)

        self.fields['sexo'].empty_label = "Seleccione sexo"
        self.fields['nacionalidad'].empty_label = "Seleccione nacionalidad"
        self.fields['pueblo_originario'].empty_label = "Seleccione (opcional)"

    # --- Validaciones personalizadas ---
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            rut = rut.replace('.', '').upper().strip()

            if '-' not in rut:
                raise ValidationError('El RUT debe incluir guión. Ej: 12345678-9')

            existe = (
                Persona.objects.filter(rut=rut)
                .exclude(pk=self.instance.pk)
                .exists()
            )

            if existe:
                raise ValidationError('Ya existe una persona con este RUT.')

        return rut

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        return nombre.strip().title() if nombre else nombre

    def clean_apellido_paterno(self):
        apellido = self.cleaned_data.get('apellido_paterno')
        return apellido.strip().title() if apellido else apellido

    def clean_apellido_materno(self):
        apellido = self.cleaned_data.get('apellido_materno')
        return apellido.strip().title() if apellido else apellido

    def clean_correo(self):
        email = self.cleaned_data.get('correo')
        return email.lower().strip() if email else email
