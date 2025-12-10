"""
partosApp/models.py - VERSION CORREGIDA
Modelos para registro de parto - Datos completos del proceso de parto
CORREGIDO: Esterilización agregada + Nombre de clase sin espacio
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# ============================================
# CATÁLOGOS PARA PARTOS
# ============================================

class CatalogoTipoParto(models.Model):
    """Catálogo para tipos de parto"""
    codigo = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_tipo_parto'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Tipo Parto'
        verbose_name_plural = 'Catálogo Tipos Parto'

    def __str__(self):
        return self.descripcion


class CatalogoClasificacionRobson(models.Model):
    """Catálogo para Clasificación de Robson (12 grupos)"""
    codigo = models.CharField(max_length=20, unique=True)
    numero_grupo = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_clasificacion_robson'
        ordering = ['numero_grupo']
        verbose_name = 'Catálogo Clasificación Robson'
        verbose_name_plural = 'Catálogo Clasificación Robson'

    def __str__(self):
        return f"Grupo {self.numero_grupo} - {self.descripcion}"


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


class CatalogoCausaCesarea(models.Model):
    """Catálogo para causas de cesárea"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_causa_cesarea'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Causa Cesárea'
        verbose_name_plural = 'Catálogo Causas Cesárea'

    def __str__(self):
        return self.descripcion


class CatalogoMotivoPartoNoAcompanado(models.Model):
    """Catálogo para motivos de parto sin acompañamiento - NOMBRE CORREGIDO"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_motivo_parto_no_acompanado'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Motivo Parto No Acompañado'
        verbose_name_plural = 'Catálogo Motivos Parto No Acompañado'

    def __str__(self):
        return self.descripcion


class CatalogoPersonaAcompanante(models.Model):
    """Catálogo para tipo de persona acompañante"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_persona_acompanante'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Persona Acompañante'
        verbose_name_plural = 'Catálogo Personas Acompañante'

    def __str__(self):
        return self.descripcion


class CatalogoMetodoNoFarmacologico(models.Model):
    """Catálogo para métodos de analgesia no farmacológica"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_metodo_no_farmacologico'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Método No Farmacológico'
        verbose_name_plural = 'Catálogo Métodos No Farmacológicos'

    def __str__(self):
        return self.descripcion


# ============================================
# MODELO: REGISTRO DE PARTO (COMPLETO Y CORREGIDO)
# ============================================

class RegistroParto(models.Model):
    """
    Registro completo del proceso de parto
    Incluye anestesia, analgesia, apego, acompañamiento y todas las complicaciones
    CORREGIDO: Esterilización agregada + Nombres de clase corregidos
    """
    
    # ============================================
    # RELACIONES
    # ============================================
    
    ficha_obstetrica = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.PROTECT,
        related_name='registros_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    ficha_ingreso_parto = models.OneToOneField(
        'ingresoPartoApp.FichaParto',
        on_delete=models.PROTECT,
        related_name='registro_parto',
        null=True,
        blank=True,
        verbose_name='Ficha de Ingreso a Parto'
    )
    
    # ============================================
    # SECCIÓN 1: IDENTIFICACIÓN
    # ============================================
    
    numero_registro = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Registro',
        help_text='Se genera automáticamente: PARTO-000001'
    )
    
    # ============================================
    # SECCIÓN 2: FECHAS Y HORAS
    # ============================================
    
    fecha_hora_admision = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Admisión'
    )
    
    fecha_hora_parto = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha y Hora del Parto'
    )
    
    # ============================================
    # SECCIÓN 3: INFORMACIÓN OBSTÉTRICA
    # ============================================
    
    edad_gestacional_semanas = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(42)],
        verbose_name='Semanas de Embarazo'
    )
    
    edad_gestacional_dias = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        verbose_name='Días adicionales'
    )
    
    tipo_parto = models.ForeignKey(
        CatalogoTipoParto,
        on_delete=models.PROTECT,
        verbose_name='Tipo de Parto'
    )
    
    clasificacion_robson = models.ForeignKey(
        CatalogoClasificacionRobson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Clasificación de Robson'
    )
    
    posicion_parto = models.ForeignKey(
        CatalogoPosicionParto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Posición Materna en Parto'
    )
    
    ofrecimiento_posiciones_alternativas = models.BooleanField(
        default=False,
        verbose_name='¿Se ofrecieron Posiciones Alternativas?'
    )
    
    # ============================================
    # SECCIÓN 4: ALUMBRAMIENTO
    # ============================================
    
    alumbramiento_dirigido = models.BooleanField(
        default=False,
        verbose_name='¿Se realizó Alumbramiento Dirigido?'
    )
    
    retira_placenta = models.BooleanField(
        default=False,
        verbose_name='¿Retira Placenta?'
    )
    
    estampado_placenta = models.BooleanField(
        default=False,
        verbose_name='¿Estampado de Placenta?'
    )
    
    # ============================================
    # SECCIÓN 5: PERINÉ Y COMPLICACIONES
    # ============================================
    
    estado_perine = models.ForeignKey(
        CatalogoEstadoPerine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Estado del Periné'
    )
    
    # Complicaciones puerperales
    inercia_uterina = models.BooleanField(
        default=False,
        verbose_name='Inercia Uterina'
    )
    
    manejo_quirurgico_inercia = models.BooleanField(
        default=False,
        verbose_name='Manejo Quirúrgico de Inercia Uterina'
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
    
    revision_utero = models.BooleanField(
        default=False,
        verbose_name='Revisión de Útero'
    )
    
    hemorragia_postparto = models.BooleanField(
        default=False,
        verbose_name='Hemorragia Postparto'
    )
    
    histerectomia_obstetrica = models.BooleanField(
        default=False,
        verbose_name='Histerectomía Obstétrica'
    )
    
    transfusion_sanguinea = models.BooleanField(
        default=False,
        verbose_name='Transfusión Sanguínea'
    )
    
    # ============================================
    # SECCIÓN 6: ESTERILIZACIÓN (AGREGADA)
    # ============================================
    
    esterilizacion = models.BooleanField(
        default=False,
        verbose_name='¿Se realizó Esterilización?',
        help_text='Ligadura tubaria, vasectomía, etc.'
    )
    
    tipo_esterilizacion = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Tipo de Esterilización',
        help_text='Ligadura tubaria, vasectomía, histerectomía, etc.'
    )
    
    fecha_hora_esterilizacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha y Hora de Esterilización'
    )
    
    # ============================================
    # SECCIÓN 7: ANESTESIA Y ANALGESIA
    # ============================================
    
    # Anestesia Neuroaxial
    anestesia_neuroaxial = models.BooleanField(
        default=False,
        verbose_name='Anestesia Neuroaxial'
    )
    
    # Óxido Nitroso
    oxido_nitroso = models.BooleanField(
        default=False,
        verbose_name='Óxido Nitroso'
    )
    
    # Analgesia Endovenosa
    analgesia_endovenosa = models.BooleanField(
        default=False,
        verbose_name='Analgesia Endovenosa'
    )
    
    # Anestesia General
    anestesia_general = models.BooleanField(
        default=False,
        verbose_name='Anestesia General'
    )
    
    # Anestesia Local
    anestesia_local = models.BooleanField(
        default=False,
        verbose_name='Anestesia Local'
    )
    
    # Analgesia NO Farmacológica
    analgesia_no_farmacologica = models.BooleanField(
        default=False,
        verbose_name='Analgesia NO Farmacológica'
    )
    
    metodos_no_farmacologicos = models.ManyToManyField(
        CatalogoMetodoNoFarmacologico,
        blank=True,
        related_name='registros_parto',
        verbose_name='Métodos NO Farmacológicos Usados',
        help_text='Balón Kinésico, Lenteja, Rebozo, Aromaterapia, etc.'
    )
    
    # Peridural
    peridural_solicitada_paciente = models.BooleanField(
        default=False,
        verbose_name='Peridural Solicitada por Paciente'
    )
    
    peridural_indicada_medico = models.BooleanField(
        default=False,
        verbose_name='Peridural Indicada por Médico GO'
    )
    
    peridural_administrada = models.BooleanField(
        default=False,
        verbose_name='Peridural Administrada'
    )
    
    tiempo_espera_peridural_minutos = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name='Tiempo de Espera Peridural (minutos)',
        help_text='Tiempo entre indicación y administración'
    )
    
    # ============================================
    # SECCIÓN 8: APEGO Y ACOMPAÑAMIENTO
    # ============================================
    
    tiempo_apego_minutos = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name='Tiempo de Apego (minutos)'
    )
    
    apego_canguro = models.BooleanField(
        default=False,
        verbose_name='Apego Canguro'
    )
    
    acompanamiento_preparto = models.BooleanField(
        default=False,
        verbose_name='¿Tuvo Acompañamiento Preparto?'
    )
    
    acompanamiento_parto = models.BooleanField(
        default=False,
        verbose_name='¿Tuvo Acompañamiento en Parto?'
    )
    
    acompanamiento_rn = models.BooleanField(
        default=False,
        verbose_name='¿Tuvo Acompañamiento con RN?'
    )
    
    motivo_parto_no_acompanado = models.ForeignKey(
        CatalogoMotivoPartoNoAcompanado,  # ✅ NOMBRE CORREGIDO
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registros_parto_no_acompanado',
        verbose_name='Motivo Parto NO Acompañado'
    )
    
    persona_acompanante = models.ForeignKey(
        CatalogoPersonaAcompanante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registros_parto_acompanante',
        verbose_name='Persona Acompañante'
    )
    
    acompanante_secciona_cordon = models.BooleanField(
        default=False,
        verbose_name='¿Acompañante Secciona Cordón?'
    )
    
    ligadura_tardia_cordon = models.BooleanField(
        default=False,
        verbose_name='Ligadura Tardía del Cordón (>1 minuto)'
    )
    
    # ============================================
    # SECCIÓN 9: PROFESIONALES
    # ============================================
    
    profesional_responsable_nombre = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Profesional Responsable (Nombre)'
    )
    
    profesional_responsable_apellido = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Profesional Responsable (Apellido)'
    )
    
    alumno_nombre = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Alumno/a (Nombre)',
        help_text='Si aplica'
    )
    
    alumno_apellido = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Alumno/a (Apellido)',
        help_text='Si aplica'
    )
    
    causa_cesarea = models.ForeignKey(
        CatalogoCausaCesarea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registros_parto_causa',
        verbose_name='Causa de Cesárea',
        help_text='Solo si tipo de parto es cesárea'
    )
    
    uso_sala_saip = models.BooleanField(
        default=False,
        verbose_name='¿Uso de Sala SAIP?'
    )
    
    # ============================================
    # SECCIÓN 10: LEY DOMINGA (N° 21.372)
    # ============================================
    
    ley_dominga_recuerdos = models.TextField(
        blank=True,
        verbose_name='Ley Dominga - Cuáles Recuerdos',
        help_text='Especificar cuáles recuerdos se entregan'
    )
    
    ley_dominga_justificacion = models.TextField(
        blank=True,
        verbose_name='Ley Dominga - Justificación',
        help_text='Si no se entregan, justificar motivo'
    )
    
    # ============================================
    # SECCIÓN 11: INFORMACIÓN GENERAL
    # ============================================
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    # ============================================
    # SECCIÓN 12: METADATA
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
            models.Index(fields=['ficha_obstetrica', '-fecha_hora_parto']),
            models.Index(fields=['-fecha_hora_parto']),
        ]

    def __str__(self):
        return f"{self.numero_registro} - {self.ficha_obstetrica.paciente.persona.Nombre}"
    
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
    
    def tiene_complicaciones(self):
        """Verifica si hubo complicaciones en el puerperio"""
        return any([
            self.inercia_uterina,
            self.restos_placentarios,
            self.trauma,
            self.alteracion_coagulacion,
            self.hemorragia_postparto,
            self.esterilizacion,
        ])
    
    @property
    def edad_gestacional_completa(self):
        """Retorna edad gestacional en formato '38+4'"""
        return f"{self.edad_gestacional_semanas}+{self.edad_gestacional_dias}"