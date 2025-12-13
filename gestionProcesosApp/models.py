"""
Modelos para la aplicación gestionProcesosApp
Gestión de procesos, personal, salas y derivaciones
"""

from django.db import models
from django.contrib.auth.models import User
from ingresoPartoApp.models import FichaParto
from recienNacidoApp.models import RegistroRecienNacido


# ==================== SALA ====================

class Sala(models.Model):
    """Sala de parto o área de atención"""
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADA', 'Ocupada'),
        ('MANTENIMIENTO', 'Mantenimiento'),
    ]
    
    nombre = models.CharField(max_length=50, unique=True)
    codigo = models.CharField(max_length=10, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')
    capacidad_maxima = models.IntegerField()
    activa = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)
    
    proceso_activo = models.ForeignKey(FichaParto, on_delete=models.SET_NULL, null=True, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'gestionProcesosApp'
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


# ==================== PERSONAL EN TURNO ====================

class PersonalTurno(models.Model):
    """Personal disponible en un turno"""
    ROL_CHOICES = [
        ('MEDICO', 'Médico'),
        ('MATRONA', 'Matrona'),
        ('TENS', 'TENS'),
        ('ADMIN', 'Administrativo'),
    ]
    
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('EN_TURNO', 'En turno'),
        ('DESCANSO', 'Descanso'),
        ('AUSENTE', 'Ausente'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turnos_personal')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')
    
    fecha_inicio_turno = models.DateTimeField()
    fecha_fin_turno = models.DateTimeField()
    
    # Dispositivo
    token_push = models.TextField(blank=True, help_text='Token para notificaciones push')
    dispositivo_activo = models.BooleanField(default=False)
    
    # Control
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Proceso asignado
    proceso_asignado = models.ForeignKey(FichaParto, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        app_label = 'gestionProcesosApp'
        ordering = ['-fecha_inicio_turno']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_rol_display()}"


# ==================== NOTIFICACIÓN ====================

class Notificacion(models.Model):
    """Notificación enviada a personal"""
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso de paciente'),
        ('PARTO', 'Parto iniciado'),
        ('URGENCIA', 'Urgencia'),
        ('DERIVACION', 'Derivación'),
    ]
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ENVIADA', 'Enviada'),
        ('ENTREGADA', 'Entregada'),
        ('VISTA', 'Vista'),
        ('CONFIRMADA', 'Confirmada'),
        ('EXPIRADA', 'Expirada'),
    ]
    
    proceso = models.ForeignKey(FichaParto, on_delete=models.CASCADE, related_name='notificaciones')
    destinatario = models.ForeignKey(PersonalTurno, on_delete=models.CASCADE, related_name='notificaciones_recibidas')
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    
    timestamp_envio = models.DateTimeField(auto_now_add=True)
    timestamp_entrega = models.DateTimeField(null=True, blank=True)
    timestamp_vista = models.DateTimeField(null=True, blank=True)
    timestamp_confirmacion = models.DateTimeField(null=True, blank=True)
    timestamp_expiracion = models.DateTimeField()
    
    # Respuesta
    token_push_usado = models.TextField(blank=True)
    respuesta_servidor = models.TextField(blank=True)
    codigo_error = models.CharField(max_length=50, blank=True)
    
    class Meta:
        app_label = 'gestionProcesosApp'
        ordering = ['-timestamp_envio']
    
    def __str__(self):
        return f"{self.titulo} - {self.destinatario}"


# ==================== ASIGNACIÓN PERSONAL ====================

class AsignacionPersonal(models.Model):
    """Asignación de personal a un proceso"""
    proceso = models.ForeignKey(FichaParto, on_delete=models.CASCADE, related_name='asignaciones')
    personal = models.ForeignKey(PersonalTurno, on_delete=models.CASCADE)
    
    rol_en_proceso = models.CharField(max_length=30)
    
    # Confirmación
    timestamp_notificacion = models.DateTimeField(auto_now_add=True)
    timestamp_confirmacion = models.DateTimeField(null=True, blank=True)
    confirmo_asistencia = models.BooleanField(default=False)
    
    # Estado de respuesta (nuevo)
    ESTADO_CHOICES = [
        ('ENVIADA', 'Enviada'),
        ('ACEPTADA', 'Aceptada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    estado_respuesta = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='ENVIADA',
        verbose_name="Estado de Respuesta"
    )
    
    # Ingreso a sala
    timestamp_ingreso_sala = models.DateTimeField(null=True, blank=True)
    ingreso_a_sala = models.BooleanField(default=False)
    
    # Salida de sala
    timestamp_salida_sala = models.DateTimeField(null=True, blank=True)
    salio_de_sala = models.BooleanField(default=False)
    
    observaciones = models.TextField(blank=True)
    
    class Meta:
        app_label = 'gestionProcesosApp'
        unique_together = ['proceso', 'personal', 'rol_en_proceso']
    
    def __str__(self):
        return f"{self.personal} - {self.rol_en_proceso}"


# ==================== CONFIRMACIÓN PERSONAL ====================

class ConfirmacionPersonal(models.Model):
    """Registro de confirmación de asistencia"""
    asignacion = models.OneToOneField(AsignacionPersonal, on_delete=models.CASCADE)
    notificacion = models.OneToOneField(Notificacion, on_delete=models.CASCADE)
    
    confirmo = models.BooleanField()
    timestamp_confirmacion = models.DateTimeField(auto_now_add=True)
    tiempo_respuesta_segundos = models.IntegerField()
    dentro_tiempo_limite = models.BooleanField()
    
    # Información del dispositivo
    ip_confirmacion = models.CharField(max_length=39, blank=True, null=True)
    user_agent = models.TextField(blank=True)
    dispositivo = models.CharField(max_length=200, blank=True, null=True)
    
    observaciones = models.TextField(blank=True)
    
    class Meta:
        app_label = 'gestionProcesosApp'
    
    def __str__(self):
        return f"Confirmación {self.asignacion.personal} - {self.timestamp_confirmacion}"


# ==================== DERIVACIÓN ====================

class Derivacion(models.Model):
    """Derivación de paciente o recién nacido"""
    TIPO_CHOICES = [
        ('PACIENTE', 'Paciente'),
        ('RECIEN_NACIDO', 'Recién nacido'),
    ]
    
    ESTADO_CHOICES = [
        ('SOLICITADA', 'Solicitada'),
        ('ACEPTADA', 'Aceptada'),
        ('EN_TRASLADO', 'En traslado'),
        ('COMPLETADA', 'Completada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    
    proceso = models.ForeignKey(FichaParto, on_delete=models.CASCADE, related_name='derivaciones')
    medico_solicitante = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    registro_recien_nacido = models.ForeignKey(RegistroRecienNacido, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    motivo = models.CharField(max_length=50)
    motivo_detallado = models.TextField()
    
    servicio_destino = models.CharField(max_length=100)
    medico_receptor = models.CharField(max_length=200, blank=True, null=True)
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='SOLICITADA')
    
    # Timestamps
    timestamp_solicitud = models.DateTimeField(auto_now_add=True)
    timestamp_aceptacion = models.DateTimeField(null=True, blank=True)
    timestamp_traslado = models.DateTimeField(null=True, blank=True)
    timestamp_completado = models.DateTimeField(null=True, blank=True)
    
    # Información clínica
    signos_vitales = models.TextField(blank=True)
    tratamiento_previo = models.TextField(blank=True)
    examenes_adjuntos = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        app_label = 'gestionProcesosApp'
        ordering = ['-timestamp_solicitud']
    
    def __str__(self):
        return f"Derivación {self.get_tipo_display()} - {self.servicio_destino}"


# ==================== GENERADOR DE CÓDIGO ====================

class GeneradorCodigo(models.Model):
    """Generador de códigos secuenciales"""
    TIPO_CHOICES = [
        ('FO', 'Ficha Obstétrica'),
        ('FP', 'Ficha Parto'),
        ('RN', 'Registro RN'),
        ('IP', 'Ingreso Paciente'),
    ]
    
    tipo = models.CharField(max_length=5, unique=True, choices=TIPO_CHOICES)
    prefijo = models.CharField(max_length=10)
    ultimo_numero = models.IntegerField(default=0)
    digitos_minimos = models.IntegerField(default=4)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'gestionProcesosApp'
        verbose_name_plural = 'Generadores de Código'
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.prefijo}"
    
    def generar_codigo(self):
        """Genera el siguiente código"""
        self.ultimo_numero += 1
        codigo = f"{self.prefijo}{str(self.ultimo_numero).zfill(self.digitos_minimos)}"
        self.save()
        return codigo
