"""
gestionApp/forms/persona_form.py
Formulario para registrar/editar Persona
Con catálogos dinámicos de la base de datos
"""

from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import (
    Persona,
    CatalogoSexo,
    CatalogoNacionalidad,
    CatalogoPuebloOriginario,
)


class PersonaForm(forms.ModelForm):
    """
    Formulario para registrar/editar una Persona
    Los catálogos se cargan dinámicamente de la BD
    """
    
    # Campos explícitos para los catálogos
    Sexo = forms.ModelChoiceField(
        queryset=CatalogoSexo.objects.filter(activo=True).order_by('orden', 'nombre'),
        empty_label="-- Seleccione Sexo --",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Sexo"
    )
    
    Nacionalidad = forms.ModelChoiceField(
        queryset=CatalogoNacionalidad.objects.filter(activo=True).order_by('orden', 'nombre'),
        empty_label="-- Seleccione Nacionalidad --",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Nacionalidad"
    )
    
    Pueblos_originarios = forms.ModelChoiceField(
        queryset=CatalogoPuebloOriginario.objects.filter(activo=True).order_by('orden', 'nombre'),
        empty_label="-- Seleccione Pueblo Originario --",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Pueblos Originarios"
    )
    
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
            'Telefono',
            'Direccion',
            'Inmigrante',
            'Discapacidad',
            'Tipo_de_Discapacidad',
            'Privada_de_Libertad',
            'Trans_Masculino',
        ]
        
        widgets = {
            # Identificación
            'Rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9',
                'pattern': '[0-9]{7,8}-[0-9Kk]',
            }),
            
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la persona',
            }),
            
            'Apellido_Paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido paterno',
            }),
            
            'Apellido_Materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido materno',
            }),
            
            # Datos básicos
            'Fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            
            # Contacto
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678',
                'type': 'tel',
            }),
            
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa',
            }),
            
            # Tipo de Discapacidad
            'Tipo_de_Discapacidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especifique el tipo de discapacidad',
            }),
            
            # Checkboxes
            'Inmigrante': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'Discapacidad': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'Privada_de_Libertad': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
            'Trans_Masculino': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
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
            'Pueblos_originarios': 'Pueblos Originarios',
            'Telefono': 'Teléfono',
            'Direccion': 'Dirección',
            'Inmigrante': '¿Es Inmigrante?',
            'Discapacidad': '¿Tiene Discapacidad?',
            'Tipo_de_Discapacidad': 'Tipo de Discapacidad',
            'Privada_de_Libertad': '¿Está Privada de Libertad?',
            'Trans_Masculino': '¿Es Trans Masculino?',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer los campos opcionales si es necesario
        self.fields['Nacionalidad'].required = False
        self.fields['Pueblos_originarios'].required = False
        self.fields['Telefono'].required = False
        self.fields['Direccion'].required = False
        self.fields['Tipo_de_Discapacidad'].required = False
    
    def clean_Rut(self):
        """Validar y normalizar RUT"""
        rut = self.cleaned_data.get('Rut', '').strip().upper()
        
        if not rut:
            raise ValidationError('El RUT es obligatorio.')
        
        # Validar formato básico
        if '-' not in rut:
            raise ValidationError('El RUT debe tener el formato: 12345678-9')
        
        partes = rut.split('-')
        if len(partes) != 2:
            raise ValidationError('El RUT debe tener un solo guión.')
        
        cuerpo, dv = partes
        
        if not cuerpo.isdigit():
            raise ValidationError('La parte numérica del RUT debe contener solo números.')
        
        if len(cuerpo) < 7 or len(cuerpo) > 8:
            raise ValidationError('El RUT debe tener 7 u 8 dígitos.')
        
        if not (dv.isdigit() or dv == 'K'):
            raise ValidationError('El dígito verificador debe ser un número o K.')
        
        return rut.upper()
    
    def clean_Nombre(self):
        """Validar nombre"""
        nombre = self.cleaned_data.get('Nombre', '').strip()
        
        if not nombre:
            raise ValidationError('El nombre es obligatorio.')
        
        if len(nombre) < 2:
            raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        
        return nombre.title()
    
    def clean_Apellido_Paterno(self):
        """Validar apellido paterno"""
        apellido = self.cleaned_data.get('Apellido_Paterno', '').strip()
        
        if not apellido:
            raise ValidationError('El apellido paterno es obligatorio.')
        
        if len(apellido) < 2:
            raise ValidationError('El apellido debe tener al menos 2 caracteres.')
        
        return apellido.title()
    
    def clean_Apellido_Materno(self):
        """Validar apellido materno"""
        apellido = self.cleaned_data.get('Apellido_Materno', '').strip()
        
        if not apellido:
            raise ValidationError('El apellido materno es obligatorio.')
        
        if len(apellido) < 2:
            raise ValidationError('El apellido debe tener al menos 2 caracteres.')
        
        return apellido.title()
    
    def clean_Fecha_nacimiento(self):
        """Validar fecha de nacimiento"""
        from datetime import date
        fecha = self.cleaned_data.get('Fecha_nacimiento')
        
        if not fecha:
            raise ValidationError('La fecha de nacimiento es obligatoria.')
        
        # Validar que no sea futura
        if fecha > date.today():
            raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')
        
        # Validar edad razonable (mayor que 10 años)
        try:
            from dateutil.relativedelta import relativedelta
            hace_10_anos = date.today() - relativedelta(years=10)
            
            if fecha > hace_10_anos:
                raise ValidationError('La persona debe tener al menos 10 años.')
        except ImportError:
            # Si dateutil no está instalado, usar cálculo simple
            anos = (date.today() - fecha).days // 365
            if anos < 10:
                raise ValidationError('La persona debe tener al menos 10 años.')
        
        return fecha
    
    def clean_Telefono(self):
        """Validar teléfono"""
        telefono = self.cleaned_data.get('Telefono', '').strip()
        
        if telefono:
            # Remover espacios y guiones
            telefono_limpio = ''.join(c for c in telefono if c.isdigit() or c == '+')
            
            if len(telefono_limpio) < 8:
                raise ValidationError('El teléfono debe tener al menos 8 dígitos.')
        
        return telefono


class BuscarPersonaForm(forms.Form):
    """
    Formulario para buscar personas
    Búsqueda simple por texto
    """
    
    q = forms.CharField(
        max_length=100,
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre, apellido o RUT...',
            'autocomplete': 'off',
        })
    )
    
    def clean_q(self):
        """Validar búsqueda"""
        q = self.cleaned_data.get('q', '').strip()
        
        # Si está vacío, está permitido (búsqueda sin filtro)
        if not q:
            return q
        
        # Si tiene contenido, debe tener mínimo 2 caracteres
        if len(q) < 2:
            raise ValidationError('Ingrese al menos 2 caracteres para buscar.')
        
        return q
