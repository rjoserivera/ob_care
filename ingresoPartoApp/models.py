"""
ingresoPartoApp/models.py
Modelo para Ingreso a Parto (Evaluación en sala de parto)
MEJORADO: Con catálogos adicionales para campos seleccionables
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# ============================================
# CATÁLOGOS EXISTENTES
# ============================================

class CatalogoEstadoCervical(models.Model):
    """Estado cervical en ingreso"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['orden', 'nombre']
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
    orden = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['orden', 'nombre']
        verbose_name = 'Estado Fetal'
        verbose_name_plural = 'Estados Fetales'
    
    def __str__(self):
        return self.nombre


# ============================================
# NUEVOS CATÁLOGOS
# ============================================

class CatalogoPosicionFetal(models.Model):
    """Posición fetal al ingreso"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['orden', 'nombre']
        verbose_name = 'Posición Fetal'
        verbose_name_plural = 'Posiciones Fetales'
    
    def __str__(self):
        return self.nombre


class CatalogoAlturaPresentacion(models.Model):
    """Altura de presentación (planos de Hodge)"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    valor_numerico = models.CharField(max_length=10, blank=True)  # -4 a +4
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['orden', 'nombre']
        verbose_name = 'Altura de Presentación'
        verbose_name_plural = 'Alturas de Presentación'
    
    def __str__(self):
        if self.valor_numerico:
            return f"{self.nombre} ({self.valor_numerico})"
        return self.nombre


class CatalogoCaracteristicasLiquido(models.Model):
    """Características del líquido amniótico"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    es_patologico = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['orden', 'nombre']
        verbose_name = 'Característica Líquido Amniótico'
        verbose_name_plural = 'Características Líquido Amniótico'
    
    def __str__(self):
        return self.nombre


class CatalogoResultadoCTG(models.Model):
    """Resultado de cardiotocografía"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    requiere_accion = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['orden', 'nombre']
        verbose_name = 'Resultado CTG'
        verbose_name_plural = 'Resultados CTG'
    
    def __str__(self):
        return self.nombre


class CatalogoResultadoExamen(models.Model):
    """Resultados de exámenes (VIH, SGB, VDRL, HepB)"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['orden', 'nombre']
        verbose_name = 'Resultado de Examen'
        verbose_name_plural = 'Resultados de Exámenes'
    
    def __str__(self):
        return self.nombre


class CatalogoSalaAsignada(models.Model):
    """Salas disponibles para parto"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True)  # Parto, Quirófano, Urgencias
    capacidad = models.IntegerField(default=1)
    activo = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['nombre']
        verbose_name = 'Sala Asignada'
        verbose_name_plural = 'Salas Asignadas'
    
    def __str__(self):
        return self.nombre

class CatalogoDerivacion(models.Model):
    """Catálogo de lugares o especialidades de derivación"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'ingresoPartoApp'
        ordering = ['orden', 'nombre']
        verbose_name = 'Lugar de Derivación'
        verbose_name_plural = 'Lugares de Derivación'
    
    def __str__(self):
        return self.nombre


# ============================================
# MODELO: FICHA DE PARTO (INGRESO) - MEJORADO
# ============================================

class FichaParto(models.Model):
# ... (existing fields) ...
    """
    Ficha de ingreso a parto - Evaluación inicial en sala de parto
    MEJORADO: Con FKs a catálogos para campos seleccionables
    """
    
    RESULTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('NEGATIVO', 'Negativo'),
        ('POSITIVO', 'Positivo'),
        ('INDETERMINADO', 'Indeterminado'),
    ]
    
    # ============================================
    # RELACIONES
    # ============================================
    
    ficha_obstetrica = models.OneToOneField(
        'matronaApp.FichaObstetrica',
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
    
    sala_asignada = models.ForeignKey(
        CatalogoSalaAsignada,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Sala Asignada'
    )
    
    # ============================================
    # DATOS DE INGRESO
    # ============================================
    
    fecha_ingreso = models.DateField(
        verbose_name='Fecha de Ingreso'
    )
    
    hora_ingreso = models.TimeField(
        verbose_name='Hora de Ingreso'
    )
    
    edad_gestacional_semanas = models.PositiveIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(45)],
        null=True,
        blank=True,
        verbose_name='Semanas de Gestación'
    )
    
    edad_gestacional_dias = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(6)],
        verbose_name='Días Adicionales'
    )
    
    # ============================================
    # EVALUACIÓN CERVICAL
    # ============================================
    
    dilatacion_cervical_cm = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
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
    
    borramiento = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        null=True,
        blank=True,
        verbose_name='Borramiento (%)'
    )
    
    # ============================================
    # EVALUACIÓN FETAL (CON CATÁLOGOS)
    # ============================================
    
    posicion_fetal = models.ForeignKey(
        CatalogoPosicionFetal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Posición Fetal'
    )
    
    altura_presentacion = models.ForeignKey(
        CatalogoAlturaPresentacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Altura de Presentación'
    )
    
    estado_fetal = models.ForeignKey(
        CatalogoEstadoFetal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Estado Fetal'
    )
    
    frecuencia_cardiaca_fetal = models.PositiveIntegerField(
        validators=[MinValueValidator(60), MaxValueValidator(220)],
        null=True,
        blank=True,
        verbose_name='Frecuencia Cardíaca Fetal (lpm)'
    )
    
    # ============================================
    # MEMBRANAS Y LÍQUIDO AMNIÓTICO
    # ============================================
    
    membranas_rotas = models.BooleanField(
        default=False,
        verbose_name='Membranas Rotas'
    )
    
    tiempo_ruptura_horas = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Tiempo de Ruptura (horas)'
    )
    
    caracteristicas_liquido = models.ForeignKey(
        CatalogoCaracteristicasLiquido,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Características Líquido Amniótico'
    )
    
    # ============================================
    # CARDIOTOCOGRAFÍA (CTG)
    # ============================================
    
    cardiotocografia_realizada = models.BooleanField(
        default=False,
        verbose_name='CTG Realizada'
    )
    
    resultado_ctg = models.ForeignKey(
        CatalogoResultadoCTG,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Resultado CTG'
    )
    
    observacion_ctg = models.TextField(
        blank=True,
        verbose_name='Observaciones CTG'
    )
    
    # ============================================
    # SIGNOS VITALES MATERNOS
    # ============================================
    
    presion_arterial_sistolica = models.PositiveIntegerField(
        validators=[MinValueValidator(60), MaxValueValidator(250)],
        null=True,
        blank=True,
        verbose_name='PA Sistólica (mmHg)'
    )
    
    presion_arterial_diastolica = models.PositiveIntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(150)],
        null=True,
        blank=True,
        verbose_name='PA Diastólica (mmHg)'
    )
    
    frecuencia_cardiaca_materna = models.PositiveIntegerField(
        validators=[MinValueValidator(40), MaxValueValidator(200)],
        null=True,
        blank=True,
        verbose_name='FC Materna (lpm)'
    )
    
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(34), MaxValueValidator(42)],
        null=True,
        blank=True,
        verbose_name='Temperatura (°C)'
    )
    
    saturacion_oxigeno = models.PositiveIntegerField(
        validators=[MinValueValidator(70), MaxValueValidator(100)],
        null=True,
        blank=True,
        verbose_name='Saturación O2 (%)'
    )
    
    # ============================================
    # EXÁMENES DE LABORATORIO
    # ============================================
    
    # VIH
    vih_tomado_prepartos = models.BooleanField(
        default=False,
        verbose_name='VIH Tomado en Prepartos'
    )
    
    vih_tomado_sala = models.BooleanField(
        default=False,
        verbose_name='VIH Tomado en Sala'
    )
    
    vih_resultado = models.CharField(
        max_length=20,
        choices=RESULTADO_CHOICES,
        default='PENDIENTE',
        verbose_name='Resultado VIH'
    )
    
    # SGB (Streptococcus Grupo B)
    sgb_pesquisa = models.BooleanField(
        default=False,
        verbose_name='Pesquisa SGB Realizada'
    )
    
    sgb_resultado = models.CharField(
        max_length=20,
        choices=RESULTADO_CHOICES,
        default='PENDIENTE',
        verbose_name='Resultado SGB'
    )
    
    antibiotico_sgb = models.BooleanField(
        default=False,
        verbose_name='Antibiótico SGB Administrado'
    )
    
    # VDRL
    vdrl_resultado = models.CharField(
        max_length=20,
        choices=RESULTADO_CHOICES,
        default='PENDIENTE',
        verbose_name='Resultado VDRL'
    )
    
    tratamiento_sifilis = models.BooleanField(
        default=False,
        verbose_name='Tratamiento Sífilis Completo'
    )
    
    # Hepatitis B
    hepatitis_b_tomado = models.BooleanField(
        default=False,
        verbose_name='Hepatitis B Tomado'
    )
    
    hepatitis_b_resultado = models.CharField(
        max_length=20,
        choices=RESULTADO_CHOICES,
        default='PENDIENTE',
        verbose_name='Resultado Hepatitis B'
    )

    derivacion_hepatitis_b = models.ForeignKey(
        CatalogoDerivacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Derivación Especialista (Hep B)'
    )
    
    # ============================================
    # PATOLOGÍAS ACTIVAS
    # ============================================
    
    preeclampsia_severa = models.BooleanField(
        default=False,
        verbose_name='Preeclampsia Severa'
    )
    
    eclampsia = models.BooleanField(
        default=False,
        verbose_name='Eclampsia'
    )
    
    sepsis_infeccion_grave = models.BooleanField(
        default=False,
        verbose_name='Sepsis / Infección Grave'
    )
    
    infeccion_ovular = models.BooleanField(
        default=False,
        verbose_name='Infección Ovular / Corioamnionitis'
    )
    
    otras_patologias = models.TextField(
        blank=True,
        verbose_name='Otras Patologías'
    )
    
    # ============================================
    # DIAGNÓSTICO Y OBSERVACIONES
    # ============================================
    
    diagnostico_ingreso = models.TextField(
        blank=True,
        verbose_name='Diagnóstico de Ingreso'
    )
    
    plan_de_manejo = models.TextField(
        blank=True,
        verbose_name='Plan de Manejo'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    # ============================================
    # CONTROL Y ESTADO
    # ============================================
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True
    )
    
    creado_por = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_parto_creadas',
        verbose_name='Creado Por'
    )
    
    # ============================================
    # PROPIEDADES
    # ============================================
    
    @property
    def presion_arterial(self):
        """Retorna PA formateada"""
        if self.presion_arterial_sistolica and self.presion_arterial_diastolica:
            return f"{self.presion_arterial_sistolica}/{self.presion_arterial_diastolica}"
        return "N/R"
    
    @property
    def edad_gestacional_display(self):
        """Retorna edad gestacional formateada"""
        semanas = self.edad_gestacional_semanas or 0
        dias = self.edad_gestacional_dias or 0
        return f"{semanas}+{dias} semanas"
    
    @property
    def tiene_patologia_activa(self):
        """Verifica si tiene alguna patología activa"""
        return (self.preeclampsia_severa or self.eclampsia or 
                self.sepsis_infeccion_grave or self.infeccion_ovular)
    
    # ============================================
    # PIN DE INICIO DE PARTO (NUEVO)
    # ============================================
    
    pin_inicio_parto = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name="PIN de Inicio de Parto",
        help_text="PIN generado automáticamente para iniciar el proceso de parto"
    )
    
    pin_generado_en = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de Generación del PIN"
    )
    
    def __str__(self):
        return f"Ficha Parto {self.numero_ficha_parto}"
    
    class Meta:
        app_label = 'ingresoPartoApp'
        verbose_name = 'Ficha de Parto (Ingreso)'
        verbose_name_plural = 'Fichas de Parto (Ingreso)'
        ordering = ['-fecha_ingreso', '-hora_ingreso']
        indexes = [
            models.Index(fields=['numero_ficha_parto']),
            models.Index(fields=['-fecha_ingreso']),
        ]


# ============================================
# MODELO: BEBÉ ESPERADO (NUEVO)
# ============================================

class BebeEsperado(models.Model):
    """Información de cada bebé esperado en el parto"""
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('I', 'Indeterminado'),
    ]
    
    ficha_parto = models.ForeignKey(
        FichaParto,
        on_delete=models.CASCADE,
        related_name='bebes_esperados',
        verbose_name='Ficha de Parto'
    )
    
    numero_bebe = models.PositiveIntegerField(
        default=1,
        verbose_name='Número de Bebé'
    )
    
    sexo_esperado = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        blank=True,
        verbose_name='Sexo Esperado'
    )
    
    peso_estimado = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Peso Estimado (gr)'
    )
    
    posicion_fetal = models.ForeignKey(
        CatalogoPosicionFetal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Posición Fetal'
    )
    
    frecuencia_cardiaca = models.PositiveIntegerField(
        validators=[MinValueValidator(60), MaxValueValidator(220)],
        null=True,
        blank=True,
        verbose_name='FCF (lpm)'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    def __str__(self):
        return f"Bebé #{self.numero_bebe} - {self.ficha_parto.numero_ficha_parto}"
    
    class Meta:
        app_label = 'ingresoPartoApp'
        verbose_name = 'Bebé Esperado'
        verbose_name_plural = 'Bebés Esperados'
        ordering = ['ficha_parto', 'numero_bebe']
        unique_together = ['ficha_parto', 'numero_bebe']