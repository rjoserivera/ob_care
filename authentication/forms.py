from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    """
    Formulario de login personalizado con opción de "Recuérdame"
    """
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'id_remember_me'
        }),
        label='Recuérdame en este dispositivo'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario',
            'autofocus': True,
            'id': 'id_username'
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'id_password'
        })