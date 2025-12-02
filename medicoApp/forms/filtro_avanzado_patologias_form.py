from django import forms


class FiltroPatologiasForm(forms.Form):
    
    codigo_cie10 = forms.CharField(
        max_length=10,
        required=False,
        label='Código CIE-10',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: O14.1'
        })
    )
    
    nombre = forms.CharField(
        max_length=200,
        required=False,
        label='Nombre de la Patología',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre...'
        })
    )
    
    nivel_riesgo = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('Bajo', 'Bajo'),
            ('Medio', 'Medio'),
            ('Alto', 'Alto'),
            ('Crítico', 'Crítico')
        ],
        required=False,
        label='Nivel de Riesgo',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo')
        ],
        required=False,
        label='Estado',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    tiene_protocolo = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('si', 'Con Protocolo'),
            ('no', 'Sin Protocolo')
        ],
        required=False,
        label='Protocolo de Seguimiento',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    descripcion = forms.CharField(
        max_length=500,
        required=False,
        label='Buscar en Descripción',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Palabras clave en la descripción...'
        })
    )
