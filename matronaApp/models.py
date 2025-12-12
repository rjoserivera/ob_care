"""
matronaApp/models.py
Modelos para matrona - Fichas obstétricas, ingresos y medicamentos
ACTUALIZADO CON TODOS LOS CAMPOS NUEVOS (dilatación, VIH, acompañante, etc.)
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from gestionApp.models import Paciente


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
    ACTUALIZADO: Con campos de dilatación, VIH, acompañante, tipo parto, etc.
    """
    
    # ============================================
    # CHOICES
    # ============================================
    
    PARENTESCO_CHOICES = [
        ('PAREJA', 'Pareja'),
        ('ESPOSO', 'Esposo/a'),
        ('MADRE', 'Madre'),
        ('PADRE', 'Padre'),
        ('HERMANO', 'Hermano/a'),
        ('SUEGRA', 'Suegra/o'),
        ('HIJO', 'Hijo/a'),
        ('AMIGO', 'Amigo/a'),
        ('OTRO', 'Otro'),
    ]
    
    RESULTADO_VIH_CHOICES = [
        ('', 'Sin realizar'),
        ('NEGATIVO', 'Negativo'),
        ('POSITIVO', 'Positivo'),
        ('INDETERMINADO', 'Indeterminado'),
    ]
    
    TIPO_PARTO_CHOICES = [
        ('', 'No definido'),
        ('VAGINAL', 'Parto Vaginal'),
        ('CESAREA', 'Cesárea'),
    ]
    
    ESTADO_DILATACION_CHOICES = [
        ('ESPERANDO', 'Esperando registro'),
        ('PROGRESANDO', 'Progresando'),
        ('ESTANCADA', 'Estancamiento'),
        ('LISTA', 'Lista para parto'),
    ]
    
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
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_obstetrica_responsable',
        verbose_name='Matrona Responsable',
        limit_choices_to={'groups__name': 'Matronas'}
    )
    
    patologias = models.ManyToManyField(
        'medicoApp.Patologias',
        blank=True,
        related_name='fichas_obstetricas',
        verbose_name='Patologías'
    )
    
    consultorio_origen = models.ForeignKey(
        CatalogoConsultorioOrigen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Consultorio de Origen'
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
    # SECCIÓN 2: ACOMPAÑANTE (ACTUALIZADO)
    # ============================================
    
    tiene_acompanante = models.BooleanField(
        default=False,
        verbose_name='¿Viene con acompañante?'
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
    
    parentesco_acompanante = models.CharField(
        max_length=20,
        choices=PARENTESCO_CHOICES,
        blank=True,
        verbose_name='Parentesco del Acompañante'
    )
    
    telefono_acompanante = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono del Acompañante'
    )
    
    # ============================================
    # SECCIÓN 3: CONTACTO DE EMERGENCIA (NUEVO)
    # ============================================
    
    nombre_contacto_emergencia = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nombre Contacto de Emergencia'
    )
    
    telefono_emergencia = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono de Emergencia'
    )
    
    parentesco_contacto_emergencia = models.CharField(
        max_length=20,
        choices=PARENTESCO_CHOICES,
        blank=True,
        verbose_name='Parentesco Contacto Emergencia'
    )
    
    # ============================================
    # SECCIÓN 4: DATOS GENERALES DEL EMBARAZO
    # ============================================
    
    plan_de_parto = models.BooleanField(
        default=False,
        verbose_name='¿Tiene Plan de Parto?'
    )
    
    visita_guiada = models.BooleanField(
        default=False,
        verbose_name='¿Realizó Visita Guiada?'
    )
    
    # ============================================
    # SECCIÓN 5: MEDIDAS ANTROPOMÉTRICAS
    # ============================================
    
    peso_actual = models.DecimalField(
        max_digits=5,
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
    
    imc = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='IMC',
        help_text='Índice de Masa Corporal (calculado automáticamente)'
    )
    
    # ============================================
    # SECCIÓN 6: ANTECEDENTES OBSTÉTRICOS
    # ============================================
    
    numero_gestas = models.IntegerField(
        default=1,
        verbose_name='Número de Gestaciones',
        help_text='Incluye embarazos anteriores + actual'
    )
    
    numero_partos = models.IntegerField(
        default=0,
        verbose_name='Número de Partos',
        help_text='Partos anteriores (vaginales + cesáreas)'
    )
    
    partos_vaginales = models.IntegerField(
        default=0,
        verbose_name='Partos Vaginales'
    )
    
    partos_cesareas = models.IntegerField(
        default=0,
        verbose_name='Partos por Cesárea'
    )
    
    numero_abortos = models.IntegerField(
        default=0,
        verbose_name='Número de Abortos'
    )
    
    nacidos_vivos = models.IntegerField(
        default=0,
        verbose_name='Nacidos Vivos'
    )
    
    # ============================================
    # SECCIÓN 7: EMBARAZO ACTUAL
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
    
    edad_gestacional_semanas = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(45)],
        verbose_name='Semanas de Gestación'
    )
    
    edad_gestacional_dias = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(6)],
        verbose_name='Días Adicionales'
    )
    
    cantidad_bebes = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Cantidad de Bebés Esperados'
    )
    
    # ============================================
    # SECCIÓN 8: EXÁMENES VIH (ACTUALIZADO)
    # ============================================
    
    # VIH Test 1
    vih_tomado = models.BooleanField(
        default=False,
        verbose_name='¿VIH 1 Tomado?'
    )
    
    vih_resultado = models.CharField(
        max_length=20,
        choices=RESULTADO_VIH_CHOICES,
        blank=True,
        verbose_name='Resultado VIH 1'
    )
    
    # Campos VIH con nombres que coinciden con el formulario existente
    vih_1_realizado = models.BooleanField(
        default=False,
        verbose_name='¿VIH 1 Realizado?'
    )
    
    vih_1_fecha = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha Examen VIH 1'
    )
    
    vih_1_resultado = models.CharField(
        max_length=20,
        choices=RESULTADO_VIH_CHOICES,
        blank=True,
        verbose_name='Resultado VIH 1'
    )
    
    # VIH Test 2
    vih_2_realizado = models.BooleanField(
        default=False,
        verbose_name='¿VIH 2 Realizado?'
    )
    
    vih_2_fecha = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha Examen VIH 2'
    )
    
    vih_2_resultado = models.CharField(
        max_length=20,
        choices=RESULTADO_VIH_CHOICES,
        blank=True,
        verbose_name='Resultado VIH 2'
    )
    
    # ============================================
    # SECCIÓN 9: OTROS EXÁMENES
    # ============================================
    
    sgb_pesquisa = models.BooleanField(
        default=False,
        verbose_name='¿SGB Pesquisado?'
    )
    
    sgb_resultado = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Resultado SGB'
    )
    
    vdrl_resultado = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Resultado VDRL'
    )
    
    hepatitis_b_tomado = models.BooleanField(
        default=False,
        verbose_name='¿Hepatitis B Tomada?'
    )
    
    hepatitis_b_resultado = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Resultado Hepatitis B'
    )
    
    # ============================================
    # SECCIÓN 10: PATOLOGÍAS (Campos específicos)
    # ============================================
    
    preeclampsia_severa = models.BooleanField(
        default=False,
        verbose_name='¿Preeclampsia Severa?'
    )
    
    eclampsia = models.BooleanField(
        default=False,
        verbose_name='¿Eclampsia?'
    )
    
    sepsis_infeccion_sistemia = models.BooleanField(
        default=False,
        verbose_name='¿Sepsis o Infección Sistémica?'
    )
    
    infeccion_ovular = models.BooleanField(
        default=False,
        verbose_name='¿Infección Ovular?'
    )
    
    otras_patologias = models.TextField(
        blank=True,
        verbose_name='Otras Patologías'
    )
    
    # ============================================
    # SECCIÓN 11: CONTROL PRENATAL
    # ============================================
    
    control_prenatal = models.BooleanField(
        default=True,
        verbose_name='¿Tuvo Control Prenatal?'
    )
    
    numero_controles = models.IntegerField(
        default=0,
        verbose_name='Número de Controles'
    )
    
    # ============================================
    # SECCIÓN 12: DILATACIÓN Y PARTO (NUEVO)
    # ============================================
    
    dilatacion_inicial = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Dilatación Inicial (cm)'
    )
    
    estado_dilatacion = models.CharField(
        max_length=20,
        choices=ESTADO_DILATACION_CHOICES,
        default='ESPERANDO',
        verbose_name='Estado de Dilatación'
    )
    
    tipo_parto = models.CharField(
        max_length=20,
        choices=TIPO_PARTO_CHOICES,
        blank=True,
        verbose_name='Tipo de Parto'
    )
    
    proceso_parto_iniciado = models.BooleanField(
        default=False,
        verbose_name='¿Proceso de Parto Iniciado?'
    )
    
    fecha_inicio_parto = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha/Hora Inicio Proceso Parto'
    )
    
    # ============================================
    # SECCIÓN 13: CONTROL Y ESTADO
    # ============================================
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Ficha Activa'
    )
    
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de Creación'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Modificación'
    )
    
    # ============================================
    # PROPIEDADES CALCULADAS
    # ============================================
    
    @property
    def personal_requerido(self):
        """Calcula el personal requerido según cantidad de bebés"""
        return {
            'medicos': self.cantidad_bebes,
            'matronas': self.cantidad_bebes * 2,
            'tens': self.cantidad_bebes * 2,
            'total': self.cantidad_bebes * 5
        }
    
    def calcular_imc(self):
        """Calcula el IMC basado en peso y talla"""
        if self.peso_actual and self.talla_actual:
            talla_metros = float(self.talla_actual) / 100
            self.imc = round(float(self.peso_actual) / (talla_metros ** 2), 2)
    
    def calcular_edad_gestacional(self):
        """Calcula semanas y días de gestación basado en FUM"""
        if self.fecha_ultima_regla:
            hoy = timezone.now().date()
            dias_transcurridos = (hoy - self.fecha_ultima_regla).days
            self.edad_gestacional_semanas = min(dias_transcurridos // 7, 42)
            self.edad_gestacional_dias = dias_transcurridos % 7
            # FPP = FUM + 280 días
            from datetime import timedelta
            self.fecha_probable_parto = self.fecha_ultima_regla + timedelta(days=280)
    
    def verificar_estancamiento(self):
        """Verifica si hay estancamiento en la dilatación (3 valores iguales)"""
        registros = self.registros_dilatacion.order_by('-fecha_hora')[:3]
        if registros.count() >= 3:
            valores = [r.valor_dilatacion for r in registros]
            if len(set(valores)) == 1:
                self.estado_dilatacion = 'ESTANCADA'
                self.save(update_fields=['estado_dilatacion'])
                return True
        return False
    
    def puede_parto_vaginal(self):
        """Verifica si cumple condiciones para parto vaginal (≥8 cm)"""
        ultimo_registro = self.registros_dilatacion.order_by('-fecha_hora').first()
        if ultimo_registro and ultimo_registro.valor_dilatacion >= 8:
            return True
        return False
    
    def save(self, *args, **kwargs):
        # Calcular IMC automáticamente
        if self.peso_actual and self.talla_actual:
            self.calcular_imc()
        # Calcular edad gestacional automáticamente
        if self.fecha_ultima_regla:
            self.calcular_edad_gestacional()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ficha {self.numero_ficha} - {self.paciente}"

    class Meta:
        app_label = 'matronaApp'
        verbose_name = 'Ficha Obstétrica'
        verbose_name_plural = 'Fichas Obstétricas'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['numero_ficha']),
            models.Index(fields=['paciente', '-fecha_creacion']),
        ]


# ============================================
# MODELO: REGISTRO DE DILATACIÓN (NUEVO)
# ============================================

class RegistroDilatacion(models.Model):
    """Modelo para registrar la dilatación cervical cada hora"""
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='registros_dilatacion',
        verbose_name='Ficha Obstétrica'
    )
    
    fecha_hora = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora del Registro'
    )
    
    valor_dilatacion = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Dilatación (cm)'
    )
    
    observacion = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Observación'
    )
    
    registrado_por = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registros_dilatacion',
        verbose_name='Registrado Por'
    )
    
    def __str__(self):
        return f"Dilatación {self.valor_dilatacion}cm - {self.fecha_hora.strftime('%H:%M')}"
    
    class Meta:
        app_label = 'matronaApp'
        verbose_name = 'Registro de Dilatación'
        verbose_name_plural = 'Registros de Dilatación'
        ordering = ['fecha_hora']
        indexes = [
            models.Index(fields=['ficha', '-fecha_hora']),
        ]


# ============================================
# MODELO: INGRESO PACIENTE
# ============================================

class IngresoPaciente(models.Model):
    """Registro de ingreso hospitalario de paciente"""
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='ingresos',
        verbose_name='Paciente'
    )
    
    numero_ficha = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha Ingreso'
    )
    
    motivo_ingreso = models.TextField(
        verbose_name='Motivo de Ingreso'
    )
    
    fecha_ingreso = models.DateField(
        verbose_name='Fecha de Ingreso'
    )
    
    hora_ingreso = models.TimeField(
        verbose_name='Hora de Ingreso'
    )
    
    edad_gestacional_semanas = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Edad Gestacional (semanas)'
    )
    
    derivacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Derivación'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    fecha_creacion = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Ingreso {self.numero_ficha} - {self.paciente}"

    class Meta:
        app_label = 'matronaApp'
        verbose_name = 'Ingreso de Paciente'
        verbose_name_plural = 'Ingresos de Pacientes'
        ordering = ['-fecha_ingreso', '-hora_ingreso']


# ============================================
# MODELO: MEDICAMENTO FICHA
# ============================================

class MedicamentoFicha(models.Model):
    """Medicamentos asignados a una ficha obstétrica"""
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='medicamentos',
        verbose_name='Ficha Obstétrica'
    )
    
    medicamento = models.CharField(
        max_length=200,
        verbose_name='Medicamento'
    )
    
    dosis = models.CharField(
        max_length=100,
        verbose_name='Dosis'
    )
    
    via_administracion = models.ForeignKey(
        CatalogoViaAdministracion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Vía de Administración'
    )
    
    frecuencia = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Frecuencia',
        help_text='Ej: Cada 6 horas, Cada 8 horas'
    )
    
    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name='Cantidad'
    )
    
    fecha_inicio = models.DateTimeField(
        verbose_name='Fecha de Inicio'
    )
    
    fecha_termino = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Término'
    )
    
    indicaciones = models.TextField(
        blank=True,
        verbose_name='Indicaciones'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    fecha_creacion = models.DateTimeField(
        default=timezone.now
    )
    
    @property
    def esta_vigente(self):
        """Verifica si el medicamento está vigente"""
        if self.fecha_termino:
            return timezone.now() <= self.fecha_termino
        return self.activo

    def __str__(self):
        return f"{self.medicamento} - {self.dosis}"

    class Meta:
        app_label = 'matronaApp'
        verbose_name = 'Medicamento de Ficha'
        verbose_name_plural = 'Medicamentos de Ficha'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['ficha', 'activo']),
        ]


# ============================================
# MODELO: ADMINISTRACIÓN DE MEDICAMENTO
# ============================================

class AdministracionMedicamento(models.Model):
    """Registro de administración de medicamentos"""
    
    medicamento_ficha = models.ForeignKey(
        MedicamentoFicha,
        on_delete=models.CASCADE,
        related_name='administraciones',
        verbose_name='Medicamento'
    )
    
    tens = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='administraciones_medicamentos',
        verbose_name='TENS Responsable',
        limit_choices_to={'groups__name': 'TENS'}
    )
    
    fecha_hora_administracion = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Administración'
    )
    
    dosis_administrada = models.CharField(
        max_length=100,
        verbose_name='Dosis Administrada'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    fecha_registro = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"{self.medicamento_ficha.medicamento} - {self.fecha_hora_administracion}"

    class Meta:
        app_label = 'matronaApp'
        verbose_name = 'Administración de Medicamento'
        verbose_name_plural = 'Administraciones de Medicamentos'
        ordering = ['-fecha_hora_administracion']


# ============================================
# MODELO: PERSONAL ASIGNADO AL PARTO (NUEVO)
# ============================================

class PersonalAsignadoParto(models.Model):
    """Modelo para el personal asignado a un proceso de parto"""
    
    ROL_CHOICES = [
        ('MEDICO', 'Médico'),
        ('MATRONA', 'Matrona'),
        ('TENS', 'TENS'),
    ]
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='personal_asignado',
        verbose_name='Ficha Obstétrica'
    )
    
    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asignaciones_parto',
        verbose_name='Usuario'
    )
    
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        verbose_name='Rol'
    )
    
    bebe_numero = models.PositiveIntegerField(
        default=1,
        verbose_name='Número de Bebé Asignado'
    )
    
    fecha_asignacion = models.DateTimeField(
        default=timezone.now
    )
    
    activo = models.BooleanField(
        default=True
    )
    
    def __str__(self):
        nombre = self.usuario.get_full_name() if self.usuario else 'Sin asignar'
        return f"{self.get_rol_display()} - {nombre} (Bebé #{self.bebe_numero})"
    
    class Meta:
        app_label = 'matronaApp'
        verbose_name = 'Personal Asignado al Parto'
        verbose_name_plural = 'Personal Asignado a Partos'
        ordering = ['bebe_numero', 'rol']