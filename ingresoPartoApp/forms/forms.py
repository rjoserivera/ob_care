"""
ingresoPartoApp/forms/forms.py
Formulario MEJORADO para FichaParto
Con todos los campos y catálogos
"""

from django import forms
from ..models import (
    FichaParto, 
    BebeEsperado,
    CatalogoEstadoCervical,
    CatalogoEstadoFetal,
    CatalogoPosicionFetal,
    CatalogoAlturaPresentacion,
    CatalogoCaracteristicasLiquido,
    CatalogoResultadoCTG,
    CatalogoSalaAsignada,
)


class FichaPartoForm(forms.ModelForm):
    """Formulario completo para crear/editar ficha de ingreso a parto"""
    
    class Meta:
        model = FichaParto
        fields = [
            # ===== DATOS DE INGRESO =====
            'fecha_ingreso',
            'hora_ingreso',
            'sala_asignada',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            
            # ===== EVALUACIÓN CERVICAL =====
            'dilatacion_cervical_cm',
            'borramiento',
            'estado_cervical',
            
            # ===== EVALUACIÓN FETAL =====
            'posicion_fetal',
            'altura_presentacion',
            'estado_fetal',
            'frecuencia_cardiaca_fetal',
            
            # ===== MEMBRANAS =====
            'membranas_rotas',
            'tiempo_ruptura_horas',
            'caracteristicas_liquido',
            
            # ===== CTG =====
            'cardiotocografia_realizada',
            'resultado_ctg',
            'observacion_ctg',
            
            # ===== SIGNOS VITALES =====
            'presion_arterial_sistolica',
            'presion_arterial_diastolica',
            'frecuencia_cardiaca_materna',
            'temperatura',
            'saturacion_oxigeno',
            
            # ===== LABORATORIO VIH =====
            'vih_tomado_prepartos',
            'vih_tomado_sala',
            'vih_resultado',
            
            # ===== LABORATORIO SGB =====
            'sgb_pesquisa',
            'sgb_resultado',
            'antibiotico_sgb',
            
            # ===== LABORATORIO VDRL =====
            'vdrl_resultado',
            'tratamiento_sifilis',
            
            # ===== LABORATORIO HEP B =====
            'hepatitis_b_tomado',
            'hepatitis_b_resultado',
            
            # ===== PATOLOGÍAS =====
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_grave',
            'infeccion_ovular',
            'otras_patologias',
            
            # ===== DIAGNÓSTICO =====
            'diagnostico_ingreso',
            'plan_de_manejo',
            'observaciones',
        ]
        
        widgets = {
            # ===== DATOS DE INGRESO =====
            'fecha_ingreso': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'hora_ingreso': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time',
                }
            ),
            'sala_asignada': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'edad_gestacional_semanas': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '20',
                    'max': '45',
                    'placeholder': 'Semanas',
                    'style': 'width: 100px;'
                }
            ),
            'edad_gestacional_dias': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'max': '6',
                    'placeholder': 'Días',
                    'style': 'width: 80px;'
                }
            ),
            
            # ===== EVALUACIÓN CERVICAL =====
            'dilatacion_cervical_cm': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'max': '10',
                    'step': '0.5',
                    'placeholder': 'cm'
                }
            ),
            'borramiento': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'max': '100',
                    'placeholder': '%'
                }
            ),
            'estado_cervical': forms.Select(
                attrs={'class': 'form-select'}
            ),
            
            # ===== EVALUACIÓN FETAL =====
            'posicion_fetal': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'altura_presentacion': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'estado_fetal': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'frecuencia_cardiaca_fetal': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '60',
                    'max': '220',
                    'placeholder': 'lpm (120-160 normal)'
                }
            ),
            
            # ===== MEMBRANAS =====
            'membranas_rotas': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'tiempo_ruptura_horas': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'placeholder': 'Horas desde ruptura'
                }
            ),
            'caracteristicas_liquido': forms.Select(
                attrs={'class': 'form-select'}
            ),
            
            # ===== CTG =====
            'cardiotocografia_realizada': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'resultado_ctg': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'observacion_ctg': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '2',
                    'placeholder': 'Observaciones del trazado...'
                }
            ),
            
            # ===== SIGNOS VITALES =====
            'presion_arterial_sistolica': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '60',
                    'max': '250',
                    'placeholder': 'mmHg'
                }
            ),
            'presion_arterial_diastolica': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '30',
                    'max': '150',
                    'placeholder': 'mmHg'
                }
            ),
            'frecuencia_cardiaca_materna': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '40',
                    'max': '200',
                    'placeholder': 'lpm'
                }
            ),
            'temperatura': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '34',
                    'max': '42',
                    'step': '0.1',
                    'placeholder': '°C'
                }
            ),
            'saturacion_oxigeno': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '70',
                    'max': '100',
                    'placeholder': '%'
                }
            ),
            
            # ===== LABORATORIO =====
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_tomado_sala': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_resultado': forms.Select(attrs={'class': 'form-select'}),
            'sgb_pesquisa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sgb_resultado': forms.Select(attrs={'class': 'form-select'}),
            'antibiotico_sgb': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vdrl_resultado': forms.Select(attrs={'class': 'form-select'}),
            'tratamiento_sifilis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hepatitis_b_resultado': forms.Select(attrs={'class': 'form-select'}),
            
            # ===== PATOLOGÍAS =====
            'preeclampsia_severa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'eclampsia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sepsis_infeccion_grave': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'infeccion_ovular': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'otras_patologias': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '2',
                    'placeholder': 'Otras patologías activas...'
                }
            ),
            
            # ===== DIAGNÓSTICO =====
            'diagnostico_ingreso': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': 'Diagnóstico de ingreso a sala de parto...'
                }
            ),
            'plan_de_manejo': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': 'Plan de manejo...'
                }
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': 'Observaciones adicionales...'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer algunos campos opcionales
        self.fields['sala_asignada'].required = False
        self.fields['diagnostico_ingreso'].required = False
        
        # Ordenar los queryset de los catálogos
        if 'estado_cervical' in self.fields:
            self.fields['estado_cervical'].queryset = CatalogoEstadoCervical.objects.filter(activo=True).order_by('orden')
        
        if 'estado_fetal' in self.fields:
            self.fields['estado_fetal'].queryset = CatalogoEstadoFetal.objects.filter(activo=True).order_by('orden')
        
        if 'posicion_fetal' in self.fields:
            self.fields['posicion_fetal'].queryset = CatalogoPosicionFetal.objects.filter(activo=True).order_by('orden')
        
        if 'altura_presentacion' in self.fields:
            self.fields['altura_presentacion'].queryset = CatalogoAlturaPresentacion.objects.filter(activo=True).order_by('orden')
        
        if 'caracteristicas_liquido' in self.fields:
            self.fields['caracteristicas_liquido'].queryset = CatalogoCaracteristicasLiquido.objects.filter(activo=True).order_by('orden')
        
        if 'resultado_ctg' in self.fields:
            self.fields['resultado_ctg'].queryset = CatalogoResultadoCTG.objects.filter(activo=True).order_by('orden')
        
        if 'sala_asignada' in self.fields:
            self.fields['sala_asignada'].queryset = CatalogoSalaAsignada.objects.filter(activo=True).order_by('nombre')

    def clean(self):
        cleaned_data = super().clean()
        
        # Si membranas rotas, tiempo de ruptura es recomendado
        membranas_rotas = cleaned_data.get('membranas_rotas')
        tiempo_ruptura = cleaned_data.get('tiempo_ruptura_horas')
        
        if membranas_rotas and not tiempo_ruptura:
            self.add_error('tiempo_ruptura_horas', 'Indique el tiempo aproximado de ruptura de membranas')
        
        # Si CTG realizada, resultado es requerido
        ctg_realizada = cleaned_data.get('cardiotocografia_realizada')
        resultado_ctg = cleaned_data.get('resultado_ctg')
        
        if ctg_realizada and not resultado_ctg:
            self.add_error('resultado_ctg', 'Indique el resultado de la cardiotocografía')
        
        # Validar presión arterial
        pa_sistolica = cleaned_data.get('presion_arterial_sistolica')
        pa_diastolica = cleaned_data.get('presion_arterial_diastolica')
        
        if pa_sistolica and pa_diastolica:
            if pa_diastolica >= pa_sistolica:
                self.add_error('presion_arterial_diastolica', 'La PA diastólica debe ser menor que la sistólica')
        
        return cleaned_data


class BebeEsperadoForm(forms.ModelForm):
    """Formulario para información de bebé esperado"""
    
    class Meta:
        model = BebeEsperado
        fields = [
            'numero_bebe',
            'sexo_esperado',
            'peso_estimado',
            'posicion_fetal',
            'frecuencia_cardiaca',
            'observaciones',
        ]
        
        widgets = {
            'numero_bebe': forms.NumberInput(
                attrs={'class': 'form-control', 'readonly': True}
            ),
            'sexo_esperado': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'peso_estimado': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '500',
                    'max': '6000',
                    'placeholder': 'gramos'
                }
            ),
            'posicion_fetal': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'frecuencia_cardiaca': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '60',
                    'max': '220',
                    'placeholder': 'lpm'
                }
            ),
            'observaciones': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Observaciones del bebé...'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'posicion_fetal' in self.fields:
            self.fields['posicion_fetal'].queryset = CatalogoPosicionFetal.objects.filter(activo=True).order_by('orden')