"""
recienNacidoApp/models.py
Modelos para recién nacido - Datos completos del RN después del parto
VERSIÓN FINAL:
- Un solo catálogo: CatalogoSexoRN
- Varios recién nacidos por parto (FK → RegistroParto)
- DocumentosParto asociados 1 a 1 a cada RN
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# ============================================
# CATÁLOGO SEXO RECIÉN NACIDO
# ============================================

class CatalogoSexoRN(models.Model):
    """Catálogo para sexo del recién nacido"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_sexo_rn'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Sexo RN'
        verbose_name_plural = 'Catálogo Sexo RN'

    def __str__(self):
        return self.descripcion


class CatalogoComplicacionesRN(models.Model):
    """Catálogo de complicaciones del recién nacido"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_complicaciones_rn'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Complicaciones RN'
        verbose_name_plural = 'Catálogo Complicaciones RN'

    def __str__(self):
        return self.descripcion


class CatalogoMotivoHospitalizacionRN(models.Model):
    """Catálogo para motivos de hospitalización del recién nacido"""
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=150)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_motivo_hospitalizacion_rn'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Motivo Hospitalización RN'
        verbose_name_plural = 'Catálogo Motivos Hospitalización RN'

    def __str__(self):
        return self.descripcion


# ============================================
# REGISTRO DE RECIÉN NACIDO
# ============================================

class RegistroRecienNacido(models.Model):
    """
    Registro completo del recién nacido
    - Relación: varios RN por cada RegistroParto
    """

    # ==========================
    # RELACIÓN CON PARTO
    # ==========================

    registro_parto = models.ForeignKey(
        'partosApp.RegistroParto',
        on_delete=models.CASCADE,
        related_name='recien_nacidos',   # <- varios RN por parto
        verbose_name='Registro de Parto'
    )

    matrona_responsable = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Matrona Responsable'
    )

    tens_responsable = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='TENS Responsable'
    )

    # ==========================
    # SECCIÓN 1: DATOS RN
    # ==========================

    sexo = models.ForeignKey(
        CatalogoSexoRN,
        on_delete=models.PROTECT,
        verbose_name='Sexo'
    )

    peso_gramos = models.PositiveIntegerField(
        validators=[MinValueValidator(500), MaxValueValidator(6000)],
        verbose_name='Peso (gramos)'
    )

    talla_centimetros = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(30), MaxValueValidator(60)],
        verbose_name='Talla (cm)'
    )

    perimetro_cefalico = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Perímetro Cefálico (cm)'
    )

    perimetro_torax = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Perímetro Torácico (cm)'
    )

    # ==========================
    # SECCIÓN 2: APGAR
    # ==========================

    apgar_1_minuto = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar al 1 Minuto'
    )

    apgar_5_minutos = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar a los 5 Minutos'
    )

    apgar_10_minutos = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
        verbose_name='Apgar a los 10 Minutos',
        help_text='Si es necesario evaluar nuevamente'
    )

    # ==========================
    # SECCIÓN 3: CORDÓN
    # ==========================

    ligadura_tardia_cordon = models.BooleanField(
        default=False,
        verbose_name='Ligadura Tardía del Cordón (>1 minuto)',
        help_text='Pinzamiento tardío del cordón'
    )

    tiempo_ligadura_minutos = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name='Tiempo de Ligadura (minutos)',
        help_text='Minutos después del nacimiento'
    )

    numero_vasos_cordon = models.PositiveIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name='Número de Vasos Umbilicales',
        help_text='Normalmente 3 (2 arterias, 1 vena)'
    )

    # ==========================
    # SECCIÓN 4: APEGO / ACOMPAÑAMIENTO
    # ==========================

    tiempo_primer_apego_minutos = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name='Tiempo del Primer Apego (minutos)',
        help_text='Minutos entre nacimiento y primer contacto piel con piel'
    )

    apego_piel_con_piel = models.BooleanField(
        default=False,
        verbose_name='Apego Piel con Piel',
        help_text='¿Se realizó contacto piel con piel directo?'
    )

    apego_canguro = models.BooleanField(
        default=False,
        verbose_name='Apego Canguro',
        help_text='¿Se realizó método canguro?'
    )

    duracion_apego_canguro_minutos = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name='Duración Apego Canguro (minutos)'
    )

    acompanamiento_madre = models.BooleanField(
        default=False,
        verbose_name='¿Acompañamiento Continuo Madre?'
    )

    acompanamiento_acompanante = models.BooleanField(
        default=False,
        verbose_name='¿Acompañamiento de Acompañante?'
    )

    acompanante_secciona_cordon = models.BooleanField(
        default=False,
        verbose_name='¿Acompañante Secciona Cordón?'
    )

    # ==========================
    # SECCIÓN 5: ALIMENTACIÓN
    # ==========================

    lactancia_iniciada = models.BooleanField(
        default=False,
        verbose_name='¿Lactancia Iniciada?'
    )

    tiempo_inicio_lactancia_minutos = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name='Tiempo Inicio Lactancia (minutos)',
        help_text='Minutos después del nacimiento'
    )

    alimentacion_con_formula = models.BooleanField(
        default=False,
        verbose_name='¿Alimentación con Fórmula?',
        help_text='Si es que fue necesario'
    )

    razon_formula = models.TextField(
        blank=True,
        verbose_name='Razón de Alimentación con Fórmula',
        help_text='Justificación si aplica'
    )

    # ==========================
    # SECCIÓN 6: EVALUACIONES
    # ==========================

    examen_fisico_completo = models.BooleanField(
        default=False,
        verbose_name='Examen Físico Completo Realizado'
    )

    screening_metabolico = models.BooleanField(
        default=False,
        verbose_name='Screening Metabólico Realizado'
    )

    vacuna_hepatitis_b = models.BooleanField(
        default=False,
        verbose_name='¿Vacuna Hepatitis B Administrada?'
    )

    profilaxis_oftalmologica = models.BooleanField(
        default=False,
        verbose_name='¿Profilaxis Oftalmológica Realizada?'
    )

    vitamina_k = models.BooleanField(
        default=False,
        verbose_name='¿Vitamina K Administrada?'
    )

    # ==========================
    # SECCIÓN 7: COMPLICACIONES
    # ==========================

    traumatismo_obstetrico = models.BooleanField(
        default=False,
        verbose_name='¿Traumatismo Obstétrico?'
    )

    descripcion_traumatismo = models.TextField(
        blank=True,
        verbose_name='Descripción del Traumatismo'
    )

    dificultad_respiratoria = models.BooleanField(
        default=False,
        verbose_name='¿Dificultad Respiratoria?'
    )

    hipoglucemia = models.BooleanField(
        default=False,
        verbose_name='¿Hipoglucemia?'
    )

    hipotermia = models.BooleanField(
        default=False,
        verbose_name='¿Hipotermia?'
    )

    ictericia = models.BooleanField(
        default=False,
        verbose_name='¿Ictericia?'
    )

    otras_complicaciones = models.TextField(
        blank=True,
        verbose_name='Otras Complicaciones'
    )

    complicaciones_seleccionadas = models.ManyToManyField(
        CatalogoComplicacionesRN,
        blank=True,
        verbose_name='Complicaciones (Selección Multiple)',
        related_name='registros_rn'
    )

    requiere_hospitalizacion = models.BooleanField(
        default=False,
        verbose_name='¿Requiere Hospitalización?'
    )

    motivo_hospitalizacion = models.ForeignKey(
        CatalogoMotivoHospitalizacionRN,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Motivo de Hospitalización',
        help_text='Si aplica'
    )

    # ==========================
    # SECCIÓN 8: FECHA / HORA
    # ==========================

    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento'
    )

    hora_nacimiento = models.TimeField(
        verbose_name='Hora de Nacimiento'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación del Registro'
    )

    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Modificación'
    )

    activo = models.BooleanField(
        default=True,
        verbose_name='Registro Activo'
    )

    class Meta:
        ordering = ['-fecha_nacimiento']
        verbose_name = 'Registro de Recién Nacido'
        verbose_name_plural = 'Registros de Recién Nacido'
        indexes = [
            models.Index(fields=['registro_parto', '-fecha_nacimiento']),
            models.Index(fields=['-fecha_nacimiento']),
        ]

    def __str__(self):
        return f"RN {self.id} - {self.fecha_nacimiento} {self.hora_nacimiento}"

    # ==========================
    # MÉTODOS DE APOYO
    # ==========================

    def es_prematuro(self):
        """Prematuro si EG < 37 semanas (usa RegistroParto)"""
        return self.registro_parto.edad_gestacional_semanas < 37

    def es_postmaduro(self):
        """Postmaduro si EG > 42 semanas"""
        return self.registro_parto.edad_gestacional_semanas > 42

    def peso_bajo_al_nacer(self):
        """Menos de 2500g"""
        return self.peso_gramos < 2500

    def peso_muy_bajo(self):
        """Menos de 1500g"""
        return self.peso_gramos < 1500

    def apgar_bajo(self):
        """Apgar 5' < 7"""
        return self.apgar_5_minutos < 7


# ============================================
# DOCUMENTOS DEL PARTO ASOCIADOS AL RN
# ============================================

class DocumentosParto(models.Model):
    """
    Documentos relacionados con el RN:
    - Registro Civil
    - Carné de salud
    - Observaciones
    """

    registro_recien_nacido = models.OneToOneField(
        RegistroRecienNacido,
        on_delete=models.CASCADE,
        related_name='documentos_parto',
        verbose_name='Registro Recién Nacido'
    )

    # Registro Civil
    folio_valido = models.BooleanField(
        default=False,
        verbose_name='¿Folio Válido?'
    )

    numero_folio = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Número de Folio'
    )

    folios_nulos = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Folios Nulos',
        help_text='Números de folios que resultaron nulos'
    )

    fecha_folio = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha del Folio'
    )

    # Otros documentos
    carne_de_salud = models.BooleanField(
        default=False,
        verbose_name='¿Carné de Salud Entregado?'
    )

    derivacion_registro_civil = models.BooleanField(
        default=False,
        verbose_name='¿Derivación a Registro Civil Realizada?'
    )

    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones sobre Documentación'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Documentos del Parto'
        verbose_name_plural = 'Documentos del Parto'

    def __str__(self):
        return f"Documentos RN {self.registro_recien_nacido.id}"
