from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Medico
from utilidad.rut_validator import normalizar_rut, RutValidator


class MedicoForm(forms.ModelForm):
    rut_persona_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT de la Persona',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'pattern': '[0-9]{7,8}'
        }),
        help_text='Ingrese el RUT de la persona a vincular como médico'
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
        model = Medico
        fields = [
            'Especialidad',
            'Registro_medico',
            'Años_experiencia',
            'Turno',
            'Activo'
        ]
        
        widgets = {
            'Especialidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Registro_medico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: RM-12345'
            }),
            'Años_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '60'
            }),
            'Turno': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'Especialidad': 'Especialidad Médica',
            'Registro_medico': 'Registro Médico',
            'Años_experiencia': 'Años de Experiencia',
            'Turno': 'Turno de Trabajo',
            'Activo': '¿Médico Activo?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk and hasattr(self.instance, 'persona'):
            datos_rut = RutValidator.separar_rut(self.instance.persona.Rut)
            self.fields['rut_persona_cuerpo'].initial = datos_rut['cuerpo']
            self.fields['rut_persona_dv'].initial = datos_rut['dv']
            
            self.fields['rut_persona_cuerpo'].disabled = True
            self.fields['rut_persona_dv'].disabled = True
            self.fields['rut_persona_cuerpo'].widget.attrs['class'] += ' bg-light'
            self.fields['rut_persona_dv'].widget.attrs['class'] += ' bg-light'
            self.fields['rut_persona_cuerpo'].help_text = 'El RUT no se puede modificar'
    
    def clean_rut_persona_cuerpo(self):
        rut_cuerpo = self.cleaned_data.get('rut_persona_cuerpo', '').strip()
        
        if not rut_cuerpo:
            raise ValidationError('El RUT de la persona es obligatorio.')
        
        if not rut_cuerpo.isdigit():
            raise ValidationError('El RUT debe contener solo números.')
        
        if len(rut_cuerpo) < 7 or len(rut_cuerpo) > 8:
            raise ValidationError('El RUT debe tener 7 u 8 dígitos.')
        
        return rut_cuerpo
    
    def clean_rut_persona_dv(self):
        rut_dv = self.cleaned_data.get('rut_persona_dv', '').strip().upper()
        
        if not rut_dv:
            raise ValidationError('El dígito verificador es obligatorio.')
        
        if len(rut_dv) != 1:
            raise ValidationError('El dígito verificador debe ser un solo carácter.')
        
        if not (rut_dv.isdigit() or rut_dv == 'K'):
            raise ValidationError('El dígito verificador debe ser un número o K.')
        
        return rut_dv
    
    def clean_Registro_medico(self):
        registro = self.cleaned_data.get('Registro_medico')
        
        if self.instance and self.instance.pk:
            if Medico.objects.filter(Registro_medico=registro).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Este número de registro ya existe.')
        else:
            if Medico.objects.filter(Registro_medico=registro).exists():
                raise ValidationError('Este número de registro ya existe.')
        
        return registro
    
    def clean_Años_experiencia(self):
        años = self.cleaned_data.get('Años_experiencia')
        
        if años < 0:
            raise ValidationError('Los años de experiencia no pueden ser negativos.')
        
        if años > 60:
            raise ValidationError('Los años de experiencia no pueden ser mayores a 60.')
        
        return años
    
    def clean(self):
        cleaned_data = super().clean()
        
        if self.instance and self.instance.pk:
            return cleaned_data
        
        rut_cuerpo = cleaned_data.get('rut_persona_cuerpo')
        rut_dv = cleaned_data.get('rut_persona_dv')
        
        if rut_cuerpo and rut_dv:
            rut_completo = f"{rut_cuerpo}-{rut_dv}"
            rut_normalizado = normalizar_rut(rut_completo)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                if hasattr(persona, 'medico'):
                    raise ValidationError({
                        'rut_persona_cuerpo': 'Esta persona ya está registrada como médico.'
                    })
                
                self._persona_obj = persona
                
            except Persona.DoesNotExist:
                raise ValidationError({
                    'rut_persona_cuerpo': (
                        'No existe una persona registrada con este RUT. '
                        'Registre primero los datos básicos de la persona.'
                    )
                })
        
        return cleaned_data
    
    def save(self, commit=True):
        medico = super().save(commit=False)
        
        if not self.instance.pk:
            persona = getattr(self, '_persona_obj', None)
            if persona:
                medico.persona = persona
        
        if commit:
            medico.save()
        
        return medico
