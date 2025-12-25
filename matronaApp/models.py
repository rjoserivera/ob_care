"""
matronaApp/models.py
Modelos para matrona - Fichas obstétricas, ingresos y medicamentos
COMPLETO: Con TODOS los campos existentes + nuevos (tipo_ingreso, catálogo medicamentos)
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
# CATÁLOGO DE MEDICAMENTOS (NUEVO)
# ============================================

class CatalogoMedicamento(models.Model):
    """Catálogo de medicamentos disponibles para búsqueda"""
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    nombre_generico = models.CharField(max_length=200, blank=True)
    presentacion = models.CharField(max_length=100, blank=True)
    concentracion = models.CharField(max_length=100, blank=True)
    unidad = models.CharField(max_length=50, blank=True)  # mg, ml, etc.
    activo = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'matronaApp'
        ordering = ['nombre']
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
    
    
    def __str__(self):
        if self.concentracion:
            return f"{self.nombre} ({self.concentracion})"
        return self.nombre


# ============================================
# CATÁLOGOS NUEVOS (REQ. USUARIO)
# ============================================

class CatalogoTipoPaciente(models.Model):
    """Catálogo de tipos de paciente"""
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'matronaApp'
        verbose_name = "Tipo de Paciente"
        verbose_name_plural = "Tipos de Paciente"
    
    def __str__(self):
        return self.nombre


class CatalogoDiscapacidad(models.Model):
    """Catálogo de discapacidades"""
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'matronaApp'
        verbose_name = "Tipo de Discapacidad"
        verbose_name_plural = "Tipos de Discapacidad"
    
    def __str__(self):
        return self.nombre


class CatalogoARO(models.Model):
    """Catálogo de Alto Riesgo Obstétrico (ARO)"""
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'matronaApp'
        verbose_name = "Clasificación ARO"
        verbose_name_plural = "Clasificaciones ARO"
    
    def __str__(self):
        return self.nombre




# ============================================
# MODELO: FICHA OBSTÉTRICA (COMPLETO)
# ============================================

class FichaObstetrica(models.Model):
    """
    Ficha obstétrica - Información de la gestante desde el ingreso
    COMPLETO: Con TODOS los campos existentes + tipo_ingreso
    """
    
    # ============================================
    # CHOICES
    # ============================================
    
    PARENTESCO_CHOICES = [
        ('ESPOSO', 'Esposo/Pareja'),
        ('MADRE', 'Madre'),
        ('PADRE', 'Padre'),
        ('HERMANA', 'Hermana'),
        ('HERMANO', 'Hermano'),
        ('AMIGA', 'Amiga'),
        ('OTRO', 'Otro'),
    ]
    TIPO_INGRESO_CHOICES = [
        ('PROGRAMADO', 'Ingreso Programado (Electivo)'),
        ('SALA', 'Ingreso a Sala (Hospitalización)'),
        ('URGENCIA', 'Ingreso por Urgencia (UEGO)'),
        ('DERIVACION', 'Ingreso por Derivación'),
    ]
    
    ESTADO_DILATACION_CHOICES = [
        ('SIN_REGISTRO', 'Sin registro'),
        ('PROGRESANDO', 'Progresando'),
        ('ESTANCADA', 'Estancada'),
        ('LISTA', 'Lista para parto'),
    ]
    
    VIH_RESULTADO_CHOICES = [
        ('NEGATIVO', 'Negativo'),
        ('POSITIVO', 'Positivo'),
        ('INDETERMINADO', 'Indeterminado'),
    ]




    
    # ============================================
    # SECCIÓN 1: RELACIÓN CON PACIENTE
    # ============================================
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='fichas_obstetricas',
        verbose_name='Paciente'
    )
    
    numero_ficha = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha'
    )
    
    # Relación opcional con matrona responsable
    matrona_responsable = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_asignadas',
        verbose_name='Matrona Responsable'
    )
    
    # Relación con patologías (ManyToMany)
    patologias = models.ManyToManyField(
        'medicoApp.Patologias',
        blank=True,
        related_name='fichas_obstetricas',
        verbose_name='Patologías CIE-10'
    )
    
    # ============================================
    # SECCIÓN 2: TIPO DE INGRESO (NUEVO)
    # ============================================
    
    tipo_ingreso = models.CharField(
        max_length=20,
        choices=TIPO_INGRESO_CHOICES,
        default='PROGRAMADO',
        verbose_name='Tipo de Ingreso',
        help_text='Urgencia/Derivación activa parto inmediato'
    )

    tipo_paciente = models.ForeignKey(
        CatalogoTipoPaciente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tipo de Paciente"
    )

    clasificacion_aro = models.ForeignKey(
        CatalogoARO,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Clasificación ARO"
    )





    
    tiene_discapacidad = models.BooleanField(
        default=False,
        verbose_name="¿Posee Discapacidad?"
    )

    discapacidad = models.ForeignKey(
        CatalogoDiscapacidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tipo de Discapacidad"
    )
    
    # ============================================
    # SECCIÓN 3: ACOMPAÑANTE
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
    
    parentesco_acompanante = models.CharField(
        max_length=50, # Increased length just in case
        blank=True,
        verbose_name='Parentesco del Acompañante'
    )
    
    telefono_acompanante = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono del Acompañante'
    )
    
    # ============================================
    # SECCIÓN 4: CONTACTO DE EMERGENCIA
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
        max_length=50,
        blank=True,
        verbose_name='Parentesco Contacto Emergencia'
    )
    
    # ============================================
    # SECCIÓN 5: DATOS GENERALES DEL EMBARAZO
    # ============================================
    
    plan_de_parto = models.BooleanField(
        default=False,
        verbose_name='¿Tiene Plan de Parto?'
    )
    
    visita_guiada = models.BooleanField(
        default=False,
        verbose_name='¿Realizó Visita Guiada?'
    )
    
    consultorio_origen = models.ForeignKey(
        CatalogoConsultorioOrigen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Consultorio de Origen'
    )
    
    # ============================================
    # SECCIÓN 6: MEDIDAS ANTROPOMÉTRICAS
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
        verbose_name='IMC'
    )
    
    # ============================================
    # SECCIÓN 7: HISTORIA OBSTÉTRICA
    # ============================================
    
    numero_gestas = models.PositiveIntegerField(
        default=1,
        verbose_name='Número de Gestaciones'
    )
    
    numero_partos = models.PositiveIntegerField(
        default=0,
        verbose_name='Número de Partos'
    )
    
    partos_vaginales = models.PositiveIntegerField(
        default=0,
        verbose_name='Partos Vaginales'
    )
    
    partos_cesareas = models.PositiveIntegerField(
        default=0,
        verbose_name='Cesáreas'
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
    # SECCIÓN 8: EMBARAZO ACTUAL
    # ============================================
    
    fecha_ultima_regla = models.DateField(
        null=True,
        blank=True,
        verbose_name='FUM (Fecha Última Regla)'
    )
    
    fecha_probable_parto = models.DateField(
        null=True,
        blank=True,
        verbose_name='FPP (Fecha Probable de Parto)'
    )
    
    edad_gestacional_semanas = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Edad Gestacional (semanas)'
    )
    
    edad_gestacional_dias = models.PositiveIntegerField(
        default=0,
        verbose_name='Días adicionales'
    )
    
    cantidad_bebes = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Cantidad de Bebés'
    )
    
    control_prenatal = models.BooleanField(
        default=False,
        verbose_name='¿Tiene Control Prenatal?'
    )
    
    numero_controles = models.PositiveIntegerField(
        default=0,
        verbose_name='Número de Controles'
    )
    
    # ============================================
    # SECCIÓN 9: EXÁMENES VIH
    # ============================================
    
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
        choices=VIH_RESULTADO_CHOICES,
        verbose_name='Resultado VIH 1'
    )
    
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
        choices=VIH_RESULTADO_CHOICES,
        verbose_name='Resultado VIH 2'
    )

    # ============================================
    # SECCIÓN 10: PATOLOGÍAS (Booleanos)
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
        verbose_name='Sepsis / Infección Sistémica'
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
    # SECCIÓN 11: ESTADO DE DILATACIÓN
    # ============================================
    
    estado_dilatacion = models.CharField(
        max_length=20,
        choices=ESTADO_DILATACION_CHOICES,
        default='SIN_REGISTRO',
        verbose_name='Estado de Dilatación'
    )
    
    # ============================================
    # SECCIÓN 12: PROCESO DE PARTO
    # ============================================
    
    proceso_parto_iniciado = models.BooleanField(
        default=False,
        verbose_name='Proceso de Parto Iniciado'
    )
    
    tipo_parto = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            ('VAGINAL', 'Parto Vaginal'),
            ('CESAREA', 'Cesárea'),
        ],
        verbose_name='Tipo de Parto'
    )
    
    fecha_inicio_parto = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha/Hora Inicio Proceso Parto'
    )
    
    # Nuevos campos para control de cierre de ficha
    parto_completado = models.BooleanField(
        default=False,
        verbose_name='Parto Completado y Registrado'
    )
    
    ficha_cerrada = models.BooleanField(
        default=False,
        verbose_name='Ficha Cerrada Definitivamente'
    )
    
    fecha_cierre = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha/Hora de Cierre de Ficha'
    )
    
    usuario_cierre = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_cerradas',
        verbose_name='Usuario que Cerró la Ficha'
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
    # PROPIEDADES Y MÉTODOS
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
    
    @property
    def ultima_dilatacion(self):
        """Retorna el último registro de dilatación"""
        return self.registros_dilatacion.order_by('-fecha_hora').first()
    
    @property
    def valor_dilatacion_actual(self):
        """Retorna el valor de la última dilatación"""
        ultimo = self.ultima_dilatacion
        return ultimo.valor_dilatacion if ultimo else 0
    
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
        """
        Verifica si hay estancamiento en la dilatación.
        Estancamiento = 3 registros consecutivos con el mismo valor.
        Retorna True si hay estancamiento.
        """
        registros = list(self.registros_dilatacion.order_by('-fecha_hora')[:3])
        if len(registros) >= 3:
            valores = [r.valor_dilatacion for r in registros]
            if len(set(valores)) == 1:  # Todos iguales
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
    
    def puede_iniciar_parto(self):
        """
        Determina si se puede iniciar el proceso de parto.
        Retorna: tuple (puede_iniciar: bool, razon: str, tipo_sugerido: str)
        
        CONDICIONES PARA ACTIVAR:
        1. Tipo de ingreso es URGENCIA o DERIVACION → Inmediato
        2. Dilatación >= 8 cm → Parto vaginal
        3. Dilatación estancada (3 registros iguales) → Posible cesárea
        """
        # VALIDACIÓN 0: Verificar si la ficha está cerrada
        if self.ficha_cerrada:
            return False, '🔒 La ficha obstétrica está cerrada definitivamente', None
        
        # VALIDACIÓN 1: Verificar si el parto ya fue completado
        if self.parto_completado:
            return False, '✅ El parto ya fue completado y registrado. Debe cerrar la ficha.', None
        
        # VALIDACIÓN 2: Verificar si ya está en proceso
        if self.proceso_parto_iniciado:
            return False, '⏳ El proceso de parto ya está en curso', None
        
        # Condición 1: Tipo de ingreso urgente
        if self.tipo_ingreso == 'URGENCIA':
            return True, '🚨 Ingreso por URGENCIA - Proceso de parto habilitado inmediatamente', 'URGENTE'
        
        if self.tipo_ingreso == 'DERIVACION':
            return True, '🏥 Ingreso por DERIVACIÓN - Proceso de parto habilitado inmediatamente', 'URGENTE'
        
        # Condición 2: Dilatación >= 8 cm
        val = self.valor_dilatacion_actual
        val_display = str(int(val)) if val % 1 == 0 else str(val)

        if self.puede_parto_vaginal():
            return True, f'✅ Dilatación >= 8 cm ({val_display} cm) - Listo para parto vaginal', 'VAGINAL'
        
        # Condición 3: Estancamiento
        if self.estado_dilatacion == 'ESTANCADA':
            return True, '⚠️ Dilatación estancada - Evaluar cesárea', 'CESAREA'
        
        # No cumple ninguna condición
        dilatacion_actual = self.valor_dilatacion_actual
        val_display = str(int(dilatacion_actual)) if dilatacion_actual % 1 == 0 else str(dilatacion_actual)
        return False, f'⏳ Dilatación actual: {val_display} cm. Se requiere 8 cm o condición especial para habilitar.', None
    
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
            models.Index(fields=['tipo_ingreso']),
        ]


# ============================================
# MODELO: REGISTRO DE DILATACIÓN
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
    
    valor_dilatacion = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
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
        return f"Dilatación {self.valor_dilatacion}cm - {self.fecha_hora.strftime('%d/%m %H:%M')}"
    
    class Meta:
        app_label = 'matronaApp'
        verbose_name = 'Registro de Dilatación'
        verbose_name_plural = 'Registros de Dilatación'
        ordering = ['-fecha_hora']
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
# MODELO: MEDICAMENTO FICHA (ACTUALIZADO)
# ============================================

class MedicamentoFicha(models.Model):
    """Medicamentos asignados a una ficha obstétrica"""
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='medicamentos',
        verbose_name='Ficha Obstétrica'
    )
    
    # Puede ser texto libre O FK a catálogo
    medicamento = models.CharField(
        max_length=200,
        verbose_name='Medicamento'
    )
    
    # FK opcional al catálogo de medicamentos (NUEVO)
    medicamento_catalogo = models.ForeignKey(
        CatalogoMedicamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asignaciones',
        verbose_name='Medicamento (Catálogo)'
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
        if not self.activo:
            return False
        if self.fecha_termino:
            return timezone.now() <= self.fecha_termino
        return True
    
    @property
    def nombre_display(self):
        """Retorna el nombre del medicamento (catálogo o texto)"""
        if self.medicamento_catalogo:
            return str(self.medicamento_catalogo)
        return self.medicamento

    def __str__(self):
        return f"{self.nombre_display} - {self.dosis}"

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
    
    se_realizo_lavado = models.BooleanField(
        default=False,
        verbose_name='¿Se realizó lavado de manos?'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    reacciones_adversas = models.TextField(
        blank=True,
        verbose_name='Reacciones Adversas'
    )
    
    administrado_exitosamente = models.BooleanField(
        default=True,
        verbose_name='¿Administrado Exitosamente?'
    )
    
    motivo_no_administracion = models.TextField(
        blank=True,
        verbose_name='Motivo de No Administración'
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
# MODELO: PERSONAL ASIGNADO AL PARTO
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