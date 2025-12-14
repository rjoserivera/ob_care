"""
tensApp/models.py
Modelos para TENS - CORREGIDO para usar User + Groups
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

# Importar catálogo compartido
from matronaApp.models import CatalogoViaAdministracion


# ============================================
# MODELO: REGISTRO TENS
# ============================================

class RegistroTens(models.Model):
    """Registro de signos vitales por TENS"""
    
    ficha = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.CASCADE,
        related_name='registros_tens',
        verbose_name='Ficha Obstétrica'
    )
    
    tens_responsable = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_signos_vitales',
        verbose_name='TENS Responsable',
        limit_choices_to={'groups__name': 'TENS'}
    )
    
    fecha = models.DateField(
        default=timezone.now,
        verbose_name='Fecha del Registro'
    )
    
    turno = models.ForeignKey(
        'gestionApp.CatalogoTurno',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_tens',
        verbose_name='Turno'
    )
    
    # Signos vitales
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(34.0), MaxValueValidator(42.0)],
        verbose_name='Temperatura (°C)'
    )
    
    frecuencia_cardiaca = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        verbose_name='Frecuencia Cardíaca (lpm)'
    )
    
    presion_arterial_sistolica = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(60), MaxValueValidator(250)],
        verbose_name='Presión Sistólica (mmHg)'
    )
    
    presion_arterial_diastolica = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(150)],
        verbose_name='Presión Diastólica (mmHg)'
    )
    
    frecuencia_respiratoria = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(8), MaxValueValidator(40)],
        verbose_name='Frecuencia Respiratoria (rpm)'
    )
    
    saturacion_oxigeno = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(50), MaxValueValidator(100)],
        verbose_name='Saturación O2 (%)'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    fecha_registro = models.DateTimeField(
        default=timezone.now
    )
    
    class Meta:
        verbose_name = 'Registro TENS'
        verbose_name_plural = 'Registros TENS'
        ordering = ['-fecha', '-fecha_registro']
        indexes = [
            models.Index(fields=['ficha', '-fecha']),
            models.Index(fields=['tens_responsable', '-fecha']),
        ]
    
    def __str__(self):
        return f"{self.ficha.numero_ficha} - {self.fecha}"
    
    @property
    def presion_arterial(self):
        """Retorna la presión arterial en formato 120/80"""
        if self.presion_arterial_sistolica and self.presion_arterial_diastolica:
            return f"{self.presion_arterial_sistolica}/{self.presion_arterial_diastolica}"
        return "No registrada"


# ============================================
# MODELO: TRATAMIENTO APLICADO
# ============================================

class Tratamiento_aplicado(models.Model):
    """Registro de tratamientos/medicamentos aplicados por TENS"""
    
    ficha = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.CASCADE,
        related_name='tratamientos_aplicados',
        verbose_name='Ficha Obstétrica'
    )
    
    paciente = models.ForeignKey(
        'gestionApp.Paciente',
        on_delete=models.CASCADE,
        related_name='tratamientos_recibidos',
        verbose_name='Paciente'
    )
    
    tens = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tratamientos_aplicados',
        verbose_name='TENS que Aplicó',
        limit_choices_to={'groups__name': 'TENS'}
    )
    
    medicamento_ficha = models.ForeignKey(
        'matronaApp.MedicamentoFicha',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='aplicaciones_tens',
        verbose_name='Medicamento de Ficha'
    )
    
    # Datos del tratamiento
    nombre_medicamento = models.CharField(
        max_length=200,
        verbose_name='Nombre del Medicamento/Tratamiento'
    )
    
    dosis = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Dosis Aplicada'
    )
    
    via_administracion = models.ForeignKey(
        CatalogoViaAdministracion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='tratamientos_aplicados',
        verbose_name='Vía de Administración'
    )
    
    fecha_aplicacion = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Aplicación'
    )
    
    hora_aplicacion = models.TimeField(
        default=timezone.now,
        verbose_name='Hora de Aplicación'
    )
    
    # Procedimiento
    se_realizo_lavado_manos = models.BooleanField(
        default=False,
        verbose_name='¿Se realizó lavado de manos?'
    )
    
    aplicado_exitosamente = models.BooleanField(
        default=True,
        verbose_name='¿Se aplicó exitosamente?'
    )
    
    motivo_no_aplicacion = models.TextField(
        blank=True,
        verbose_name='Motivo de No Aplicación'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    fecha_registro = models.DateTimeField(
        default=timezone.now
    )
    
    class Meta:
        verbose_name = 'Tratamiento Aplicado'
        verbose_name_plural = 'Tratamientos Aplicados'
        ordering = ['-fecha_aplicacion', '-hora_aplicacion']
        indexes = [
            models.Index(fields=['ficha', '-fecha_aplicacion']),
            models.Index(fields=['paciente', '-fecha_aplicacion']),
            models.Index(fields=['tens', '-fecha_aplicacion']),
        ]
    
    def __str__(self):
        return f"{self.nombre_medicamento} - {self.paciente} - {self.fecha_aplicacion}"