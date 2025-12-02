from django import forms


class BuscarPatologiaForm(forms.Form):
    
    busqueda = forms.CharField(
        max_length=200,
        required=False,
        label='Buscar Patología',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre o código CIE-10...',
            'id': 'buscar_patologia'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('Activo', 'Activas'),
            ('Inactivo', 'Inactivas')
        ],
        required=False,
        label='Estado',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    nivel_riesgo = forms.ChoiceField(
        choices=[
            ('', 'Todos los niveles'),
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
