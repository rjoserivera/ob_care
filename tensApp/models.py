# ============================================
# tensApp/models.py
# VERSIÓN SIN CHOICES - FK A TABLAS CATÁLOGO
# ============================================
# NOTA: Usa CatalogoViaAdministracion de matronaApp (compartido)
# ============================================

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Importar catálogo compartido
from matronaApp.models import CatalogoViaAdministracion


# ============================================
# MODELO: REGISTRO TENS (Sin CHOICES)
# ============================================

class RegistroTens(models.Model):
    """
    Registro de signos vitales por TENS
    Este modelo NO tiene CHOICES, solo campos normales
    """
    
    ficha = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.CASCADE,
        related_name='registros_tens',
        verbose_name='Ficha Obstétrica'
    )
    
    tens_responsable = models.ForeignKey(
        'gestionApp.Tens',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_signos_vitales',
        verbose_name='TENS Responsable'
    )
    
    fecha = models.DateField(
        default=timezone.now,
        verbose_name='Fecha del Registro'
    )
    
    # Usamos FK al catálogo de turno de gestionApp
    turno = models.ForeignKey(
        'gestionApp.CatalogoTurno',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_tens',
        verbose_name='Turno'
    )
    
    # Signos vitales (sin CHOICES)
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
        auto_now_add=True,
        verbose_name='Fecha y Hora del Registro'
    )
    
    class Meta:
        ordering = ['-fecha', '-fecha_registro']
        verbose_name = 'Registro TENS'
        verbose_name_plural = 'Registros TENS'
        indexes = [
            models.Index(fields=['ficha', '-fecha']),
            models.Index(fields=['tens_responsable', '-fecha']),
        ]
    
    def __str__(self):
        return f"{self.ficha.paciente.persona.Nombre} - {self.fecha}"
    
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
    """
    Registro de tratamientos/medicamentos aplicados por TENS
    SIN CHOICES - Usa FK a tablas catálogo
    """
    
    # ============================================
    # RELACIONES
    # ============================================
    
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
        'gestionApp.Tens',
        on_delete=models.PROTECT,
        related_name='tratamientos_aplicados',
        verbose_name='TENS que Aplicó'
    )
    
    medicamento_ficha = models.ForeignKey(
        'matronaApp.MedicamentoFicha',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='aplicaciones_tens',
        verbose_name='Medicamento de Ficha',
        help_text='Si aplica un medicamento prescrito en la ficha'
    )
    
    # ============================================
    # DATOS DEL TRATAMIENTO
    # ============================================
    
    nombre_medicamento = models.CharField(
        max_length=200,
        verbose_name='Nombre del Medicamento/Tratamiento'
    )
    
    dosis = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Dosis Aplicada',
        help_text='Ej: 500mg, 10ml, 2 comprimidos'
    )
    
    # FK a catálogo compartido (antes era CHOICES)
    via_administracion_catalogo = models.ForeignKey(
        CatalogoViaAdministracion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='tratamientos_aplicados',
        verbose_name='Vía de Administración'
    )
    
    @property
    def via_administracion(self):
        """Alias para compatibilidad"""
        return self.via_administracion_catalogo.codigo if self.via_administracion_catalogo else None
    
    fecha_aplicacion = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Aplicación'
    )
    
    hora_aplicacion = models.TimeField(
        default=timezone.now,
        verbose_name='Hora de Aplicación'
    )
    
    # ============================================
    # PROCEDIMIENTO
    # ============================================
    
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
        verbose_name='Motivo de No Aplicación',
        help_text='Si no se aplicó, indicar el motivo'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    reacciones_adversas = models.TextField(
        blank=True,
        verbose_name='Reacciones Adversas',
        help_text='Cualquier reacción adversa observada'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Registro Activo'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Modificación'
    )
    
    class Meta:
        ordering = ['-fecha_aplicacion', '-hora_aplicacion']
        verbose_name = 'Tratamiento Aplicado'
        verbose_name_plural = 'Tratamientos Aplicados'
        indexes = [
            models.Index(fields=['ficha', '-fecha_aplicacion']),
            models.Index(fields=['paciente', '-fecha_aplicacion']),
            models.Index(fields=['tens', '-fecha_aplicacion']),
            models.Index(fields=['medicamento_ficha', '-fecha_aplicacion']),
        ]
    
    def __str__(self):
        return f"{self.nombre_medicamento} - {self.paciente.persona.Nombre} - {self.fecha_aplicacion}"


