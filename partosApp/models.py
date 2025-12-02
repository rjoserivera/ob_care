# ============================================
# partosApp/models.py
# VERSIÓN SIN CHOICES - FK A TABLAS CATÁLOGO
# ============================================

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# ============================================
# TABLAS CATÁLOGO PARA partosApp
# ============================================

class CatalogoVihSala(models.Model):
    """Catálogo para VIH tomado en sala"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_vih_sala'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo VIH Sala'
        verbose_name_plural = 'Catálogo VIH Sala'

    def __str__(self):
        return self.descripcion


class CatalogoRoturaMembrana(models.Model):
    """Catálogo para tipos de rotura de membrana"""
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_rotura_membrana'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Rotura Membrana'
        verbose_name_plural = 'Catálogo Rotura Membrana'

    def __str__(self):
        return self.descripcion


class CatalogoRegimen(models.Model):
    """Catálogo para tipos de régimen en trabajo de parto"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_regimen'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Régimen'
        verbose_name_plural = 'Catálogo Régimen'

    def __str__(self):
        return self.descripcion


class CatalogoTipoParto(models.Model):
    """Catálogo para tipos de parto"""
    codigo = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_tipo_parto'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Tipo de Parto'
        verbose_name_plural = 'Catálogo Tipos de Parto'

    def __str__(self):
        return self.descripcion


class CatalogoClasificacionRobson(models.Model):
    """Catálogo para clasificación de Robson (12 grupos)"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_clasificacion_robson'
        ordering = ['orden', 'codigo']
        verbose_name = 'Catálogo Clasificación Robson'
        verbose_name_plural = 'Catálogo Clasificación Robson'

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class CatalogoPosicionParto(models.Model):
    """Catálogo para posiciones maternas durante el parto"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_posicion_parto'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Posición Parto'
        verbose_name_plural = 'Catálogo Posiciones Parto'

    def __str__(self):
        return self.descripcion


class CatalogoEstadoPerine(models.Model):
    """Catálogo para estados del periné post-parto"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_estado_perine'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Estado Periné'
        verbose_name_plural = 'Catálogo Estados Periné'

    def __str__(self):
        return self.descripcion


class CatalogoSangradoPostparto(models.Model):
    """Catálogo para niveles de sangrado postparto"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_sangrado_postparto'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Sangrado Postparto'
        verbose_name_plural = 'Catálogo Sangrado Postparto'

    def __str__(self):
        return self.descripcion


# ============================================
# MODELO PRINCIPAL: REGISTRO DE PARTO
# ============================================

class RegistroParto(models.Model):
    """
    Registro del proceso de parto
    SIN CHOICES - Usa FK a tablas catálogo
    """

    # ============================================
    # RELACIONES
    # ============================================
    
    ficha = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.PROTECT,
        related_name='registros_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    ficha_ingreso = models.OneToOneField(
        'ingresoPartoApp.FichaParto',
        on_delete=models.PROTECT,
        related_name='registro_parto',
        null=True,
        blank=True,
        verbose_name='Ficha de Ingreso',
        help_text='Vincula con la ficha de ingreso'
    )
    
    numero_registro = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Registro',
        help_text='Se genera automáticamente: PARTO-000001'
    )
    
    # ============================================
    # FECHAS Y HORAS
    # ============================================
    
    fecha_hora_admision = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Admisión',
        help_text='Cuando ingresa para el parto'
    )
    
    fecha_hora_parto = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha y Hora del Parto',
        help_text='Momento exacto del nacimiento'
    )
    
    # ============================================
    # SECCIÓN 1: TRABAJO DE PARTO
    # ============================================
    
    vih_tomado_prepartos = models.BooleanField(
        default=False,
        verbose_name='VIH tomado en Prepartos',
        help_text='¿Se tomó VIH al ingresar a prepartos?'
    )
    
    # FK a catálogo (antes era CHOICES)
    vih_sala = models.ForeignKey(
        CatalogoVihSala,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_parto',
        verbose_name='VIH tomado en Sala',
        help_text='Sala donde se tomó el VIH (si aplica)'
    )
    
    @property
    def vih_tomado_sala(self):
        """Alias para compatibilidad con código existente"""
        return self.vih_sala.codigo if self.vih_sala else None
    
    # Edad Gestacional
    edad_gestacional_semanas = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(42)],
        verbose_name='Semanas de Embarazo',
        help_text='Semanas completas al momento del parto'
    )
    
    edad_gestacional_dias = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        verbose_name='Días adicionales',
        help_text='Ej: 38 semanas y 4 días'
    )
    
    # Monitoreo
    monitor_ttc = models.BooleanField(
        default=False,
        verbose_name='Monitor TTC',
        help_text='¿Se usó monitor de contracciones?'
    )
    
    induccion = models.BooleanField(
        default=False,
        verbose_name='Inducción',
        help_text='¿Se indujo el parto?'
    )
    
    aceleracion_correccion = models.BooleanField(
        default=False,
        verbose_name='Aceleración o Corrección',
        help_text='¿Se aceleró el trabajo de parto?'
    )
    
    numero_tactos_vaginales = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Número de Tactos Vaginales (TV)',
        help_text='Número total de exámenes vaginales realizados'
    )
    
    # FK a catálogo (antes era CHOICES)
    rotura_membrana_catalogo = models.ForeignKey(
        CatalogoRoturaMembrana,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_parto',
        verbose_name='Rotura de Membrana'
    )
    
    @property
    def rotura_membrana(self):
        """Alias para compatibilidad"""
        return self.rotura_membrana_catalogo.codigo if self.rotura_membrana_catalogo else None
    
    tiempo_membranas_rotas = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Membranas Rotas (minutos)',
        help_text='Tiempo transcurrido con membranas rotas'
    )
    
    # Tiempos del Parto
    tiempo_dilatacion = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Dilatación (minutos)',
        help_text='Duración de la fase de dilatación'
    )
    
    tiempo_expulsivo = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Expulsivo (minutos)',
        help_text='Duración de la fase expulsiva'
    )
    
    # ============================================
    # SECCIÓN 2: INFORMACIÓN DEL PARTO
    # ============================================
    
    libertad_movimiento = models.BooleanField(
        default=True,
        verbose_name='Libertad de Movimiento en Trabajo de Parto',
        help_text='¿La paciente tuvo libertad de movimiento?'
    )
    
    # FK a catálogo (antes era CHOICES)
    tipo_regimen_catalogo = models.ForeignKey(
        CatalogoRegimen,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_parto',
        verbose_name='Tipo de Régimen en Trabajo de Parto'
    )
    
    @property
    def tipo_regimen(self):
        """Alias para compatibilidad"""
        return self.tipo_regimen_catalogo.codigo if self.tipo_regimen_catalogo else None
    
    # FK a catálogo (antes era CHOICES)
    tipo_parto_catalogo = models.ForeignKey(
        CatalogoTipoParto,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_parto',
        verbose_name='Tipo de Parto'
    )
    
    @property
    def tipo_parto(self):
        """Alias para compatibilidad"""
        return self.tipo_parto_catalogo.codigo if self.tipo_parto_catalogo else None
    
    alumbramiento_dirigido = models.BooleanField(
        default=True,
        verbose_name='Alumbramiento Dirigido',
        help_text='¿Se realizó alumbramiento dirigido?'
    )
    
    # FK a catálogo (antes era CHOICES)
    clasificacion_robson_catalogo = models.ForeignKey(
        CatalogoClasificacionRobson,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_parto',
        verbose_name='Clasificación de Robson',
        help_text='Clasificación de Robson para cesáreas'
    )
    
    @property
    def clasificacion_robson(self):
        """Alias para compatibilidad"""
        return self.clasificacion_robson_catalogo.codigo if self.clasificacion_robson_catalogo else None
    
    # FK a catálogo (antes era CHOICES)
    posicion_materna_catalogo = models.ForeignKey(
        CatalogoPosicionParto,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_parto',
        verbose_name='Posición Materna en el Parto'
    )
    
    @property
    def posicion_materna_parto(self):
        """Alias para compatibilidad"""
        return self.posicion_materna_catalogo.codigo if self.posicion_materna_catalogo else None
    
    ofrecimiento_posiciones_alternativas = models.BooleanField(
        default=True,
        verbose_name='Ofrecimiento de Posiciones Alternativas del Parto',
        help_text='¿Se ofrecieron posiciones alternativas?'
    )
    
    # ============================================
    # SECCIÓN 3: PUERPERIO
    # ============================================
    
    # FK a catálogo (antes era CHOICES)
    estado_perine_catalogo = models.ForeignKey(
        CatalogoEstadoPerine,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_parto',
        verbose_name='Estado del Periné'
    )
    
    @property
    def estado_perine(self):
        """Alias para compatibilidad"""
        return self.estado_perine_catalogo.codigo if self.estado_perine_catalogo else None
    
    esterilizacion = models.BooleanField(
        default=False,
        verbose_name='Esterilización',
        help_text='¿Se realizó esterilización?'
    )
    
    revision = models.BooleanField(
        default=True,
        verbose_name='Revisión del Canal del Parto'
    )
    
    # Complicaciones del Puerperio
    inercia_uterina = models.BooleanField(
        default=False,
        verbose_name='Inercia Uterina'
    )
    
    restos_placentarios = models.BooleanField(
        default=False,
        verbose_name='Restos Placentarios'
    )
    
    trauma = models.BooleanField(
        default=False,
        verbose_name='Trauma'
    )
    
    alteracion_coagulacion = models.BooleanField(
        default=False,
        verbose_name='Alteración de la Coagulación'
    )
    
    manejo_quirurgico_inercia = models.BooleanField(
        default=False,
        verbose_name='Manejo Quirúrgico de Inercia Uterina'
    )
    
    histerectomia_obstetrica = models.BooleanField(
        default=False,
        verbose_name='Histerectomía Obstétrica'
    )
    
    transfusion_sanguinea = models.BooleanField(
        default=False,
        verbose_name='Transfusión Sanguínea'
    )
    
    # Contacto y lactancia
    contacto_piel_piel = models.BooleanField(
        default=False,
        verbose_name='Contacto Piel a Piel'
    )
    
    lactancia_primera_hora = models.BooleanField(
        default=False,
        verbose_name='Lactancia en la Primera Hora'
    )
    
    apego_precoz = models.BooleanField(
        default=False,
        verbose_name='Apego Precoz'
    )
    
    # FK a catálogo (antes era CHOICES)
    sangrado_postparto_catalogo = models.ForeignKey(
        CatalogoSangradoPostparto,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='registros_parto',
        verbose_name='Sangrado Postparto'
    )
    
    @property
    def sangrado_postparto(self):
        """Alias para compatibilidad"""
        return self.sangrado_postparto_catalogo.codigo if self.sangrado_postparto_catalogo else None
    
    hemorragia_postparto = models.BooleanField(
        default=False,
        verbose_name='Hemorragia Postparto'
    )
    
    retencion_placentaria = models.BooleanField(
        default=False,
        verbose_name='Retención Placentaria'
    )
    
    # ============================================
    # SECCIÓN 4: ANESTESIA Y ANALGESIA
    # ============================================
    
    anestesia_neuroaxial = models.BooleanField(
        default=False,
        verbose_name='Anestesia Neuroaxial'
    )
    
    oxido_nitroso = models.BooleanField(
        default=False,
        verbose_name='Óxido Nitroso'
    )
    
    analgesia_endovenosa = models.BooleanField(
        default=False,
        verbose_name='Analgesia Endovenosa'
    )
    
    anestesia_general = models.BooleanField(
        default=False,
        verbose_name='Anestesia General'
    )
    
    anestesia_local = models.BooleanField(
        default=False,
        verbose_name='Anestesia Local'
    )
    
    analgesia_no_farmacologica = models.BooleanField(
        default=False,
        verbose_name='Analgesia No Farmacológica'
    )
    
    # Métodos no farmacológicos
    balon_kinesico = models.BooleanField(
        default=False,
        verbose_name='Balón Kinésico'
    )
    
    lenteja_parto = models.BooleanField(
        default=False,
        verbose_name='Lenteja de Parto'
    )
    
    rebozo = models.BooleanField(
        default=False,
        verbose_name='Rebozo'
    )
    
    aromaterapia = models.BooleanField(
        default=False,
        verbose_name='Aromaterapia'
    )
    
    # Peridural
    peridural_solicitada_paciente = models.BooleanField(
        default=False,
        verbose_name='Peridural Solicitada por Paciente'
    )
    
    peridural_indicada_medico = models.BooleanField(
        default=False,
        verbose_name='Peridural Indicada por Médico'
    )
    
    peridural_administrada = models.BooleanField(
        default=False,
        verbose_name='Peridural Administrada'
    )
    
    tiempo_espera_peridural = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo de Espera Peridural (minutos)'
    )
    
    # ============================================
    # SECCIÓN 5: PROFESIONALES Y OBSERVACIONES
    # ============================================
    
    profesional_responsable = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Profesional Responsable'
    )
    
    alumno = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Alumno'
    )
    
    causa_cesarea = models.TextField(
        blank=True,
        verbose_name='Causa de Cesárea',
        help_text='Si aplica, indicar la causa'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    uso_sala_saip = models.BooleanField(
        default=False,
        verbose_name='Uso de Sala SAIP'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
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
        ordering = ['-fecha_hora_parto']
        verbose_name = 'Registro de Parto'
        verbose_name_plural = 'Registros de Parto'
        indexes = [
            models.Index(fields=['numero_registro']),
            models.Index(fields=['ficha', '-fecha_hora_parto']),
            models.Index(fields=['-fecha_hora_parto']),
        ]
    
    def __str__(self):
        return f"{self.numero_registro} - {self.ficha.paciente.persona.Nombre}"
    
    def save(self, *args, **kwargs):
        """Generar número automático si no existe"""
        if not self.numero_registro:
            ultimo = RegistroParto.objects.order_by('-id').first()
            if ultimo:
                try:
                    numero = int(ultimo.numero_registro.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_registro = f"PARTO-{numero:06d}"
        super().save(*args, **kwargs)
    
    @property
    def edad_gestacional_completa(self):
        """Retorna edad gestacional en formato '38+4'"""
        return f"{self.edad_gestacional_semanas}+{self.edad_gestacional_dias}"
    
    def tiene_complicaciones(self):
        """Verifica si hubo complicaciones en el puerperio"""
        return any([
            self.inercia_uterina,
            self.restos_placentarios,
            self.trauma,
            self.alteracion_coagulacion,
            self.hemorragia_postparto,
            self.retencion_placentaria,
        ])


