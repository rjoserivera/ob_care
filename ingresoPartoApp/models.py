Models ingresopartoapp completo · PY
Copiar

"""
ingresoPartoApp/models.py
Modelo para Ingreso a Parto (Evaluación en sala de parto)
COMPLETO: Todos los campos necesarios
"""

from django.db import models
from django.utils import timezone
from matronaApp.models import FichaObstetrica


# ============================================
# CATÁLOGOS
# ============================================

class CatalogoEstadoCervical(models.Model):
    """Estado cervical en ingreso"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        verbose_name = 'Estado Cervical'
        verbose_name_plural = 'Estados Cervicales'
    
    def __str__(self):
        return self.nombre


class CatalogoEstadoFetal(models.Model):
    """Estado fetal en ingreso"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        verbose_name = 'Estado Fetal'
        verbose_name_plural = 'Estados Fetales'
    
    def __str__(self):
        return self.nombre


# ============================================
# MODELO: FICHA DE PARTO (INGRESO)
# ============================================

class FichaParto(models.Model):
    """
    Ficha de ingreso a parto - Evaluación inicial en sala de parto
    """
    
    # ============================================
    # RELACIONES
    # ============================================
    
    ficha_obstetrica = models.OneToOneField(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='ficha_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    # ============================================
    # IDENTIFICACIÓN
    # ============================================
    
    numero_ficha_parto = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Número de Ficha de Parto'
    )
    
    fecha_ingreso = models.DateField(
        verbose_name='Fecha de Ingreso'
    )
    
    hora_ingreso = models.TimeField(
        verbose_name='Hora de Ingreso'
    )
    
    # ============================================
    # EVALUACIÓN INICIAL
    # ============================================
    
    edad_gestacional_semanas = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Semanas de Gestación'
    )
    
    edad_gestacional_dias = models.PositiveIntegerField(
        default=0,
        verbose_name='Días Adicionales'
    )
    
    dilatacion_cervical_cm = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name='Dilatación Cervical (cm)'
    )
    
    estado_cervical = models.ForeignKey(
        CatalogoEstadoCervical,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Estado Cervical'
    )
    
    posicion_fetal = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Posición Fetal'
    )
    
    altura_presentacion = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Altura de Presentación'
    )
    
    membranas_rotas = models.BooleanField(
        default=False,
        verbose_name='Membranas Rotas'
    )
    
    tiempo_ruptura = models.DurationField(
        null=True,
        blank=True,
        verbose_name='Tiempo de Ruptura'
    )
    
    caracteristicas_liquido = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Características del Líquido Amniótico'
    )
    
    # ============================================
    # EVALUACIÓN FETAL
    # ============================================
    
    frecuencia_cardiaca_fetal = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Frecuencia Cardíaca Fetal (lpm)'
    )
    
    estado_fetal = models.ForeignKey(
        CatalogoEstadoFetal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Estado Fetal'
    )
    
    cardiotocografia_realizada = models.BooleanField(
        default=False,
        verbose_name='CTG Realizada'
    )
    
    resultado_ctg = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Resultado CTG'
    )
    
    # ============================================
    # EVALUACIÓN MATERNA
    # ============================================
    
    presion_arterial_sistolica = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='PA Sistólica (mmHg)'
    )
    
    presion_arterial_diastolica = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='PA Diastólica (mmHg)'
    )
    
    frecuencia_cardiaca_materna = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='FC Materna (lpm)'
    )
    
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name='Temperatura (°C)'
    )
    
    frecuencia_respiratoria = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='FR (rpm)'
    )
    
    # ============================================
    # LABORATORIO
    # ============================================
    
    sgb_pesquisa = models.BooleanField(
        default=False,
        verbose_name='SGB Pesquisa'
    )
    
    sgb_resultado = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Resultado SGB'
    )
    
    vih_tomado = models.BooleanField(
        default=False,
        verbose_name='VIH Tomado'
    )
    
    vih_resultado = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Resultado VIH'
    )
    
    vih_aro = models.BooleanField(
        default=False,
        verbose_name='VIH ARO'
    )
    
    vdrl_resultado = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Resultado VDRL'
    )
    
    vdrl_tratamiento_atb = models.BooleanField(
        default=False,
        verbose_name='VDRL Tratamiento ATB'
    )
    
    hepatitis_b_tomado = models.BooleanField(
        default=False,
        verbose_name='Hepatitis B Tomado'
    )
    
    hepatitis_b_resultado = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Resultado Hepatitis B'
    )
    
    hepatitis_b_derivacion = models.BooleanField(
        default=False,
        verbose_name='Hepatitis B Derivación'
    )
    
    # ============================================
    # DIAGNÓSTICO Y PLAN
    # ============================================
    
    diagnostico_ingreso = models.TextField(
        blank=True,
        verbose_name='Diagnóstico de Ingreso'
    )
    
    plan_manejo = models.TextField(
        blank=True,
        verbose_name='Plan de Manejo'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    antecedentes_relevantes = models.TextField(
        blank=True,
        verbose_name='Antecedentes Relevantes'
    )
    
    # ============================================
    # METADATA
    # ============================================
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Ficha Activa'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Modificación'
    )
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['-fecha_ingreso']
        verbose_name = 'Ficha de Parto'
        verbose_name_plural = 'Fichas de Parto'
    
    def __str__(self):
        paciente = self.ficha_obstetrica.paciente
        return f"Ficha Parto {self.numero_ficha_parto} - {paciente.persona.Nombre}"