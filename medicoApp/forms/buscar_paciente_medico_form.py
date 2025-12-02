from django import forms


class BuscarPacienteMedicoForm(forms.Form):
    
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por RUT, nombre o apellido...',
            'id': 'buscar_paciente',
            'autofocus': True
        }),
        label='Buscar Paciente'
    )
