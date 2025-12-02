"""
Formulario para Documentos de Parto
recienNacidoApp/forms/documentos_parto_form.py
"""
from django import forms
from django.core.exceptions import ValidationError
from recienNacidoApp.models import DocumentosParto


class DocumentosPartoForm(forms.ModelForm):
    """
    Formulario para documentos post-parto
    Incluye: Ley Dominga, placenta, registro civil, manejo dolor
    """
    
    class Meta:
        model = DocumentosParto
        fields = [
            'registro_recien_nacido',
            # Ley Dominga
            'recuerdos_entregados',
            # Placenta
            'retira_placenta',
            'estampado_placenta',
            # Registro Civil
            'folio_valido',
            'folios_nulos',
            # Otros
            'manejo_dolor_no_farmacologico',
        ]
        
        widgets = {
            'registro_recien_nacido': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            
            # Ley Dominga
            'recuerdos_entregados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de recuerdos entregados según Ley N° 21.372 Dominga. Si no se entregan, justificar motivo.'
            }),
            
            # Placenta
            'retira_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'estampado_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Registro Civil
            'folio_valido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de folio válido del Registro Civil'
            }),
            'folios_nulos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Folios anulados (si aplica, separados por coma)'
            }),
            
            # Otros
            'manejo_dolor_no_farmacologico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de métodos no farmacológicos utilizados (masajes, respiración, hidroterapia, etc.)'
            }),
        }
        
        labels = {
            'registro_recien_nacido': 'Registro de Recién Nacido',
            'recuerdos_entregados': 'Recuerdos Entregados (Ley Dominga)',
            'retira_placenta': 'Familia Retira Placenta',
            'estampado_placenta': 'Se Realizó Estampado de Placenta',
            'folio_valido': 'Folio Válido Registro Civil',
            'folios_nulos': 'Folios Nulos/Anulados',
            'manejo_dolor_no_farmacologico': 'Manejo del Dolor No Farmacológico',
        }
        
        help_texts = {
            'recuerdos_entregados': 'Ley N° 21.372 - Derecho a conservar recuerdos del proceso de parto',
            'retira_placenta': '¿La familia solicitó llevarse la placenta?',
            'estampado_placenta': 'Impresión artística de la placenta como recuerdo',
            'folio_valido': 'Número oficial del documento de Registro Civil',
            'folios_nulos': 'Indicar folios que fueron anulados por errores',
            'manejo_dolor_no_farmacologico': 'Técnicas complementarias para el manejo del dolor durante el parto',
        }
    
    def clean_folio_valido(self):
        """Validar formato del folio válido"""
        folio = self.cleaned_data.get('folio_valido')
        
        if folio:
            # Eliminar espacios
            folio = folio.strip()
            
            # Validar que no esté vacío después de limpiar
            if not folio:
                raise ValidationError('El folio no puede estar vacío.')
        
        return folio
    
    def clean_folios_nulos(self):
        """Validar formato de folios nulos"""
        folios = self.cleaned_data.get('folios_nulos')
        
        if folios:
            # Eliminar espacios innecesarios
            folios = folios.strip()
        
        return folios
    
    def clean(self):
        """Validaciones generales del formulario"""
        cleaned_data = super().clean()
        
        # Validar placenta
        retira = cleaned_data.get('retira_placenta')
        estampado = cleaned_data.get('estampado_placenta')
        
        # Si se hace estampado, probablemente no se retira (se destruye)
        # Esta es solo una advertencia, no un error
        if estampado and retira:
            # Solo informativo, no bloqueante
            pass
        
        return cleaned_data
