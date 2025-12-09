# 🔄 gestionProcesosApp

## Gestión de Procesos de Parto

App central del sistema OB_CARE que orquesta todo el flujo del proceso de parto, desde el inicio a los 8cm de dilatación hasta el cierre final con la liberación de sala.

---

## 📋 Tabla de Contenidos

1. [Descripción General](#1-descripción-general)
2. [Modelos](#2-modelos)
3. [Catálogos](#3-catálogos)
4. [URLs](#4-urls)
5. [Vistas Principales](#5-vistas-principales)
6. [Formularios](#6-formularios)
7. [Servicios de Negocio](#7-servicios-de-negocio)
8. [Sistema de Notificaciones](#8-sistema-de-notificaciones)
9. [Validadores](#9-validadores)
10. [Signals](#10-signals)
11. [Templates](#11-templates)
12. [Diagrama de Flujo](#12-diagrama-de-flujo)
13. [Permisos](#13-permisos)
14. [Tests](#14-tests)
15. [Notas Importantes](#15-notas-importantes)

---

## 1. Descripción General

### Propósito

`gestionProcesosApp` es la **app central** que implementa la lógica de negocio del flujo de parto optimizado:

- **Inicio a 8cm**: Maximiza uso de salas (paciente llega a 9-10cm cuando equipo está listo)
- **Confirmación en 1 minuto**: Garantiza respuesta inmediata del personal
- **Cronómetro oficial**: Solo el médico puede iniciar/finalizar
- **Apego 5 minutos**: Balance entre contacto inicial y eficiencia
- **Tiempo promedio**: ~1 hora por proceso

### Responsabilidades

| Responsabilidad | Descripción |
|-----------------|-------------|
| Gestión de Procesos | Crear, iniciar, finalizar procesos de parto |
| Asignación de Salas | Asignar y liberar salas automáticamente |
| Cálculo de Personal | Determinar personal requerido según número de bebés |
| Notificaciones | Enviar alertas push al personal asignado |
| Confirmaciones | Registrar confirmaciones con timeout de 60 segundos |
| Cronómetro | Controlar tiempo oficial del proceso |
| Trazabilidad | Registrar ingreso/egreso de personal a salas |
| Derivaciones | Manejar derivaciones a UCI u otras unidades |

---

## 2. Modelos

### 2.1 ProcesoParto (Modelo Principal)

```python
from django.db import models
from django.contrib.auth.models import User
from gestionApp.models import Paciente
from matronaApp.models import FichaObstetrica

class ProcesoParto(models.Model):
    """
    Modelo central que representa un proceso de parto completo.
    Desde el inicio (8cm) hasta la finalización y liberación de sala.
    """
    
    # ═══════════════════════════════════════════════════════════════
    # IDENTIFICACIÓN
    # ═══════════════════════════════════════════════════════════════
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name="Código de Proceso"
    )  # Formato: MT-0001, MT-0002, etc.
    
    # ═══════════════════════════════════════════════════════════════
    # RELACIONES PRINCIPALES
    # ═══════════════════════════════════════════════════════════════
    ficha_obstetrica = models.OneToOneField(
        FichaObstetrica,
        on_delete=models.PROTECT,
        related_name='proceso_parto',
        verbose_name="Ficha Obstétrica"
    )
    
    sala = models.ForeignKey(
        'SalaParto',
        on_delete=models.PROTECT,
        related_name='procesos',
        verbose_name="Sala Asignada"
    )
    
    sala_real = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Sala Real",
        help_text="Si el parto ocurrió en otro lugar (ej: urgencias)"
    )
    
    # ═══════════════════════════════════════════════════════════════
    # CLASIFICACIÓN
    # ═══════════════════════════════════════════════════════════════
    tipo_paciente = models.ForeignKey(
        'CatalogoTipoPaciente',
        on_delete=models.PROTECT,
        verbose_name="Tipo de Paciente"
    )
    
    tipo_parto = models.ForeignKey(
        'CatalogoTipoProceso',
        on_delete=models.PROTECT,
        verbose_name="Tipo de Parto"
    )
    
    prioridad = models.ForeignKey(
        'CatalogoPrioridad',
        on_delete=models.PROTECT,
        verbose_name="Prioridad"
    )
    
    nivel_riesgo = models.ForeignKey(
        'CatalogoNivelRiesgo',
        on_delete=models.PROTECT,
        verbose_name="Nivel de Riesgo"
    )
    
    # ═══════════════════════════════════════════════════════════════
    # ESTADO DEL PROCESO
    # ═══════════════════════════════════════════════════════════════
    estado = models.ForeignKey(
        'CatalogoEstadoProceso',
        on_delete=models.PROTECT,
        verbose_name="Estado"
    )
    
    # ═══════════════════════════════════════════════════════════════
    # TIMESTAMPS CRÍTICOS
    # ═══════════════════════════════════════════════════════════════
    # Momento en que matrona presiona "Iniciar Proceso"
    hora_inicio_proceso = models.DateTimeField(
        verbose_name="Hora Inicio Proceso"
    )
    
    # Momento en que sistema envía notificaciones
    hora_notificaciones = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora Notificaciones Enviadas"
    )
    
    # Momento en que médico ingresa y marca inicio (CRONÓMETRO OFICIAL)
    hora_cronometro_inicio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora Inicio Cronómetro Oficial"
    )
    
    # Momento del nacimiento del primer bebé
    hora_nacimiento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora Nacimiento"
    )
    
    # Momento en que médico finaliza el proceso
    hora_cronometro_fin = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora Fin Cronómetro Oficial"
    )
    
    # ═══════════════════════════════════════════════════════════════
    # PERSONAL
    # ═══════════════════════════════════════════════════════════════
    personal_requerido = models.JSONField(
        default=dict,
        verbose_name="Personal Requerido",
        help_text="Cálculo automático según número de bebés"
    )
    # Ejemplo: {"medicos": 1, "matronas": 1, "tens": 3, "anestesiologo": 0, "total": 5}
    
    medico_responsable = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='procesos_como_responsable',
        null=True,
        blank=True,
        verbose_name="Médico Responsable"
    )
    
    # ═══════════════════════════════════════════════════════════════
    # DERIVACIÓN (si aplica)
    # ═══════════════════════════════════════════════════════════════
    derivacion_destino = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Destino Derivación"
    )  # UCI, NEONATOLOGIA, etc.
    
    derivacion_motivo = models.TextField(
        blank=True,
        verbose_name="Motivo Derivación"
    )
    
    derivacion_hora = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora Derivación"
    )
    
    # ═══════════════════════════════════════════════════════════════
    # EMERGENCIA EXTERNA
    # ═══════════════════════════════════════════════════════════════
    es_emergencia_externa = models.BooleanField(
        default=False,
        verbose_name="Es Emergencia Externa"
    )
    
    tiempo_llegada_estimado = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Tiempo Llegada Estimado (min)"
    )
    
    origen_emergencia = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Origen Emergencia"
    )  # Nombre del consultorio, ambulancia, etc.
    
    # ═══════════════════════════════════════════════════════════════
    # OBSERVACIONES
    # ═══════════════════════════════════════════════════════════════
    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones"
    )
    
    # ═══════════════════════════════════════════════════════════════
    # AUDITORÍA
    # ═══════════════════════════════════════════════════════════════
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='procesos_creados',
        verbose_name="Creado Por"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Proceso de Parto"
        verbose_name_plural = "Procesos de Parto"
        ordering = ['-hora_inicio_proceso']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['estado', 'hora_inicio_proceso']),
            models.Index(fields=['sala', 'estado']),
        ]
    
    def __str__(self):
        return f"{self.codigo} - {self.ficha_obstetrica.paciente}"
    
    # ═══════════════════════════════════════════════════════════════
    # PROPIEDADES CALCULADAS
    # ═══════════════════════════════════════════════════════════════
    @property
    def duracion_cronometro(self):
        """Duración oficial del proceso en minutos"""
        if self.hora_cronometro_inicio and self.hora_cronometro_fin:
            delta = self.hora_cronometro_fin - self.hora_cronometro_inicio
            return int(delta.total_seconds() / 60)
        return None
    
    @property
    def num_bebes(self):
        """Número de bebés del embarazo"""
        return self.ficha_obstetrica.num_bebes
    
    @property
    def todas_confirmaciones_recibidas(self):
        """Verifica si todo el personal confirmó"""
        total_requerido = self.personal_requerido.get('total', 0)
        confirmados = self.confirmaciones.filter(confirmado=True).count()
        return confirmados >= total_requerido
    
    @property
    def recien_nacidos(self):
        """Recién nacidos asociados al proceso"""
        return self.registros_recien_nacido.all()
    
    # ═══════════════════════════════════════════════════════════════
    # MÉTODOS DE NEGOCIO
    # ═══════════════════════════════════════════════════════════════
    def generar_codigo(self):
        """Genera código único MT-XXXX"""
        from django.db.models import Max
        ultimo = ProcesoParto.objects.aggregate(Max('id'))['id__max'] or 0
        return f"MT-{(ultimo + 1):04d}"
    
    def puede_iniciar_cronometro(self, usuario):
        """Valida si el usuario puede iniciar el cronómetro"""
        if not usuario.groups.filter(name='medico').exists():
            return False, "Solo médicos pueden iniciar el cronómetro"
        if self.hora_cronometro_inicio:
            return False, "El cronómetro ya fue iniciado"
        if self.estado.codigo != 'CONFIRMADO':
            return False, "El equipo debe estar confirmado"
        return True, None
    
    def puede_finalizar(self, usuario):
        """Valida si se puede finalizar el proceso"""
        if not usuario.groups.filter(name='medico').exists():
            return False, "Solo médicos pueden finalizar"
        if not self.hora_cronometro_inicio:
            return False, "El cronómetro no ha sido iniciado"
        
        # Verificar que todos los bebés estén registrados
        bebes_registrados = self.recien_nacidos.count()
        if bebes_registrados < self.num_bebes:
            return False, f"Faltan registrar {self.num_bebes - bebes_registrados} bebé(s)"
        
        return True, None
```

### 2.2 SalaParto

```python
class SalaParto(models.Model):
    """
    Salas de parto disponibles en el hospital.
    Estado se actualiza automáticamente según procesos.
    """
    
    nombre = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Nombre"
    )  # "A", "B", "C", "D"
    
    estado = models.ForeignKey(
        'CatalogoEstadoSala',
        on_delete=models.PROTECT,
        verbose_name="Estado"
    )
    
    # Características
    tiene_quirofano = models.BooleanField(
        default=False,
        verbose_name="Tiene Quirófano"
    )
    
    capacidad_bebes = models.PositiveIntegerField(
        default=1,
        verbose_name="Capacidad de Bebés"
    )
    
    tiene_monitor_fetal = models.BooleanField(
        default=True,
        verbose_name="Tiene Monitor Fetal"
    )
    
    tiene_cuna_termica = models.BooleanField(
        default=True,
        verbose_name="Tiene Cuna Térmica"
    )
    
    # Ubicación
    piso = models.PositiveIntegerField(
        default=1,
        verbose_name="Piso"
    )
    
    sector = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Sector"
    )
    
    # Estado actual
    proceso_actual = models.OneToOneField(
        ProcesoParto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sala_ocupada',
        verbose_name="Proceso Actual"
    )
    
    # Auditoría
    ultima_limpieza = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Última Limpieza"
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )
    
    class Meta:
        verbose_name = "Sala de Parto"
        verbose_name_plural = "Salas de Parto"
        ordering = ['nombre']
    
    def __str__(self):
        return f"Sala {self.nombre}"
    
    @property
    def esta_disponible(self):
        return self.estado.codigo == 'DISPONIBLE' and self.activa
    
    def ocupar(self, proceso):
        """Marca la sala como ocupada por un proceso"""
        self.proceso_actual = proceso
        self.estado = CatalogoEstadoSala.objects.get(codigo='OCUPADA')
        self.save()
    
    def liberar(self):
        """Libera la sala y la pone en limpieza"""
        self.proceso_actual = None
        self.estado = CatalogoEstadoSala.objects.get(codigo='LIMPIEZA')
        self.save()
    
    def marcar_disponible(self):
        """Marca la sala como disponible después de limpieza"""
        from django.utils import timezone
        self.estado = CatalogoEstadoSala.objects.get(codigo='DISPONIBLE')
        self.ultima_limpieza = timezone.now()
        self.save()
```

### 2.3 ConfirmacionPersonal

```python
class ConfirmacionPersonal(models.Model):
    """
    Registro de confirmaciones del personal asignado.
    Timeout de 60 segundos para confirmar.
    """
    
    proceso = models.ForeignKey(
        ProcesoParto,
        on_delete=models.CASCADE,
        related_name='confirmaciones',
        verbose_name="Proceso"
    )
    
    profesional = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='confirmaciones_procesos',
        verbose_name="Profesional"
    )
    
    rol = models.ForeignKey(
        'CatalogoRolProceso',
        on_delete=models.PROTECT,
        verbose_name="Rol Asignado"
    )  # MEDICO, MATRONA, TENS, ANESTESIOLOGO
    
    # Timestamps
    hora_notificacion = models.DateTimeField(
        verbose_name="Hora Notificación"
    )
    
    hora_confirmacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora Confirmación"
    )
    
    # Estado
    confirmado = models.BooleanField(
        default=False,
        verbose_name="Confirmado"
    )
    
    # Métricas
    tiempo_respuesta_segundos = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Tiempo Respuesta (seg)"
    )
    
    dentro_tiempo = models.BooleanField(
        default=False,
        verbose_name="Dentro de Tiempo",
        help_text="Confirmó en menos de 60 segundos"
    )
    
    # Reemplazo (si no confirmó a tiempo)
    es_reemplazo = models.BooleanField(
        default=False,
        verbose_name="Es Reemplazo"
    )
    
    reemplaza_a = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reemplazado_por',
        verbose_name="Reemplaza A"
    )
    
    class Meta:
        verbose_name = "Confirmación de Personal"
        verbose_name_plural = "Confirmaciones de Personal"
        unique_together = ['proceso', 'profesional']
        ordering = ['hora_notificacion']
    
    def __str__(self):
        estado = "✓" if self.confirmado else "✗"
        return f"{estado} {self.profesional} - {self.proceso.codigo}"
    
    def confirmar(self):
        """Registra la confirmación del profesional"""
        from django.utils import timezone
        
        ahora = timezone.now()
        self.hora_confirmacion = ahora
        self.confirmado = True
        
        # Calcular tiempo de respuesta
        delta = ahora - self.hora_notificacion
        self.tiempo_respuesta_segundos = int(delta.total_seconds())
        self.dentro_tiempo = self.tiempo_respuesta_segundos <= 60
        
        self.save()
```

### 2.4 RegistroIngresoSala

```python
class RegistroIngresoSala(models.Model):
    """
    Trazabilidad de entrada/salida de personal a salas.
    Permite control de acceso y auditoría.
    """
    
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
        ('REINGRESO', 'Reingreso'),
    ]
    
    proceso = models.ForeignKey(
        ProcesoParto,
        on_delete=models.CASCADE,
        related_name='registros_ingreso',
        verbose_name="Proceso"
    )
    
    profesional = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ingresos_salas',
        verbose_name="Profesional"
    )
    
    sala = models.ForeignKey(
        SalaParto,
        on_delete=models.PROTECT,
        related_name='registros_ingreso',
        verbose_name="Sala"
    )
    
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        verbose_name="Tipo"
    )
    
    hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Hora"
    )
    
    motivo_salida = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Motivo de Salida"
    )  # "Traslado bebé a registro", "Emergencia en otra sala", etc.
    
    class Meta:
        verbose_name = "Registro de Ingreso a Sala"
        verbose_name_plural = "Registros de Ingreso a Sala"
        ordering = ['-hora']
    
    def __str__(self):
        return f"{self.tipo} - {self.profesional} - Sala {self.sala.nombre}"
```

### 2.5 AsignacionPersonal

```python
class AsignacionPersonal(models.Model):
    """
    Asignación específica de personal a un proceso.
    Incluye asignación a bebé específico en caso de múltiples.
    """
    
    proceso = models.ForeignKey(
        ProcesoParto,
        on_delete=models.CASCADE,
        related_name='asignaciones',
        verbose_name="Proceso"
    )
    
    profesional = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='asignaciones_procesos',
        verbose_name="Profesional"
    )
    
    rol = models.ForeignKey(
        'CatalogoRolProceso',
        on_delete=models.PROTECT,
        verbose_name="Rol"
    )
    
    # Para embarazos múltiples
    bebe_asignado = models.CharField(
        max_length=1,
        blank=True,
        verbose_name="Bebé Asignado"
    )  # "A", "B", "C" para identificar a cuál bebé atiende
    
    es_responsable_principal = models.BooleanField(
        default=False,
        verbose_name="Es Responsable Principal"
    )
    
    hora_asignacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Hora Asignación"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Asignación de Personal"
        verbose_name_plural = "Asignaciones de Personal"
        unique_together = ['proceso', 'profesional', 'rol']
    
    def __str__(self):
        bebe = f" (Bebé {self.bebe_asignado})" if self.bebe_asignado else ""
        return f"{self.profesional} - {self.rol}{bebe}"
```

### 2.6 NotificacionProceso

```python
class NotificacionProceso(models.Model):
    """
    Registro de notificaciones enviadas.
    Soporta push notifications y otros canales.
    """
    
    TIPO_CHOICES = [
        ('URGENTE', 'Urgente'),
        ('CODIGO_ROJO', 'Código Rojo'),
        ('EMERGENCIA_EXTERNA', 'Emergencia Externa'),
        ('INFORMATIVO', 'Informativo'),
    ]
    
    CANAL_CHOICES = [
        ('PUSH', 'Push Notification'),
        ('SMS', 'SMS'),
        ('EMAIL', 'Email'),
        ('SISTEMA', 'Notificación del Sistema'),
    ]
    
    proceso = models.ForeignKey(
        ProcesoParto,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        verbose_name="Proceso"
    )
    
    destinatario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='notificaciones_recibidas',
        verbose_name="Destinatario"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name="Tipo"
    )
    
    canal = models.CharField(
        max_length=10,
        choices=CANAL_CHOICES,
        default='PUSH',
        verbose_name="Canal"
    )
    
    mensaje = models.TextField(
        verbose_name="Mensaje"
    )
    
    # Estado de entrega
    enviada = models.BooleanField(
        default=False,
        verbose_name="Enviada"
    )
    
    hora_envio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora Envío"
    )
    
    entregada = models.BooleanField(
        default=False,
        verbose_name="Entregada"
    )
    
    hora_entrega = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora Entrega"
    )
    
    leida = models.BooleanField(
        default=False,
        verbose_name="Leída"
    )
    
    hora_lectura = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora Lectura"
    )
    
    # Error si falló
    error = models.TextField(
        blank=True,
        verbose_name="Error"
    )
    
    class Meta:
        verbose_name = "Notificación de Proceso"
        verbose_name_plural = "Notificaciones de Proceso"
        ordering = ['-hora_envio']
    
    def __str__(self):
        return f"{self.tipo} → {self.destinatario} ({self.proceso.codigo})"
```

### 2.7 EventoProceso

```python
class EventoProceso(models.Model):
    """
    Log de eventos del proceso para auditoría completa.
    Registra cada acción importante del flujo.
    """
    
    EVENTO_CHOICES = [
        ('PROCESO_CREADO', 'Proceso Creado'),
        ('PROCESO_INICIADO', 'Proceso Iniciado'),
        ('NOTIFICACIONES_ENVIADAS', 'Notificaciones Enviadas'),
        ('CONFIRMACION_RECIBIDA', 'Confirmación Recibida'),
        ('TIMEOUT_CONFIRMACION', 'Timeout Confirmación'),
        ('REEMPLAZO_ASIGNADO', 'Reemplazo Asignado'),
        ('CRONOMETRO_INICIADO', 'Cronómetro Iniciado'),
        ('BEBE_NACIDO', 'Bebé Nacido'),
        ('APEGO_INICIADO', 'Apego Iniciado'),
        ('APEGO_COMPLETADO', 'Apego Completado'),
        ('TRASLADO_REGISTRO', 'Traslado a Registro'),
        ('REGISTRO_COMPLETO', 'Registro Completo'),
        ('DERIVACION_UCI', 'Derivación a UCI'),
        ('PROCESO_FINALIZADO', 'Proceso Finalizado'),
        ('SALA_LIBERADA', 'Sala Liberada'),
        ('INGRESO_SALA', 'Ingreso a Sala'),
        ('SALIDA_SALA', 'Salida de Sala'),
    ]
    
    proceso = models.ForeignKey(
        ProcesoParto,
        on_delete=models.CASCADE,
        related_name='eventos',
        verbose_name="Proceso"
    )
    
    evento = models.CharField(
        max_length=30,
        choices=EVENTO_CHOICES,
        verbose_name="Evento"
    )
    
    hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Hora"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='eventos_procesos',
        verbose_name="Usuario"
    )
    
    detalle = models.JSONField(
        default=dict,
        verbose_name="Detalle"
    )
    
    class Meta:
        verbose_name = "Evento de Proceso"
        verbose_name_plural = "Eventos de Proceso"
        ordering = ['-hora']
    
    def __str__(self):
        return f"{self.proceso.codigo} - {self.evento}"
```

---

## 3. Catálogos

### 3.1 Lista de Catálogos

```python
class CatalogoEstadoProceso(models.Model):
    """Estados del proceso de parto"""
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6c757d')  # Hex color
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Estado de Proceso"
        ordering = ['orden']


class CatalogoEstadoSala(models.Model):
    """Estados de las salas de parto"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#6c757d')
    activo = models.BooleanField(default=True)


class CatalogoTipoPaciente(models.Model):
    """Tipos de paciente al iniciar proceso"""
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)


class CatalogoTipoProceso(models.Model):
    """Tipos de proceso/parto"""
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    requiere_quirofano = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)


class CatalogoPrioridad(models.Model):
    """Niveles de prioridad"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    nivel = models.PositiveIntegerField()  # 1=más urgente
    color = models.CharField(max_length=7)
    tiempo_respuesta_max = models.PositiveIntegerField()  # segundos
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nivel']


class CatalogoNivelRiesgo(models.Model):
    """Niveles de riesgo obstétrico"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=7)
    activo = models.BooleanField(default=True)


class CatalogoRolProceso(models.Model):
    """Roles en el proceso de parto"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    grupo_django = models.CharField(max_length=50)  # Mapeo a auth.Group
    orden_llegada = models.PositiveIntegerField()  # 1=TENS, 2=Matrona, 3=Médico
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['orden_llegada']
```

### 3.2 Datos Iniciales de Catálogos

```python
# Estados del Proceso
ESTADOS_PROCESO = [
    {'codigo': 'CREADO', 'nombre': 'Creado', 'color': '#6c757d', 'orden': 1},
    {'codigo': 'INICIADO', 'nombre': 'Iniciado', 'color': '#17a2b8', 'orden': 2},
    {'codigo': 'NOTIFICANDO', 'nombre': 'Notificando', 'color': '#ffc107', 'orden': 3},
    {'codigo': 'CONFIRMADO', 'nombre': 'Confirmado', 'color': '#28a745', 'orden': 4},
    {'codigo': 'CONFIRMADO_PARCIAL', 'nombre': 'Confirmado Parcial', 'color': '#fd7e14', 'orden': 5},
    {'codigo': 'ESCALADO', 'nombre': 'Escalado', 'color': '#dc3545', 'orden': 6},
    {'codigo': 'EN_CURSO', 'nombre': 'En Curso', 'color': '#007bff', 'orden': 7},
    {'codigo': 'CERRADO', 'nombre': 'Cerrado', 'color': '#28a745', 'orden': 8},
    {'codigo': 'CERRADO_DERIVACION', 'nombre': 'Cerrado con Derivación', 'color': '#6f42c1', 'orden': 9},
]

# Estados de Sala
ESTADOS_SALA = [
    {'codigo': 'DISPONIBLE', 'nombre': 'Disponible', 'color': '#28a745'},
    {'codigo': 'OCUPADA', 'nombre': 'Ocupada', 'color': '#dc3545'},
    {'codigo': 'LIMPIEZA', 'nombre': 'En Limpieza', 'color': '#ffc107'},
    {'codigo': 'MANTENIMIENTO', 'nombre': 'En Mantenimiento', 'color': '#6c757d'},
]

# Tipos de Paciente
TIPOS_PACIENTE = [
    {'codigo': 'HOSPITALIZADA_ESPERA', 'nombre': 'Hospitalizada - Sala de Espera'},
    {'codigo': 'HOSPITALIZADA_PREQUIRURGICA', 'nombre': 'Hospitalizada - Pre-quirúrgica'},
    {'codigo': 'HOSPITALIZADA_CRITICA', 'nombre': 'Hospitalizada - Caso Crítico'},
    {'codigo': 'EXTERNA_AMBULANCIA', 'nombre': 'Externa - Ambulancia'},
    {'codigo': 'EXTERNA_URGENCIAS', 'nombre': 'Externa - Urgencias'},
]

# Tipos de Proceso
TIPOS_PROCESO = [
    {'codigo': 'PARTO_NORMAL', 'nombre': 'Parto Normal', 'requiere_quirofano': False},
    {'codigo': 'CESAREA_PROGRAMADA', 'nombre': 'Cesárea Programada', 'requiere_quirofano': True},
    {'codigo': 'CESAREA_EMERGENCIA', 'nombre': 'Cesárea de Emergencia', 'requiere_quirofano': True},
    {'codigo': 'EMERGENCIA_EXTERNA', 'nombre': 'Emergencia Externa', 'requiere_quirofano': False},
]

# Prioridades
PRIORIDADES = [
    {'codigo': 'P1_EMERGENCIA', 'nombre': 'P1 - Emergencia', 'nivel': 1, 'color': '#dc3545', 'tiempo_respuesta_max': 30},
    {'codigo': 'P2_ALTA', 'nombre': 'P2 - Alta', 'nivel': 2, 'color': '#fd7e14', 'tiempo_respuesta_max': 45},
    {'codigo': 'P3_PRIORITARIA', 'nombre': 'P3 - Prioritaria', 'nivel': 3, 'color': '#ffc107', 'tiempo_respuesta_max': 60},
    {'codigo': 'P4_NORMAL', 'nombre': 'P4 - Normal', 'nivel': 4, 'color': '#28a745', 'tiempo_respuesta_max': 60},
]

# Niveles de Riesgo
NIVELES_RIESGO = [
    {'codigo': 'CRITICO', 'nombre': 'Crítico', 'color': '#dc3545'},
    {'codigo': 'ALTO', 'nombre': 'Alto', 'color': '#fd7e14'},
    {'codigo': 'MEDIO', 'nombre': 'Medio', 'color': '#ffc107'},
    {'codigo': 'BAJO', 'nombre': 'Bajo', 'color': '#28a745'},
]

# Roles en Proceso
ROLES_PROCESO = [
    {'codigo': 'MEDICO', 'nombre': 'Médico', 'grupo_django': 'medico', 'orden_llegada': 3},
    {'codigo': 'MATRONA', 'nombre': 'Matrona', 'grupo_django': 'matrona', 'orden_llegada': 2},
    {'codigo': 'TENS', 'nombre': 'TENS', 'grupo_django': 'tens', 'orden_llegada': 1},
    {'codigo': 'ANESTESIOLOGO', 'nombre': 'Anestesiólogo', 'grupo_django': 'medico', 'orden_llegada': 2},
]
```

---

## 4. URLs

```python
# gestionProcesosApp/urls.py

from django.urls import path
from . import views

app_name = 'procesos'

urlpatterns = [
    # ═══════════════════════════════════════════════════════════════
    # DASHBOARD Y LISTADOS
    # ═══════════════════════════════════════════════════════════════
    path('', views.dashboard_procesos, name='dashboard'),
    path('activos/', views.procesos_activos, name='activos'),
    path('historial/', views.historial_procesos, name='historial'),
    
    # ═══════════════════════════════════════════════════════════════
    # GESTIÓN DE PROCESOS
    # ═══════════════════════════════════════════════════════════════
    path('iniciar/', views.iniciar_proceso, name='iniciar'),
    path('iniciar/<int:ficha_id>/', views.iniciar_proceso, name='iniciar_con_ficha'),
    path('<str:codigo>/', views.detalle_proceso, name='detalle'),
    path('<str:codigo>/cronometro/iniciar/', views.iniciar_cronometro, name='iniciar_cronometro'),
    path('<str:codigo>/cronometro/finalizar/', views.finalizar_proceso, name='finalizar'),
    path('<str:codigo>/derivar/', views.derivar_uci, name='derivar_uci'),
    
    # ═══════════════════════════════════════════════════════════════
    # CONFIRMACIONES
    # ═══════════════════════════════════════════════════════════════
    path('<str:codigo>/confirmar/', views.confirmar_asistencia, name='confirmar'),
    path('<str:codigo>/confirmaciones/', views.ver_confirmaciones, name='confirmaciones'),
    
    # ═══════════════════════════════════════════════════════════════
    # REGISTRO DE INGRESO A SALA
    # ═══════════════════════════════════════════════════════════════
    path('<str:codigo>/ingreso/', views.registrar_ingreso, name='registrar_ingreso'),
    path('<str:codigo>/salida/', views.registrar_salida, name='registrar_salida'),
    
    # ═══════════════════════════════════════════════════════════════
    # EMERGENCIAS
    # ═══════════════════════════════════════════════════════════════
    path('emergencia/crear/', views.crear_ficha_emergencia, name='crear_emergencia'),
    path('emergencia/<int:ficha_id>/completar/', views.completar_emergencia, name='completar_emergencia'),
    
    # ═══════════════════════════════════════════════════════════════
    # SALAS
    # ═══════════════════════════════════════════════════════════════
    path('salas/', views.estado_salas, name='salas'),
    path('salas/<int:sala_id>/liberar/', views.liberar_sala, name='liberar_sala'),
    
    # ═══════════════════════════════════════════════════════════════
    # NOTIFICACIONES
    # ═══════════════════════════════════════════════════════════════
    path('notificaciones/', views.mis_notificaciones, name='notificaciones'),
    path('notificaciones/<int:pk>/leer/', views.marcar_leida, name='marcar_leida'),
    
    # ═══════════════════════════════════════════════════════════════
    # API ENDPOINTS (para AJAX y tiempo real)
    # ═══════════════════════════════════════════════════════════════
    path('api/proceso/<str:codigo>/estado/', views.api_estado_proceso, name='api_estado'),
    path('api/salas/disponibles/', views.api_salas_disponibles, name='api_salas'),
    path('api/personal/disponible/', views.api_personal_disponible, name='api_personal'),
]
```

---

## 5. Vistas Principales

### 5.1 Iniciar Proceso

```python
# gestionProcesosApp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db import transaction

from .models import ProcesoParto, SalaParto, ConfirmacionPersonal
from .services import ProcesoService, NotificacionService, PersonalService
from .decorators import roles_required


@login_required
@roles_required(['matrona', 'coordinador'])
def iniciar_proceso(request, ficha_id=None):
    """
    Vista para iniciar un nuevo proceso de parto.
    Trigger: Paciente alcanza 8cm de dilatación.
    """
    
    if ficha_id:
        ficha = get_object_or_404(FichaObstetrica, pk=ficha_id)
    else:
        ficha = None
    
    if request.method == 'POST':
        form = IniciarProcesoForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Usar servicio para crear proceso
                    proceso = ProcesoService.iniciar_proceso(
                        ficha_obstetrica=form.cleaned_data['ficha_obstetrica'],
                        tipo_paciente=form.cleaned_data['tipo_paciente'],
                        usuario=request.user
                    )
                    
                    messages.success(
                        request,
                        f'Proceso {proceso.codigo} iniciado. '
                        f'Sala {proceso.sala.nombre} asignada. '
                        f'Notificaciones enviadas a {proceso.personal_requerido["total"]} profesionales.'
                    )
                    
                    return redirect('procesos:detalle', codigo=proceso.codigo)
                    
            except Exception as e:
                messages.error(request, f'Error al iniciar proceso: {str(e)}')
    else:
        form = IniciarProcesoForm(initial={'ficha_obstetrica': ficha})
    
    # Obtener fichas que pueden iniciar proceso (dilatación >= 8cm)
    fichas_disponibles = FichaObstetrica.objects.filter(
        dilatacion_actual__gte=8,
        estado='ACTIVA'
    ).exclude(
        proceso_parto__isnull=False
    )
    
    return render(request, 'gestionProcesosApp/iniciar_proceso.html', {
        'form': form,
        'ficha': ficha,
        'fichas_disponibles': fichas_disponibles,
    })


@login_required
@roles_required(['medico'])
def iniciar_cronometro(request, codigo):
    """
    Médico inicia el cronómetro oficial del proceso.
    Este es el momento único que marca el inicio de atención formal.
    """
    
    proceso = get_object_or_404(ProcesoParto, codigo=codigo)
    
    # Validar permisos
    puede, error = proceso.puede_iniciar_cronometro(request.user)
    if not puede:
        messages.error(request, error)
        return redirect('procesos:detalle', codigo=codigo)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                ProcesoService.iniciar_cronometro(proceso, request.user)
                
                messages.success(
                    request,
                    f'Cronómetro iniciado a las {proceso.hora_cronometro_inicio.strftime("%H:%M:%S")}'
                )
                
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('procesos:detalle', codigo=codigo)


@login_required
@roles_required(['medico'])
def finalizar_proceso(request, codigo):
    """
    Médico finaliza el proceso de parto.
    Valida que todos los datos estén completos.
    """
    
    proceso = get_object_or_404(ProcesoParto, codigo=codigo)
    
    # Validar
    puede, error = proceso.puede_finalizar(request.user)
    if not puede:
        messages.error(request, error)
        return redirect('procesos:detalle', codigo=codigo)
    
    if request.method == 'POST':
        form = FinalizarProcesoForm(request.POST, proceso=proceso)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    ProcesoService.finalizar_proceso(
                        proceso=proceso,
                        usuario=request.user,
                        observaciones=form.cleaned_data.get('observaciones', '')
                    )
                    
                    messages.success(
                        request,
                        f'Proceso {proceso.codigo} finalizado. '
                        f'Duración: {proceso.duracion_cronometro} minutos. '
                        f'Sala {proceso.sala.nombre} liberada.'
                    )
                    
                    return redirect('procesos:dashboard')
                    
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = FinalizarProcesoForm(proceso=proceso)
    
    return render(request, 'gestionProcesosApp/finalizar_proceso.html', {
        'proceso': proceso,
        'form': form,
    })


@login_required
def confirmar_asistencia(request, codigo):
    """
    Profesional confirma su asistencia al proceso.
    Timeout: 60 segundos desde la notificación.
    """
    
    proceso = get_object_or_404(ProcesoParto, codigo=codigo)
    
    # Buscar confirmación pendiente del usuario
    confirmacion = get_object_or_404(
        ConfirmacionPersonal,
        proceso=proceso,
        profesional=request.user,
        confirmado=False
    )
    
    if request.method == 'POST':
        confirmacion.confirmar()
        
        # Verificar si todos confirmaron
        if proceso.todas_confirmaciones_recibidas:
            proceso.estado = CatalogoEstadoProceso.objects.get(codigo='CONFIRMADO')
            proceso.save()
        
        tiempo = confirmacion.tiempo_respuesta_segundos
        estado = "✓ a tiempo" if confirmacion.dentro_tiempo else "⚠️ tardío"
        
        messages.success(
            request,
            f'Confirmación registrada en {tiempo} segundos ({estado}). '
            f'Dirigirse a Sala {proceso.sala.nombre}.'
        )
        
        return redirect('procesos:detalle', codigo=codigo)
    
    return render(request, 'gestionProcesosApp/confirmar_asistencia.html', {
        'proceso': proceso,
        'confirmacion': confirmacion,
    })
```

---

## 6. Formularios

```python
# gestionProcesosApp/forms.py

from django import forms
from .models import ProcesoParto, SalaParto
from matronaApp.models import FichaObstetrica


class IniciarProcesoForm(forms.Form):
    """Formulario para iniciar proceso de parto"""
    
    ficha_obstetrica = forms.ModelChoiceField(
        queryset=FichaObstetrica.objects.filter(estado='ACTIVA'),
        label="Ficha Obstétrica",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tipo_paciente = forms.ModelChoiceField(
        queryset=CatalogoTipoPaciente.objects.filter(activo=True),
        label="Tipo de Paciente",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def clean_ficha_obstetrica(self):
        ficha = self.cleaned_data['ficha_obstetrica']
        
        # Validar dilatación >= 8cm
        if ficha.dilatacion_actual < 8:
            raise forms.ValidationError(
                f'La dilatación actual es {ficha.dilatacion_actual}cm. '
                f'Se requiere al menos 8cm para iniciar el proceso.'
            )
        
        # Validar que no tenga proceso activo
        if hasattr(ficha, 'proceso_parto'):
            raise forms.ValidationError(
                'Esta ficha ya tiene un proceso de parto asociado.'
            )
        
        return ficha


class FichaEmergenciaForm(forms.Form):
    """Formulario rápido para emergencias externas"""
    
    rut = forms.CharField(
        max_length=12,
        label="RUT",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9'
        })
    )
    
    nombre = forms.CharField(
        max_length=200,
        label="Nombre Completo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    edad = forms.IntegerField(
        min_value=10,
        max_value=60,
        label="Edad",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    TIPO_EMBARAZO_CHOICES = [
        ('SIMPLE', 'Simple (1 bebé)'),
        ('GEMELAR', 'Gemelar (2 bebés)'),
        ('MULTIPLE', 'Múltiple (3+ bebés)'),
    ]
    
    tipo_embarazo = forms.ChoiceField(
        choices=TIPO_EMBARAZO_CHOICES,
        label="Tipo de Embarazo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    num_bebes = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=1,
        label="Número de Bebés",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    dilatacion = forms.IntegerField(
        min_value=0,
        max_value=10,
        label="Dilatación Actual (cm)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    tiempo_llegada = forms.IntegerField(
        min_value=1,
        max_value=60,
        required=False,
        label="Tiempo Estimado de Llegada (min)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    origen = forms.CharField(
        max_length=200,
        required=False,
        label="Origen (consultorio, ambulancia)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class FinalizarProcesoForm(forms.Form):
    """Formulario para finalizar proceso"""
    
    observaciones = forms.CharField(
        required=False,
        label="Observaciones",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        })
    )
    
    confirmar = forms.BooleanField(
        required=True,
        label="Confirmo que todos los datos están completos"
    )
    
    def __init__(self, *args, proceso=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.proceso = proceso
    
    def clean(self):
        cleaned_data = super().clean()
        
        if self.proceso:
            # Verificar bebés registrados
            bebes_registrados = self.proceso.recien_nacidos.count()
            bebes_esperados = self.proceso.num_bebes
            
            if bebes_registrados < bebes_esperados:
                raise forms.ValidationError(
                    f'Faltan registrar {bebes_esperados - bebes_registrados} bebé(s). '
                    f'No se puede finalizar el proceso.'
                )
        
        return cleaned_data


class DerivacionUCIForm(forms.Form):
    """Formulario para derivar madre a UCI"""
    
    motivo = forms.CharField(
        label="Motivo de Derivación",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción detallada del motivo...'
        })
    )
    
    diagnostico = forms.CharField(
        label="Diagnóstico",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Preeclampsia severa con eclampsia inminente'
        })
    )
    
    requiere_ventilacion = forms.BooleanField(
        required=False,
        label="Requiere Ventilación Mecánica"
    )
    
    requiere_monitoreo_invasivo = forms.BooleanField(
        required=False,
        label="Requiere Monitoreo Invasivo"
    )
```

---

## 7. Servicios de Negocio

```python
# gestionProcesosApp/services.py

from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User

from .models import (
    ProcesoParto, SalaParto, ConfirmacionPersonal,
    AsignacionPersonal, EventoProceso, NotificacionProceso
)


class ProcesoService:
    """Servicio principal para gestión de procesos de parto"""
    
    TIMEOUT_CONFIRMACION = 60  # segundos
    DURACION_APEGO = 5  # minutos
    
    @classmethod
    @transaction.atomic
    def iniciar_proceso(cls, ficha_obstetrica, tipo_paciente, usuario):
        """
        Inicia un nuevo proceso de parto.
        
        1. Valida la ficha (>= 8cm, activa, sin proceso)
        2. Calcula personal requerido
        3. Asigna sala disponible
        4. Genera código único
        5. Crea el proceso
        6. Envía notificaciones al personal
        """
        
        # Validaciones
        if ficha_obstetrica.dilatacion_actual < 8:
            raise ValueError("Dilatación insuficiente (requiere >= 8cm)")
        
        if hasattr(ficha_obstetrica, 'proceso_parto'):
            raise ValueError("Ya existe un proceso para esta ficha")
        
        # Calcular personal
        personal = cls._calcular_personal(
            num_bebes=ficha_obstetrica.num_bebes,
            es_cesarea=tipo_paciente.codigo in ['HOSPITALIZADA_PREQUIRURGICA'],
            es_critico=tipo_paciente.codigo == 'HOSPITALIZADA_CRITICA'
        )
        
        # Asignar sala
        sala = cls._asignar_sala(
            requiere_quirofano=tipo_paciente.codigo in ['HOSPITALIZADA_PREQUIRURGICA'],
            capacidad_minima=ficha_obstetrica.num_bebes
        )
        
        if not sala:
            raise ValueError("No hay salas disponibles")
        
        # Determinar prioridad y riesgo
        prioridad = cls._determinar_prioridad(ficha_obstetrica, tipo_paciente)
        nivel_riesgo = cls._determinar_riesgo(ficha_obstetrica)
        
        # Crear proceso
        proceso = ProcesoParto.objects.create(
            codigo=ProcesoParto().generar_codigo(),
            ficha_obstetrica=ficha_obstetrica,
            sala=sala,
            tipo_paciente=tipo_paciente,
            tipo_parto=cls._determinar_tipo_parto(ficha_obstetrica, tipo_paciente),
            prioridad=prioridad,
            nivel_riesgo=nivel_riesgo,
            estado=CatalogoEstadoProceso.objects.get(codigo='INICIADO'),
            hora_inicio_proceso=timezone.now(),
            personal_requerido=personal,
            creado_por=usuario,
            es_emergencia_externa=tipo_paciente.codigo.startswith('EXTERNA_')
        )
        
        # Ocupar sala
        sala.ocupar(proceso)
        
        # Registrar evento
        EventoProceso.objects.create(
            proceso=proceso,
            evento='PROCESO_INICIADO',
            usuario=usuario,
            detalle={
                'tipo_paciente': tipo_paciente.codigo,
                'sala': sala.nombre,
                'personal_requerido': personal
            }
        )
        
        # Asignar y notificar personal
        cls._asignar_y_notificar_personal(proceso, usuario)
        
        return proceso
    
    @classmethod
    def _calcular_personal(cls, num_bebes, es_cesarea=False, es_critico=False):
        """
        Calcula personal requerido según fórmula:
        - Por bebé: 1 médico + 1 matrona + 1 TENS
        - Adicional: 2 TENS de apoyo
        - Cesárea: +1 anestesiólogo
        - Crítico: +1 médico de soporte
        """
        
        medicos = num_bebes
        matronas = num_bebes
        tens_bebes = num_bebes
        tens_apoyo = 2
        anestesiologo = 1 if es_cesarea else 0
        
        if es_critico:
            medicos += 1  # Médico de soporte
            anestesiologo = 1  # Siempre por si se necesita cesárea
        
        return {
            'medicos': medicos,
            'matronas': matronas,
            'tens': tens_bebes + tens_apoyo,
            'anestesiologo': anestesiologo,
            'total': medicos + matronas + tens_bebes + tens_apoyo + anestesiologo
        }
    
    @classmethod
    def _asignar_sala(cls, requiere_quirofano=False, capacidad_minima=1):
        """Busca y asigna una sala disponible"""
        
        query = SalaParto.objects.filter(
            estado__codigo='DISPONIBLE',
            activa=True,
            capacidad_bebes__gte=capacidad_minima
        )
        
        if requiere_quirofano:
            query = query.filter(tiene_quirofano=True)
        
        return query.first()
    
    @classmethod
    def _asignar_y_notificar_personal(cls, proceso, usuario):
        """Asigna personal disponible y envía notificaciones"""
        
        personal_req = proceso.personal_requerido
        ahora = timezone.now()
        
        # Buscar médicos disponibles
        medicos = PersonalService.buscar_disponibles('medico', personal_req['medicos'])
        matronas = PersonalService.buscar_disponibles('matrona', personal_req['matronas'])
        tens = PersonalService.buscar_disponibles('tens', personal_req['tens'])
        
        profesionales = []
        
        # Asignar médicos
        for i, medico in enumerate(medicos):
            rol = CatalogoRolProceso.objects.get(codigo='MEDICO')
            AsignacionPersonal.objects.create(
                proceso=proceso,
                profesional=medico,
                rol=rol,
                es_responsable_principal=(i == 0)
            )
            profesionales.append((medico, rol))
            
            if i == 0:
                proceso.medico_responsable = medico
                proceso.save()
        
        # Asignar matronas
        letras_bebes = 'ABCDEFGHIJ'
        for i, matrona in enumerate(matronas):
            rol = CatalogoRolProceso.objects.get(codigo='MATRONA')
            bebe = letras_bebes[i] if proceso.num_bebes > 1 and i < proceso.num_bebes else ''
            AsignacionPersonal.objects.create(
                proceso=proceso,
                profesional=matrona,
                rol=rol,
                bebe_asignado=bebe
            )
            profesionales.append((matrona, rol))
        
        # Asignar TENS
        for i, ten in enumerate(tens):
            rol = CatalogoRolProceso.objects.get(codigo='TENS')
            bebe = letras_bebes[i] if i < proceso.num_bebes else ''
            AsignacionPersonal.objects.create(
                proceso=proceso,
                profesional=ten,
                rol=rol,
                bebe_asignado=bebe
            )
            profesionales.append((ten, rol))
        
        # Anestesiólogo si es necesario
        if personal_req['anestesiologo'] > 0:
            anestesiologos = PersonalService.buscar_disponibles('medico', 1, especialidad='anestesiologia')
            for anest in anestesiologos:
                rol = CatalogoRolProceso.objects.get(codigo='ANESTESIOLOGO')
                AsignacionPersonal.objects.create(
                    proceso=proceso,
                    profesional=anest,
                    rol=rol
                )
                profesionales.append((anest, rol))
        
        # Enviar notificaciones
        proceso.hora_notificaciones = ahora
        proceso.save()
        
        for profesional, rol in profesionales:
            NotificacionService.enviar_notificacion_proceso(proceso, profesional, rol)
            
            # Crear registro de confirmación pendiente
            ConfirmacionPersonal.objects.create(
                proceso=proceso,
                profesional=profesional,
                rol=rol,
                hora_notificacion=ahora
            )
        
        # Registrar evento
        EventoProceso.objects.create(
            proceso=proceso,
            evento='NOTIFICACIONES_ENVIADAS',
            usuario=usuario,
            detalle={
                'cantidad': len(profesionales),
                'profesionales': [p.username for p, r in profesionales]
            }
        )
    
    @classmethod
    @transaction.atomic
    def iniciar_cronometro(cls, proceso, usuario):
        """
        Médico inicia el cronómetro oficial.
        Momento único que marca inicio de atención formal.
        """
        
        ahora = timezone.now()
        
        proceso.hora_cronometro_inicio = ahora
        proceso.medico_responsable = usuario
        proceso.estado = CatalogoEstadoProceso.objects.get(codigo='EN_CURSO')
        proceso.save()
        
        # Registrar evento
        EventoProceso.objects.create(
            proceso=proceso,
            evento='CRONOMETRO_INICIADO',
            usuario=usuario,
            detalle={'hora': ahora.isoformat()}
        )
        
        return proceso
    
    @classmethod
    @transaction.atomic
    def finalizar_proceso(cls, proceso, usuario, observaciones=''):
        """
        Finaliza el proceso de parto.
        Cierra fichas y libera sala.
        """
        
        ahora = timezone.now()
        
        proceso.hora_cronometro_fin = ahora
        proceso.estado = CatalogoEstadoProceso.objects.get(codigo='CERRADO')
        proceso.observaciones = observaciones
        proceso.save()
        
        # Cerrar ficha obstétrica
        proceso.ficha_obstetrica.estado = 'CERRADA'
        proceso.ficha_obstetrica.save()
        
        # Cerrar fichas de recién nacidos
        for rn in proceso.recien_nacidos.all():
            rn.estado = 'CERRADO'
            rn.save()
        
        # Liberar sala
        proceso.sala.liberar()
        
        # Registrar eventos
        EventoProceso.objects.create(
            proceso=proceso,
            evento='PROCESO_FINALIZADO',
            usuario=usuario,
            detalle={
                'duracion_minutos': proceso.duracion_cronometro,
                'hora_fin': ahora.isoformat()
            }
        )
        
        EventoProceso.objects.create(
            proceso=proceso,
            evento='SALA_LIBERADA',
            usuario=usuario,
            detalle={'sala': proceso.sala.nombre}
        )
        
        return proceso
    
    @classmethod
    @transaction.atomic
    def derivar_a_uci(cls, proceso, usuario, motivo, diagnostico):
        """
        Deriva la madre a UCI.
        Cierre parcial: proceso cerrado, bebés pueden seguir siendo registrados.
        """
        
        ahora = timezone.now()
        
        proceso.derivacion_destino = 'UCI'
        proceso.derivacion_motivo = f"{diagnostico}\n\n{motivo}"
        proceso.derivacion_hora = ahora
        proceso.hora_cronometro_fin = ahora
        proceso.estado = CatalogoEstadoProceso.objects.get(codigo='CERRADO_DERIVACION')
        proceso.save()
        
        # Marcar ficha obstétrica como derivada
        proceso.ficha_obstetrica.estado = 'CERRADA_DERIVADA_UCI'
        proceso.ficha_obstetrica.save()
        
        # Liberar sala
        proceso.sala.liberar()
        
        # Registrar evento
        EventoProceso.objects.create(
            proceso=proceso,
            evento='DERIVACION_UCI',
            usuario=usuario,
            detalle={
                'motivo': motivo,
                'diagnostico': diagnostico,
                'hora': ahora.isoformat()
            }
        )
        
        # Notificar a UCI
        NotificacionService.notificar_uci(proceso, diagnostico)
        
        return proceso


class PersonalService:
    """Servicio para gestión de personal"""
    
    @classmethod
    def buscar_disponibles(cls, rol, cantidad, especialidad=None):
        """
        Busca profesionales disponibles para un rol.
        Considera turno actual y procesos en curso.
        """
        
        from django.contrib.auth.models import User
        
        # Obtener usuarios del grupo correspondiente
        query = User.objects.filter(
            groups__name=rol,
            is_active=True
        )
        
        # Excluir los que están en procesos activos
        procesos_activos = ProcesoParto.objects.filter(
            estado__codigo__in=['INICIADO', 'CONFIRMADO', 'EN_CURSO']
        )
        
        usuarios_ocupados = AsignacionPersonal.objects.filter(
            proceso__in=procesos_activos,
            activo=True
        ).values_list('profesional_id', flat=True)
        
        query = query.exclude(id__in=usuarios_ocupados)
        
        # TODO: Filtrar por turno actual
        # TODO: Filtrar por especialidad si aplica
        
        return list(query[:cantidad])


class NotificacionService:
    """Servicio de notificaciones"""
    
    PLANTILLAS = {
        'URGENTE': """
URGENTE - RÁPIDO
Proceso de parto iniciado
Código: {codigo}
Paciente: {paciente}, {dilatacion}cm dilatación
Sala: {sala}
CONFIRMAR EN 1 MINUTO
        """,
        'CODIGO_ROJO': """
🔴 CÓDIGO ROJO - CASO CRÍTICO
Código: {codigo}
Paciente: {paciente}
Sala: {sala}
CONFIRMAR INMEDIATAMENTE
        """,
        'EMERGENCIA_EXTERNA': """
🔴 CÓDIGO ROJO - EMERGENCIA EXTERNA
Paciente llegando en {tiempo_llegada} minutos
{dilatacion}cm dilatación
Código: {codigo}
Sala: {sala}
CONFIRMAR AHORA
        """
    }
    
    @classmethod
    def enviar_notificacion_proceso(cls, proceso, profesional, rol):
        """Envía notificación push a un profesional"""
        
        # Determinar tipo de notificación
        if proceso.es_emergencia_externa:
            tipo = 'EMERGENCIA_EXTERNA'
        elif proceso.nivel_riesgo.codigo == 'CRITICO':
            tipo = 'CODIGO_ROJO'
        else:
            tipo = 'URGENTE'
        
        # Generar mensaje
        mensaje = cls.PLANTILLAS[tipo].format(
            codigo=proceso.codigo,
            paciente=proceso.ficha_obstetrica.paciente.nombre_completo,
            dilatacion=proceso.ficha_obstetrica.dilatacion_actual,
            sala=proceso.sala.nombre,
            tiempo_llegada=proceso.tiempo_llegada_estimado or '?'
        )
        
        # Crear registro
        notificacion = NotificacionProceso.objects.create(
            proceso=proceso,
            destinatario=profesional,
            tipo=tipo,
            mensaje=mensaje
        )
        
        # Enviar push notification
        cls._enviar_push(profesional, mensaje, proceso.codigo)
        
        notificacion.enviada = True
        notificacion.hora_envio = timezone.now()
        notificacion.save()
        
        return notificacion
    
    @classmethod
    def _enviar_push(cls, usuario, mensaje, codigo_proceso):
        """Envía push notification real (integrar con Firebase, etc.)"""
        # TODO: Implementar integración con servicio de push notifications
        pass
    
    @classmethod
    def notificar_uci(cls, proceso, diagnostico):
        """Notifica a UCI sobre derivación"""
        # TODO: Implementar notificación a UCI
        pass
```

---

## 8. Sistema de Notificaciones

### 8.1 Configuración de Push Notifications

```python
# gestionProcesosApp/notifications.py

from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials


class PushNotificationService:
    """Servicio de notificaciones push usando Firebase"""
    
    @classmethod
    def initialize(cls):
        """Inicializa Firebase Admin SDK"""
        cred = credentials.Certificate('path/to/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
    
    @classmethod
    def enviar(cls, token_dispositivo, titulo, mensaje, data=None):
        """
        Envía una notificación push.
        
        Args:
            token_dispositivo: Token FCM del dispositivo
            titulo: Título de la notificación
            mensaje: Cuerpo del mensaje
            data: Datos adicionales (dict)
        """
        
        notification = messaging.Notification(
            title=titulo,
            body=mensaje
        )
        
        message = messaging.Message(
            notification=notification,
            data=data or {},
            token=token_dispositivo,
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(
                    sound='urgente',
                    channel_id='proceso_parto'
                )
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound='urgente.wav',
                        badge=1
                    )
                )
            )
        )
        
        response = messaging.send(message)
        return response
    
    @classmethod
    def enviar_a_grupo(cls, tokens, titulo, mensaje, data=None):
        """Envía notificación a múltiples dispositivos"""
        
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=titulo,
                body=mensaje
            ),
            data=data or {},
            tokens=tokens
        )
        
        response = messaging.send_multicast(message)
        return response
```

### 8.2 Consumer WebSocket (Tiempo Real)

```python
# gestionProcesosApp/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ProcesoConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer para actualizaciones en tiempo real"""
    
    async def connect(self):
        self.proceso_codigo = self.scope['url_route']['kwargs']['codigo']
        self.room_group_name = f'proceso_{self.proceso_codigo}'
        
        # Unirse al grupo del proceso
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'subscribe':
            # Enviar estado actual
            estado = await self.get_estado_proceso()
            await self.send(text_data=json.dumps({
                'type': 'estado_actual',
                'data': estado
            }))
    
    # Handlers para eventos del proceso
    async def confirmacion_recibida(self, event):
        await self.send(text_data=json.dumps({
            'type': 'confirmacion',
            'data': event['data']
        }))
    
    async def cronometro_iniciado(self, event):
        await self.send(text_data=json.dumps({
            'type': 'cronometro_iniciado',
            'data': event['data']
        }))
    
    async def nacimiento(self, event):
        await self.send(text_data=json.dumps({
            'type': 'nacimiento',
            'data': event['data']
        }))
    
    async def proceso_cerrado(self, event):
        await self.send(text_data=json.dumps({
            'type': 'proceso_cerrado',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_estado_proceso(self):
        from .models import ProcesoParto
        proceso = ProcesoParto.objects.get(codigo=self.proceso_codigo)
        return {
            'codigo': proceso.codigo,
            'estado': proceso.estado.codigo,
            'cronometro_inicio': proceso.hora_cronometro_inicio.isoformat() if proceso.hora_cronometro_inicio else None,
            'confirmaciones': list(proceso.confirmaciones.values(
                'profesional__username', 'rol__nombre', 'confirmado', 'tiempo_respuesta_segundos'
            ))
        }
```

---

## 9. Validadores

```python
# gestionProcesosApp/validators.py

from django.core.exceptions import ValidationError


class ValidadorProceso:
    """Validaciones de negocio para procesos de parto"""
    
    @staticmethod
    def validar_puede_iniciar(ficha_obstetrica):
        """Valida si se puede iniciar un proceso"""
        errores = []
        
        if ficha_obstetrica.dilatacion_actual < 8:
            errores.append(
                f"Dilatación insuficiente: {ficha_obstetrica.dilatacion_actual}cm "
                f"(se requiere >= 8cm)"
            )
        
        if ficha_obstetrica.estado != 'ACTIVA':
            errores.append("La ficha obstétrica no está activa")
        
        if hasattr(ficha_obstetrica, 'proceso_parto'):
            errores.append("Ya existe un proceso para esta ficha")
        
        if errores:
            raise ValidationError(errores)
        
        return True
    
    @staticmethod
    def validar_puede_iniciar_cronometro(proceso, usuario):
        """Valida si el médico puede iniciar el cronómetro"""
        errores = []
        
        if not usuario.groups.filter(name='medico').exists():
            errores.append("Solo médicos pueden iniciar el cronómetro")
        
        if proceso.hora_cronometro_inicio is not None:
            errores.append("El cronómetro ya fue iniciado")
        
        if proceso.estado.codigo != 'CONFIRMADO':
            errores.append("El equipo debe estar confirmado primero")
        
        if errores:
            raise ValidationError(errores)
        
        return True
    
    @staticmethod
    def validar_puede_finalizar(proceso, usuario):
        """Valida si se puede finalizar el proceso"""
        errores = []
        
        if not usuario.groups.filter(name='medico').exists():
            errores.append("Solo médicos pueden finalizar el proceso")
        
        if proceso.hora_cronometro_inicio is None:
            errores.append("El cronómetro no ha sido iniciado")
        
        bebes_registrados = proceso.recien_nacidos.count()
        bebes_esperados = proceso.num_bebes
        
        if bebes_registrados < bebes_esperados:
            errores.append(
                f"Faltan registrar {bebes_esperados - bebes_registrados} bebé(s)"
            )
        
        # Verificar datos completos de cada bebé
        for rn in proceso.recien_nacidos.all():
            if not rn.tiene_datos_completos():
                errores.append(f"Bebé {rn.codigo} tiene datos incompletos")
        
        if errores:
            raise ValidationError(errores)
        
        return True
    
    @staticmethod
    def validar_sala_disponible(sala, proceso):
        """Valida si una sala puede ser asignada"""
        errores = []
        
        if sala.estado.codigo != 'DISPONIBLE':
            errores.append(f"La sala {sala.nombre} no está disponible")
        
        if proceso.tipo_parto.requiere_quirofano and not sala.tiene_quirofano:
            errores.append(
                f"La sala {sala.nombre} no tiene quirófano "
                f"(requerido para {proceso.tipo_parto.nombre})"
            )
        
        if proceso.num_bebes > sala.capacidad_bebes:
            errores.append(
                f"La sala {sala.nombre} tiene capacidad para {sala.capacidad_bebes} bebé(s), "
                f"se requiere {proceso.num_bebes}"
            )
        
        if errores:
            raise ValidationError(errores)
        
        return True
```

---

## 10. Signals

```python
# gestionProcesosApp/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import (
    ProcesoParto, ConfirmacionPersonal, 
    EventoProceso, SalaParto
)


@receiver(post_save, sender=ConfirmacionPersonal)
def notificar_confirmacion(sender, instance, **kwargs):
    """Notifica vía WebSocket cuando alguien confirma"""
    
    if instance.confirmado:
        channel_layer = get_channel_layer()
        
        async_to_sync(channel_layer.group_send)(
            f'proceso_{instance.proceso.codigo}',
            {
                'type': 'confirmacion_recibida',
                'data': {
                    'profesional': instance.profesional.get_full_name(),
                    'rol': instance.rol.nombre,
                    'tiempo_respuesta': instance.tiempo_respuesta_segundos,
                    'dentro_tiempo': instance.dentro_tiempo
                }
            }
        )
        
        # Registrar evento
        EventoProceso.objects.create(
            proceso=instance.proceso,
            evento='CONFIRMACION_RECIBIDA',
            usuario=instance.profesional,
            detalle={
                'tiempo_respuesta': instance.tiempo_respuesta_segundos,
                'dentro_tiempo': instance.dentro_tiempo
            }
        )


@receiver(pre_save, sender=ProcesoParto)
def detectar_cambio_estado(sender, instance, **kwargs):
    """Detecta cambios de estado para notificar"""
    
    if instance.pk:
        try:
            anterior = ProcesoParto.objects.get(pk=instance.pk)
            instance._estado_anterior = anterior.estado
        except ProcesoParto.DoesNotExist:
            instance._estado_anterior = None
    else:
        instance._estado_anterior = None


@receiver(post_save, sender=ProcesoParto)
def notificar_cambio_estado(sender, instance, created, **kwargs):
    """Notifica cambios de estado vía WebSocket"""
    
    if not created and hasattr(instance, '_estado_anterior'):
        if instance._estado_anterior != instance.estado:
            channel_layer = get_channel_layer()
            
            # Notificar nuevo estado
            if instance.estado.codigo == 'EN_CURSO':
                async_to_sync(channel_layer.group_send)(
                    f'proceso_{instance.codigo}',
                    {
                        'type': 'cronometro_iniciado',
                        'data': {
                            'hora_inicio': instance.hora_cronometro_inicio.isoformat()
                        }
                    }
                )
            
            elif instance.estado.codigo in ['CERRADO', 'CERRADO_DERIVACION']:
                async_to_sync(channel_layer.group_send)(
                    f'proceso_{instance.codigo}',
                    {
                        'type': 'proceso_cerrado',
                        'data': {
                            'estado': instance.estado.codigo,
                            'duracion': instance.duracion_cronometro,
                            'hora_fin': instance.hora_cronometro_fin.isoformat() if instance.hora_cronometro_fin else None
                        }
                    }
                )


@receiver(post_save, sender=SalaParto)
def notificar_cambio_sala(sender, instance, **kwargs):
    """Notifica cambios en estado de salas"""
    
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        'salas_estado',
        {
            'type': 'sala_actualizada',
            'data': {
                'sala': instance.nombre,
                'estado': instance.estado.codigo,
                'proceso': instance.proceso_actual.codigo if instance.proceso_actual else None
            }
        }
    )
```

---

## 11. Templates

### 11.1 Estructura de Templates

```
gestionProcesosApp/
└── templates/
    └── gestionProcesosApp/
        ├── base_procesos.html
        ├── dashboard.html
        ├── iniciar_proceso.html
        ├── detalle_proceso.html
        ├── confirmar_asistencia.html
        ├── finalizar_proceso.html
        ├── estado_salas.html
        ├── emergencia/
        │   ├── crear_ficha.html
        │   └── completar.html
        ├── partials/
        │   ├── _cronometro.html
        │   ├── _confirmaciones.html
        │   ├── _timeline_eventos.html
        │   └── _sala_card.html
        └── notificaciones/
            ├── lista.html
            └── _notificacion_item.html
```

### 11.2 Template del Cronómetro

```html
<!-- templates/gestionProcesosApp/partials/_cronometro.html -->

<div id="cronometro-container" class="card {% if proceso.estado.codigo == 'EN_CURSO' %}border-primary{% endif %}">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">
            <i class="bi bi-stopwatch me-2"></i>
            Cronómetro Oficial
        </h5>
        <span class="badge bg-{{ proceso.estado.color|default:'secondary' }}">
            {{ proceso.estado.nombre }}
        </span>
    </div>
    
    <div class="card-body text-center">
        {% if proceso.hora_cronometro_inicio %}
            <!-- Cronómetro activo o finalizado -->
            <div id="cronometro-display" class="display-1 font-monospace mb-3"
                 data-inicio="{{ proceso.hora_cronometro_inicio|date:'c' }}"
                 data-fin="{{ proceso.hora_cronometro_fin|date:'c'|default:'' }}">
                00:00:00
            </div>
            
            <p class="text-muted">
                Iniciado: {{ proceso.hora_cronometro_inicio|date:"H:i:s" }}
                {% if proceso.hora_cronometro_fin %}
                    <br>Finalizado: {{ proceso.hora_cronometro_fin|date:"H:i:s" }}
                    <br><strong>Duración: {{ proceso.duracion_cronometro }} minutos</strong>
                {% endif %}
            </p>
            
        {% else %}
            <!-- Esperando inicio -->
            <div class="display-1 font-monospace text-muted mb-3">
                --:--:--
            </div>
            
            <p class="text-muted">
                Esperando que el médico inicie el cronómetro
            </p>
            
            {% if user.groups.all|join:"," == "medico" %}
                <form method="post" action="{% url 'procesos:iniciar_cronometro' proceso.codigo %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-primary btn-lg">
                        <i class="bi bi-play-fill me-2"></i>
                        Iniciar Cronómetro
                    </button>
                </form>
            {% endif %}
        {% endif %}
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const display = document.getElementById('cronometro-display');
    if (!display) return;
    
    const inicio = display.dataset.inicio;
    const fin = display.dataset.fin;
    
    if (!inicio) return;
    
    const fechaInicio = new Date(inicio);
    const fechaFin = fin ? new Date(fin) : null;
    
    function actualizarCronometro() {
        const ahora = fechaFin || new Date();
        const diff = ahora - fechaInicio;
        
        const horas = Math.floor(diff / 3600000);
        const minutos = Math.floor((diff % 3600000) / 60000);
        const segundos = Math.floor((diff % 60000) / 1000);
        
        display.textContent = 
            String(horas).padStart(2, '0') + ':' +
            String(minutos).padStart(2, '0') + ':' +
            String(segundos).padStart(2, '0');
    }
    
    actualizarCronometro();
    
    if (!fechaFin) {
        setInterval(actualizarCronometro, 1000);
    }
});
</script>
```

---

## 12. Diagrama de Flujo

```
                                    ┌─────────────────────────────┐
                                    │                             │
                                    │   PACIENTE ALCANZA 8cm      │
                                    │                             │
                                    └──────────────┬──────────────┘
                                                   │
                                                   ▼
                              ┌─────────────────────────────────────────┐
                              │         MATRONA / COORDINADOR           │
                              │     Presiona "Iniciar Proceso"          │
                              └──────────────────┬──────────────────────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    │                            │                            │
                    ▼                            ▼                            ▼
           ┌────────────────┐          ┌────────────────┐          ┌────────────────┐
           │ Calcular       │          │ Asignar Sala   │          │ Generar        │
           │ Personal       │          │ Disponible     │          │ Código MT-XXXX │
           │ Requerido      │          │                │          │                │
           └────────┬───────┘          └────────┬───────┘          └────────┬───────┘
                    │                           │                           │
                    └───────────────────────────┴───────────────────────────┘
                                                │
                                                ▼
                              ┌─────────────────────────────────────────┐
                              │       ENVIAR NOTIFICACIONES PUSH        │
                              │         (timeout: 60 segundos)          │
                              └──────────────────┬──────────────────────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    │                            │                            │
                    ▼                            ▼                            ▼
           ┌────────────────┐          ┌────────────────┐          ┌────────────────┐
           │ TENS           │          │ MATRONA        │          │ MÉDICO         │
           │ Confirma       │          │ Confirma       │          │ Confirma       │
           └────────┬───────┘          └────────┬───────┘          └────────┬───────┘
                    │                           │                           │
                    └───────────────────────────┴───────────────────────────┘
                                                │
                                                ▼
                              ┌─────────────────────────────────────────┐
                              │         LLEGADA SECUENCIAL A SALA       │
                              │  1° TENS → 2° Matrona → 3° Médico       │
                              └──────────────────┬──────────────────────┘
                                                 │
                                                 ▼
                              ┌─────────────────────────────────────────┐
                              │      MÉDICO INGRESA E INICIA            │
                              │      CRONÓMETRO OFICIAL                 │
                              │      (momento único)                    │
                              └──────────────────┬──────────────────────┘
                                                 │
                                                 ▼
                              ┌─────────────────────────────────────────┐
                              │              PARTO                      │
                              │                                         │
                              └──────────────────┬──────────────────────┘
                                                 │
                                                 ▼
                              ┌─────────────────────────────────────────┐
                              │          BEBÉ NACE                      │
                              │     Generar código RN-XXXX              │
                              └──────────────────┬──────────────────────┘
                                                 │
                                                 ▼
                              ┌─────────────────────────────────────────┐
                              │       APEGO PIEL A PIEL                 │
                              │         (5 minutos)                     │
                              └──────────────────┬──────────────────────┘
                                                 │
                                                 ▼
                              ┌─────────────────────────────────────────┐
                              │     TRASLADO A SALA DE REGISTRO         │
                              │   Peso, Talla, Vit K, BCG, Huellas      │
                              └──────────────────┬──────────────────────┘
                                                 │
                                                 ▼
                              ┌─────────────────────────────────────────┐
                              │      MÉDICO FINALIZA PROCESO            │
                              │   - Cerrar fichas                       │
                              │   - Liberar sala                        │
                              │   - Calcular duración                   │
                              └─────────────────────────────────────────┘
```

---

## 13. Permisos

| Acción | Médico | Matrona | TENS | Coordinador | Admin |
|--------|:------:|:-------:|:----:|:-----------:|:-----:|
| Ver dashboard procesos | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver detalle proceso | ✅ | ✅ | ✅ | ✅ | ✅ |
| Iniciar proceso | ❌ | ✅ | ❌ | ✅ | ✅ |
| Confirmar asistencia | ✅ | ✅ | ✅ | ❌ | ❌ |
| Iniciar cronómetro | ✅ | ❌ | ❌ | ❌ | ❌ |
| Finalizar proceso | ✅ | ❌ | ❌ | ❌ | ✅ |
| Derivar a UCI | ✅ | ❌ | ❌ | ❌ | ❌ |
| Crear ficha emergencia | ❌ | ❌ | ❌ | ✅ | ✅ |
| Ver estado salas | ✅ | ✅ | ✅ | ✅ | ✅ |
| Liberar sala manual | ❌ | ❌ | ❌ | ✅ | ✅ |
| Ver historial | ✅ | ✅ | ❌ | ✅ | ✅ |

---

## 14. Tests

### 14.1 Casos de Prueba

| ID | Caso de Prueba | Entrada | Resultado Esperado |
|----|----------------|---------|-------------------|
| CP-001 | Iniciar proceso con dilatación >= 8cm | Ficha con 8cm | Proceso creado, sala asignada |
| CP-002 | Iniciar proceso con dilatación < 8cm | Ficha con 5cm | Error de validación |
| CP-003 | Calcular personal para 1 bebé | num_bebes=1 | 1 médico, 1 matrona, 3 TENS |
| CP-004 | Calcular personal para 2 bebés | num_bebes=2 | 2 médicos, 2 matronas, 4 TENS |
| CP-005 | Confirmación dentro de tiempo | < 60 segundos | dentro_tiempo=True |
| CP-006 | Confirmación fuera de tiempo | > 60 segundos | dentro_tiempo=False |
| CP-007 | Médico inicia cronómetro | Usuario con rol médico | Cronómetro iniciado |
| CP-008 | Matrona intenta iniciar cronómetro | Usuario con rol matrona | Error de permisos |
| CP-009 | Finalizar sin todos los bebés | 2 esperados, 1 registrado | Error de validación |
| CP-010 | Derivación a UCI | Médico deriva | Estado CERRADO_DERIVACION |

### 14.2 Comandos de Test

```bash
# Ejecutar tests de la app
pytest gestionProcesosApp/tests/ -v

# Tests específicos
pytest gestionProcesosApp/tests/test_services.py -v
pytest gestionProcesosApp/tests/test_validaciones.py -v
pytest gestionProcesosApp/tests/test_views.py -v

# Coverage
pytest gestionProcesosApp/tests/ --cov=gestionProcesosApp --cov-report=html
```

---

## 15. Notas Importantes

### 15.1 Reglas de Negocio Críticas

1. **Inicio a 8cm**: El proceso se inicia cuando la paciente alcanza 8cm de dilatación para optimizar el uso de salas.

2. **Timeout de 60 segundos**: El personal tiene máximo 60 segundos para confirmar después de recibir la notificación.

3. **Cronómetro único**: Solo el médico puede iniciar el cronómetro oficial, y es un momento único que no puede repetirse.

4. **Fórmula de personal**: Por cada bebé se asigna 1 médico + 1 matrona + 1 TENS, más 2 TENS de apoyo fijos.

5. **Apego de 5 minutos**: El bebé permanece en contacto piel a piel con la madre durante 5 minutos antes del traslado a registro.

### 15.2 Integraciones

- **Firebase Cloud Messaging**: Para notificaciones push
- **Django Channels**: Para WebSocket y actualizaciones en tiempo real
- **Celery**: Para tareas asíncronas (timeout de confirmaciones, alertas)

### 15.3 Consideraciones de Rendimiento

- Índices en campos frecuentemente consultados (codigo, estado, sala)
- Cache de salas disponibles
- WebSocket para evitar polling

### 15.4 Extensibilidad

El sistema está diseñado para soportar:
- Nuevos tipos de proceso
- Roles adicionales
- Integración con control de acceso físico
- Métricas y dashboards

---

## 📊 Diagrama de Relaciones

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            gestionProcesosApp                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐      1:1       ┌─────────────────┐                │
│  │ FichaObstetrica │◄──────────────►│  ProcesoParto   │                │
│  │  (matronaApp)   │                │                 │                │
│  └─────────────────┘                └────────┬────────┘                │
│                                              │                          │
│                          ┌───────────────────┼───────────────────┐     │
│                          │                   │                   │     │
│                          ▼                   ▼                   ▼     │
│                 ┌─────────────────┐ ┌─────────────────┐ ┌─────────────┐│
│                 │ Confirmacion    │ │ Asignacion      │ │ Evento      ││
│                 │ Personal        │ │ Personal        │ │ Proceso     ││
│                 └────────┬────────┘ └────────┬────────┘ └─────────────┘│
│                          │                   │                          │
│                          ▼                   ▼                          │
│                 ┌─────────────────┐ ┌─────────────────┐                │
│                 │ User            │ │ CatalogoRol     │                │
│                 │ (auth)          │ │ Proceso         │                │
│                 └─────────────────┘ └─────────────────┘                │
│                                                                         │
│  ┌─────────────────┐      N:1       ┌─────────────────┐                │
│  │  ProcesoParto   │───────────────►│   SalaParto     │                │
│  └─────────────────┘                └─────────────────┘                │
│                                                                         │
│  ┌─────────────────┐      1:N       ┌─────────────────┐                │
│  │  ProcesoParto   │◄──────────────►│ RegistroRN      │                │
│  └─────────────────┘                │ (recienNacidoApp)                │
│                                     └─────────────────┘                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

*Documentación gestionProcesosApp - OB_CARE v1.0*
