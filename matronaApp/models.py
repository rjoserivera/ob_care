"""
matronaApp/models.py
Modelos para matrona - Fichas obstétricas, ingresos y medicamentos
ACTUALIZADO CON TODOS LOS CAMPOS FALTANTES
"""

from django.db import models
from django.utils import timezone
from gestionApp.models import Paciente, Matrona, Tens


# ============================================
# CATÁLOGOS PARA MATRONAAPP
# ============================================

class CatalogoViaAdministracion(models.Model):
    """Catálogo para vías de administración de medicamentos"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    class Meta:
        app_label = 'matronaApp'
        ordering = ['orden', 'nombre']
        verbose_name = "Catálogo Vía de Administración"
        verbose_name_plural = "Catálogo Vías de Administración"

    def __str__(self):
        return self.nombre


class CatalogoConsultorioOrigen(models.Model):
    """Catálogo de consultorios de origen"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    class Meta:
        app_label = 'matronaApp'
        ordering = ['orden', 'nombre']
        verbose_name = "Catálogo Consultorio Origen"
        verbose_name_plural = "Catálogo Consultorios Origen"

    def __str__(self):
        return self.nombre


# ============================================
# MODELO: FICHA OBSTÉTRICA (AMPLIADO)
# ============================================

class FichaObstetrica(models.Model):
    """
    Ficha obstétrica - Información de la gestante desde el ingreso
    ACTUALIZADO: Agregados todos los campos faltantes
    """
    
    # ============================================
    # RELACIONES
    # ============================================
    
    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='ficha_obstetrica',
        verbose_name='Paciente'
    )
    
    matrona_responsable = models.ForeignKey(
        Matrona,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_obstetrica',
        verbose_name='Matrona Responsable'
    )
    
    # ============================================
    # SECCIÓN 1: IDENTIFICACIÓN
    # ============================================
    
    numero_ficha = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Número de Ficha'
    )
    
    # ============================================
    # SECCIÓN 2: DATOS GENERALES DEL EMBARAZO
    # ============================================
    
    plan_de_parto = models.BooleanField(
        default=False,
        verbose_name='¿Tiene Plan de Parto?',
        help_text='¿La paciente presentó plan de parto?'
    )
    
    visita_guiada = models.BooleanField(
        default=False,
        verbose_name='¿Realizó Visita Guiada?',
        help_text='¿Hizo visita previa a la unidad?'
    )
    
    imc = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='IMC',
        help_text='Índice de Masa Corporal'
    )
    
    # ============================================
    # SECCIÓN: ACOMPAÑANTE
    # ============================================
    
    tiene_acompanante = models.BooleanField(
        default=False,
        verbose_name='¿Tiene Acompañante?'
    )
    
    nombre_acompanante = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nombre del Acompañante'
    )
    
    rut_acompanante = models.CharField(
        max_length=12,
        blank=True,
        verbose_name='RUT del Acompañante'
    )
    
    # ============================================
    # SECCIÓN: EXÁMENES VIH
    # ============================================
    
    # VIH 1
    vih_1_realizado = models.BooleanField(
        default=False,
        verbose_name='VIH 1 Realizado'
    )
    
    vih_1_fecha = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha VIH 1'
    )
    
    vih_1_resultado = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            ('', '---------'),
            ('NEGATIVO', 'Negativo'),
            ('POSITIVO', 'Positivo'),
            ('PENDIENTE', 'Pendiente'),
        ],
        verbose_name='Resultado VIH 1'
    )
    
    # VIH 2
    vih_2_realizado = models.BooleanField(
        default=False,
        verbose_name='VIH 2 Realizado'
    )
    
    vih_2_fecha = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha VIH 2'
    )
    
    vih_2_resultado = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            ('', '---------'),
            ('NEGATIVO', 'Negativo'),
            ('POSITIVO', 'Positivo'),
            ('PENDIENTE', 'Pendiente'),
        ],
        verbose_name='Resultado VIH 2'
    )
    
    # ============================================
    # SECCIÓN: CANTIDAD DE BEBÉS
    # ============================================
    
    cantidad_bebes = models.PositiveIntegerField(
        default=1,
        verbose_name='Cantidad de Bebés',
        help_text='Número de bebés en el vientre (1 = único, 2 = gemelos, etc.)'
    )
    
    # ============================================
    # SECCIÓN 3: CONSULTORIO DE ORIGEN
    # ============================================
    
    consultorio_origen = models.ForeignKey(
        CatalogoConsultorioOrigen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_obstetrica',
        verbose_name='Consultorio de Origen'
    )
    
    # ============================================
    # SECCIÓN 4: HISTORIA OBSTÉTRICA
    # ============================================
    
    numero_gestas = models.PositiveIntegerField(
        default=1,
        verbose_name='Número de Gestaciones',
        help_text='Embarazos anteriores + actual'
    )
    
    numero_partos = models.PositiveIntegerField(
        default=0,
        verbose_name='Número de Partos',
        help_text='Partos anteriores (vaginales + cesáreas)'
    )
    
    partos_vaginales = models.PositiveIntegerField(
        default=0,
        verbose_name='Partos Vaginales'
    )
    
    partos_cesareas = models.PositiveIntegerField(
        default=0,
        verbose_name='Partos por Cesárea'
    )
    
    numero_abortos = models.PositiveIntegerField(
        default=0,
        verbose_name='Número de Abortos'
    )
    
    nacidos_vivos = models.PositiveIntegerField(
        default=0,
        verbose_name='Nacidos Vivos'
    )
    
    # ============================================
    # SECCIÓN 5: EMBARAZO ACTUAL
    # ============================================
    
    fecha_ultima_regla = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha Última Menstruación (FUM)'
    )
    
    fecha_probable_parto = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha Probable de Parto (FPP)'
    )
    
    edad_gestacional_semanas = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Semanas de Gestación'
    )
    
    edad_gestacional_dias = models.PositiveIntegerField(
        default=0,
        verbose_name='Días Adicionales'
    )
    
    peso_actual = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Peso Actual (kg)'
    )
    
    talla_actual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Talla (cm)'
    )
    
    # ============================================
    # SECCIÓN 6: PATOLOGÍAS Y COMPLICACIONES
    # ============================================
    
    preeclampsia_severa = models.BooleanField(
        default=False,
        verbose_name='Preeclampsia Severa'
    )
    
    eclampsia = models.BooleanField(
        default=False,
        verbose_name='Eclampsia'
    )
    
    sepsis_infeccion_sistemia = models.BooleanField(
        default=False,
        verbose_name='Sepsis o Infección Sistémica Grave'
    )
    
    infeccion_ovular = models.BooleanField(
        default=False,
        verbose_name='Infección Ovular o Corioamnionitis'
    )
    
    otras_patologias = models.TextField(
        blank=True,
        verbose_name='Otras Patologías',
        help_text='Describir otras patologías presentes'
    )
    
    # ============================================
    # SECCIÓN 7: CONTROL PRENATAL
    # ============================================
    
    control_prenatal = models.BooleanField(
        default=True,
        verbose_name='¿Tuvo Control Prenatal?'
    )
    
    numero_controles = models.PositiveIntegerField(
        default=0,
        verbose_name='Número de Controles'
    )
    
    # ============================================
    # SECCIÓN 8: METADATA
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
        app_label = 'matronaApp'
        ordering = ['-fecha_creacion']
        verbose_name = 'Ficha Obstétrica'
        verbose_name_plural = 'Fichas Obstétricas'

    def __str__(self):
        return f"Ficha {self.numero_ficha} - {self.paciente.persona.Nombre}"


# ============================================
# MODELO: INGRESO DE PACIENTE
# ============================================

class IngresoPaciente(models.Model):
    """
    Registro de ingreso de paciente al módulo de matrona
    Se crea automáticamente cuando se crea una Ficha Obstétrica
    """
    
    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='ingreso_matrona',
        verbose_name='Paciente'
    )
    
    motivo_ingreso = models.CharField(
        max_length=500,
        verbose_name='Motivo de Ingreso'
    )
    
    fecha_ingreso = models.DateField(
        verbose_name='Fecha de Ingreso'
    )
    
    hora_ingreso = models.TimeField(
        verbose_name='Hora de Ingreso'
    )
    
    edad_gestacional_semanas = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Semanas de Gestación'
    )
    
    derivacion = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Derivación'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    numero_ficha = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Número de Ficha'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Registro Activo'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    class Meta:
        app_label = 'matronaApp'
        ordering = ['-fecha_ingreso']
        verbose_name = 'Ingreso de Paciente'
        verbose_name_plural = 'Ingresos de Paciente'
    
    def __str__(self):
        return f"Ingreso: {self.paciente.persona.Nombre} - {self.fecha_ingreso}"


# ============================================
# MODELO: MEDICAMENTO POR FICHA
# ============================================

class MedicamentoFicha(models.Model):
    """
    Medicamentos asignados a una ficha obstétrica
    """
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='medicamentos',
        verbose_name='Ficha Obstétrica'
    )
    
    medicamento = models.CharField(
        max_length=200,
        verbose_name='Nombre del Medicamento'
    )
    
    dosis = models.CharField(
        max_length=100,
        verbose_name='Dosis'
    )
    
    via_administracion = models.ForeignKey(
        CatalogoViaAdministracion,
        on_delete=models.PROTECT,
        verbose_name='Vía de Administración'
    )
    
    frecuencia = models.CharField(
        max_length=100,
        verbose_name='Frecuencia',
        help_text='Ej: Cada 6 horas, Cada 8 horas, etc.'
    )
    
    fecha_inicio = models.DateTimeField(
        verbose_name='Fecha y Hora de Inicio'
    )
    
    fecha_termino = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha y Hora de Término'
    )
    
    indicaciones = models.TextField(
        blank=True,
        verbose_name='Indicaciones Especiales'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Medicamento Activo'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        app_label = 'matronaApp'
        ordering = ['-fecha_creacion']
        verbose_name = 'Medicamento en Ficha'
        verbose_name_plural = 'Medicamentos en Ficha'

    def __str__(self):
        return f"{self.medicamento} - {self.ficha.numero_ficha}"


# ============================================
# MODELO: ADMINISTRACIÓN DE MEDICAMENTO
# ============================================

class AdministracionMedicamento(models.Model):
    """
    Registro de administración de medicamentos a la paciente
    """
    
    medicamento_ficha = models.ForeignKey(
        MedicamentoFicha,
        on_delete=models.CASCADE,
        related_name='administraciones',
        verbose_name='Medicamento'
    )
    
    tens = models.ForeignKey(
        Tens,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medicamentos_administrados',
        verbose_name='TENS Responsable'
    )
    
    fecha_hora_administracion = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Administración'
    )
    
    lote = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Lote del Medicamento'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    class Meta:
        app_label = 'matronaApp'
        ordering = ['-fecha_hora_administracion']
        verbose_name = 'Administración de Medicamento'
        verbose_name_plural = 'Administraciones de Medicamento'

    def __str__(self):
        return f"{self.medicamento_ficha.medicamento} - {self.fecha_hora_administracion}"