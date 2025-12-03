# gestionApp/forms/persona_form.py
"""
Formulario corregido para el modelo Persona
Compatible con nombres reales del modelo
"""

from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import (
    CatalogoNacionalidad,
    CatalogoPuebloOriginario,
    CatalogoSexo,
    Persona,
)


class PersonaForm(forms.ModelForm):

    class Meta:
        model = Persona
        fields = [
            'Rut',
            'Nombre',
            'Apellido_Paterno',
            'Apellido_Materno',
            'Fecha_nacimiento',
            'Sexo',
            'Nacionalidad',
            'Pueblos_originarios',
            'Direccion',
            'Telefono',
            'Email',
        ]

        widgets = {
            'Rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9',
                'maxlength': '12',
            }),
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre',
            }),
            'Apellido_Paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido paterno',
            }),
            'Apellido_Materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido materno',
            }),
            'Fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'Sexo': forms.Select(attrs={'class': 'form-select'}),
            'Nacionalidad': forms.Select(attrs={'class': 'form-select'}),
            'Pueblos_originarios': forms.Select(attrs={'class': 'form-select'}),
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese dirección',
            }),
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: +56912345678',
            }),
            'Email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
            }),
        }

        labels = {
            'Rut': 'RUT',
            'Nombre': 'Nombre',
            'Apellido_Paterno': 'Apellido Paterno',
            'Apellido_Materno': 'Apellido Materno',
            'Fecha_nacimiento': 'Fecha de Nacimiento',
            'Sexo': 'Sexo',
            'Nacionalidad': 'Nacionalidad',
            'Pueblos_originarios': 'Pueblo Originario',
            'Direccion': 'Dirección',
            'Telefono': 'Teléfono',
            'Email': 'Correo Electrónico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['Sexo'].queryset = CatalogoSexo.objects.filter(activo=True)
        self.fields['Nacionalidad'].queryset = CatalogoNacionalidad.objects.filter(activo=True)
        self.fields['Pueblos_originarios'].queryset = CatalogoPuebloOriginario.objects.filter(activo=True)

        self.fields['Sexo'].empty_label = "Seleccione sexo"
        self.fields['Nacionalidad'].empty_label = "Seleccione nacionalidad"
        self.fields['Pueblos_originarios'].empty_label = "Seleccione (opcional)"

    # --- Validaciones ---
    def clean_Rut(self):
        rut = self.cleaned_data.get('Rut')
        if rut:
            rut = rut.replace('.', '').upper().strip()

            if '-' not in rut:
                raise ValidationError('El RUT debe incluir guión. Ej: 12345678-9')

            existe = (
                Persona.objects.filter(Rut=rut)
                .exclude(pk=self.instance.pk)
                .exists()
            )
            if existe:
                raise ValidationError('Ya existe una persona con este RUT.')

        return rut

    def clean_Nombre(self):
        nombre = self.cleaned_data.get('Nombre')
        return nombre.strip().title() if nombre else nombre

    def clean_Apellido_Paterno(self):
        apellido = self.cleaned_data.get('Apellido_Paterno')
        return apellido.strip().title() if apellido else apellido

    def clean_Apellido_Materno(self):
        apellido = self.cleaned_data.get('Apellido_Materno')
        return apellido.strip().title() if apellido else apellido

    def clean_Email(self):
        email = self.cleaned_data.get('Email')
        return email.lower().strip() if email else email
