# ============================================
# ingresoPartoApp/models.py
# VERSIÓN SIN CHOICES - FK A TABLAS CATÁLOGO
# ============================================

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# ============================================
# TABLAS CATÁLOGO PARA ingresoPartoApp
# ============================================

class CatalogoTipoPaciente(models.Model):
    """Catálogo para tipos de paciente al ingreso"""
    codigo = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_tipo_paciente'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Tipo Paciente'
        verbose_name_plural = 'Catálogo Tipos de Paciente'

    def __str__(self):
        return self.descripcion


class CatalogoOrigenIngreso(models.Model):
    """Catálogo para origen del ingreso"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_origen_ingreso'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Origen Ingreso'
        verbose_name_plural = 'Catálogo Orígenes de Ingreso'

    def __str__(self):
        return self.descripcion


class CatalogoOrdenVIH(models.Model):
    """Catálogo para orden de toma de VIH (1°, 2°, 3°)"""
    codigo = models.CharField(max_length=5, unique=True)
    descripcion = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_orden_vih'
        ordering = ['orden']
        verbose_name = 'Catálogo Orden VIH'
        verbose_name_plural = 'Catálogo Orden VIH'

    def __str__(self):
        return self.descripcion


class CatalogoResultadoSGB(models.Model):
    """Catálogo para resultados de SGB"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_resultado_sgb'
        ordering = ['orden']
        verbose_name = 'Catálogo Resultado SGB'
        verbose_name_plural = 'Catálogo Resultados SGB'

    def __str__(self):
        return self.descripcion


class CatalogoResultadoVDRL(models.Model):
    """Catálogo para resultados de VDRL"""
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'catalogo_resultado_vdrl'
        ordering = ['orden']
        verbose_name = 'Catálogo Resultado VDRL'
        verbose_name_plural = 'Catálogo Resultados VDRL'

    def __str__(self):
        return self.descripcion


# ============================================
# MODELO PRINCIPAL: FICHA PARTO
# ============================================

class FichaParto(models.Model):
    """
    Ficha de ingreso para el proceso de parto
    SIN CHOICES - Usa FK a tablas catálogo
    """
    
    # ============================================
    # RELACIÓN CON FICHA OBSTÉTRICA
    # ============================================
    
    ficha_obstetrica = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.PROTECT,
        related_name='fichas_ingreso_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    numero_ficha_parto = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha de Parto',
        help_text='Se genera automáticamente: FP-000001'
    )
    
    # ============================================
    # SECCIÓN 1: DATOS GENERALES DEL INGRESO
    # ============================================
    
    # FK a catálogo (antes era CHOICES)
    tipo_paciente_catalogo = models.ForeignKey(
        CatalogoTipoPaciente,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='fichas_parto',
        verbose_name='Tipo de Paciente',
        help_text='Clasificación según origen'
    )
    
    @property
    def tipo_paciente(self):
        """Alias para compatibilidad"""
        return self.tipo_paciente_catalogo.codigo if self.tipo_paciente_catalogo else None
    
    # FK a catálogo (antes era CHOICES)
    origen_ingreso_catalogo = models.ForeignKey(
        CatalogoOrigenIngreso,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='fichas_parto',
        verbose_name='Origen de Ingreso',
        help_text='De dónde viene la paciente'
    )
    
    @property
    def origen_ingreso(self):
        """Alias para compatibilidad"""
        return self.origen_ingreso_catalogo.codigo if self.origen_ingreso_catalogo else None
    
    fecha_ingreso = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Ingreso'
    )
    
    hora_ingreso = models.TimeField(
        default=timezone.now,
        verbose_name='Hora de Ingreso'
    )
    
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
    
    control_prenatal = models.BooleanField(
        default=True,
        verbose_name='¿Tuvo Control Prenatal?',
        help_text='¿Asistió a controles durante el embarazo?'
    )
    
    consultorio_origen = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Consultorio de Origen',
        help_text='Nombre del consultorio o CESFAM'
    )
    
    # ============================================
    # SECCIÓN 2: PATOLOGÍAS AL INGRESO
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
        verbose_name='Sepsis o Infección Sistémica Grave'
    )
    
    infeccion_ovular = models.BooleanField(
        default=False,
        verbose_name='Infección Ovular o Corioamnionitis'
    )
    
    otra_patologia = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Otra Patología',
        help_text='Especificar otra patología si aplica'
    )
    
    # ============================================
    # SECCIÓN 3: TAMIZAJE VIH
    # ============================================
    
    numero_aro = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Número ARO',
        help_text='Número de Alto Riesgo Obstétrico'
    )
    
    vih_tomado_prepartos = models.BooleanField(
        default=False,
        verbose_name='Se tomó VIH en Prepartos',
        help_text='¿Se realizó test de VIH al ingresar a prepartos?'
    )
    
    vih_tomado_sala = models.BooleanField(
        default=False,
        verbose_name='Se tomó VIH en Sala',
        help_text='¿Se realizó test de VIH en sala de parto?'
    )
    
    # FK a catálogo (antes era CHOICES)
    vih_orden_catalogo = models.ForeignKey(
        CatalogoOrdenVIH,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='fichas_parto',
        verbose_name='Orden de Toma (1°-2°-3°)',
        help_text='Número de vez que se toma el VIH'
    )
    
    @property
    def vih_orden_toma(self):
        """Alias para compatibilidad"""
        return self.vih_orden_catalogo.codigo if self.vih_orden_catalogo else None
    
    # ============================================
    # SECCIÓN 4: TAMIZAJE SGB
    # ============================================
    
    sgb_pesquisa = models.BooleanField(
        default=False,
        verbose_name='Pesquisa SGB Realizada',
        help_text='¿Se realizó cultivo para SGB?'
    )
    
    # FK a catálogo (antes era CHOICES)
    sgb_resultado_catalogo = models.ForeignKey(
        CatalogoResultadoSGB,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='fichas_parto',
        verbose_name='Resultado SGB'
    )
    
    @property
    def sgb_resultado(self):
        """Alias para compatibilidad"""
        return self.sgb_resultado_catalogo.codigo if self.sgb_resultado_catalogo else None
    
    antibiotico_sgb = models.BooleanField(
        default=False,
        verbose_name='Antibiótico por SGB (NO POR RPM)',
        help_text='¿Se administró antibiótico profiláctico por SGB positivo?'
    )
    
    # ============================================
    # SECCIÓN 5: TAMIZAJE VDRL
    # ============================================
    
    # FK a catálogo (antes era CHOICES)
    vdrl_resultado_catalogo = models.ForeignKey(
        CatalogoResultadoVDRL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='fichas_parto',
        verbose_name='Resultado VDRL durante embarazo',
        help_text='Resultado del test VDRL para sífilis'
    )
    
    @property
    def vdrl_resultado(self):
        """Alias para compatibilidad"""
        return self.vdrl_resultado_catalogo.codigo if self.vdrl_resultado_catalogo else None
    
    tratamiento_sifilis = models.BooleanField(
        default=False,
        verbose_name='Tratamiento ATB por Sífilis al momento del Parto',
        help_text='¿Se administró tratamiento antibiótico para sífilis?'
    )
    
    # ============================================
    # SECCIÓN 6: TAMIZAJE HEPATITIS B
    # ============================================
    
    hepatitis_b_tomado = models.BooleanField(
        default=False,
        verbose_name='Examen Hepatitis B - Tomado',
        help_text='¿Se realizó serología para Hepatitis B?'
    )
    
    derivacion_gastro = models.BooleanField(
        default=False,
        verbose_name='Derivación a Gastro-Hepatólogo',
        help_text='¿Requiere derivación a especialista?'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación del Registro'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Última Modificación'
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Ficha Activa'
    )
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Ficha de Parto (Ingreso)'
        verbose_name_plural = 'Fichas de Parto (Ingresos)'
        indexes = [
            models.Index(fields=['numero_ficha_parto']),
            models.Index(fields=['ficha_obstetrica', '-fecha_ingreso']),
        ]
    
    def __str__(self):
        return f"{self.numero_ficha_parto} - {self.ficha_obstetrica.paciente.persona.Nombre}"
    
    def save(self, *args, **kwargs):
        """Generar número automático si no existe"""
        if not self.numero_ficha_parto:
            ultima = FichaParto.objects.order_by('-id').first()
            if ultima:
                try:
                    numero = int(ultima.numero_ficha_parto.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_ficha_parto = f"FP-{numero:06d}"
        super().save(*args, **kwargs)
    
    def tiene_tamizajes_completos(self):
        """Verifica si todos los tamizajes están completos"""
        return all([
            self.sgb_pesquisa,
            self.vdrl_resultado_catalogo is not None,
            self.hepatitis_b_tomado,
            self.vih_tomado_prepartos or self.vih_tomado_sala,
        ])
    
    def tiene_patologias_graves(self):
        """Verifica si tiene patologías que requieren atención especial"""
        return any([
            self.preeclampsia_severa,
            self.eclampsia,
            self.sepsis_infeccion_grave,
            self.infeccion_ovular,
        ])
    
    def resumen_tamizajes(self):
        """Retorna un resumen de los tamizajes realizados"""
        resumen = []
        
        if self.sgb_pesquisa:
            resultado = self.sgb_resultado_catalogo.descripcion if self.sgb_resultado_catalogo else 'Pendiente'
            resumen.append(f"SGB: {resultado}")
        
        if self.vdrl_resultado_catalogo:
            resumen.append(f"VDRL: {self.vdrl_resultado_catalogo.descripcion}")
        
        if self.hepatitis_b_tomado:
            resumen.append("Hepatitis B: Realizado")
        
        if self.vih_tomado_prepartos or self.vih_tomado_sala:
            orden = self.vih_orden_catalogo.codigo if self.vih_orden_catalogo else '1'
            resumen.append(f"VIH: Toma {orden}°")
        
        return " | ".join(resumen) if resumen else "Sin tamizajes registrados"


