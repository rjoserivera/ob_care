from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona
from matronaApp.models import Paciente
from utilidad.rut_validator import normalizar_rut, RutValidator
from datetime import date


class PacienteForm(forms.ModelForm):
    rut_persona_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT de la Persona',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'pattern': '[0-9]{7,8}'
        }),
        help_text='Ingrese el RUT de la persona a vincular como paciente'
    )
    
    rut_persona_dv = forms.CharField(
        max_length=1,
        required=True,
        label='DV',
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'K',
            'maxlength': '1',
            'pattern': '[0-9Kk]',
            'style': 'text-transform: uppercase;'
        })
    )
    
    class Meta:
        model = Paciente
        # ✅ CORREGIDO: Usar '__all__' para incluir todos los campos que existen
        fields = '__all__'
        
        # OPCIONAL: Si quieres especificar los campos manualmente, usa estos nombres correctos:
        # fields = [
        #     'persona',
        #     'Estado_civil',
        #     'Previcion',
        #     'paridad',
        #     'Ductus_Venosus',
        #     'control_prenatal',
        #     'Consultorio',          # ← Con C MAYÚSCULA
        #     'IMC',                  # ← TODO MAYÚSCULAS
        #     'Preeclampsia_Severa',
        #     'Eclampsia',
        #     'Sepsis_o_Infeccion_SiST',
        #     'Infeccion_Ovular_o_Corioamnionitis',
        #     'Acompañante',
        #     'Contacto_emergencia',
        # ]
        
        widgets = {
            'Estado_civil': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Previcion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'paridad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: G3P2A0'
            }),
            'Ductus_Venosus': forms.Select(attrs={
                'class': 'form-select'
            }),
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'Consultorio': forms.Select(attrs={
                'class': 'form-select'
            }),
            'IMC': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '10',
                'max': '60',
                'placeholder': 'Índice de Masa Corporal'
            }),
            'Preeclampsia_Severa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'Eclampsia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'Sepsis_o_Infeccion_SiST': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'Infeccion_Ovular_o_Corioamnionitis': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'Acompañante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del acompañante'
            }),
            'Contacto_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer que persona no sea required en el formulario
        # ya que se manejará mediante los campos de RUT
        if 'persona' in self.fields:
            self.fields['persona'].required = False
            self.fields['persona'].widget = forms.HiddenInput()
        
        # Pre-llenar RUT si estamos editando
        if self.instance and self.instance.pk and hasattr(self.instance, 'persona'):
            rut_completo = self.instance.persona.Rut
            if rut_completo and '-' in rut_completo:
                cuerpo, dv = rut_completo.split('-')
                self.initial['rut_persona_cuerpo'] = cuerpo
                self.initial['rut_persona_dv'] = dv
    
    def clean(self):
        cleaned_data = super().clean()
        rut_cuerpo = cleaned_data.get('rut_persona_cuerpo')
        rut_dv = cleaned_data.get('rut_persona_dv')
        
        if rut_cuerpo and rut_dv:
            # Construir RUT completo
            rut_completo = f"{rut_cuerpo}-{rut_dv.upper()}"
            rut_normalizado = normalizar_rut(rut_completo)
            
            # Validar formato
            validator = RutValidator()
            try:
                validator(rut_normalizado)
            except ValidationError as e:
                raise ValidationError(f"RUT inválido: {e.message}")
            
            # Buscar la persona
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                cleaned_data['persona'] = persona
            except Persona.DoesNotExist:
                raise ValidationError(
                    f"No existe una persona registrada con el RUT {rut_normalizado}. "
                    "Por favor, registre primero a la persona."
                )
            
            # Verificar si ya existe un paciente con esta persona
            if not self.instance.pk:  # Solo al crear, no al editar
                if Paciente.objects.filter(persona=persona).exists():
                    raise ValidationError(
                        f"Ya existe un paciente registrado para la persona con RUT {rut_normalizado}"
                    )
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Asignar la persona
        if 'persona' in self.cleaned_data:
            instance.persona = self.cleaned_data['persona']
        
        if commit:
            instance.save()
            self.save_m2m()  # Guardar relaciones ManyToMany si las hay
        
        return instance