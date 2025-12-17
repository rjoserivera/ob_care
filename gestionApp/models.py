"""
gestionApp/models.py
Modelos simplificados para gestión de personas y pacientes
Los roles (Médico, Matrona, TENS) se manejan desde Django Admin con Groups y Permissions

ACTUALIZADO: Solo Persona y Paciente + Catálogos
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


# ============================================
# VALIDADOR DE RUT CHILENO
# ============================================

def validar_rut_chileno(value):
    """
    Valida el formato y dígito verificador del RUT chileno
    Acepta formatos: 12345678-9, 12.345.678-9, 123456789
    """
    # Limpiar el RUT
    rut = value.replace(".", "").replace("-", "").replace(" ", "").upper()
    
    if len(rut) < 2:
        raise ValidationError("RUT inválido: muy corto")
    
    # Separar cuerpo y dígito verificador
    cuerpo = rut[:-1]
    dv = rut[-1]
    
    # Validar que el cuerpo sean solo números
    if not cuerpo.isdigit():
        raise ValidationError("RUT inválido: el cuerpo debe contener solo números")
    
    # Calcular dígito verificador
    suma = 0
    multiplo = 2
    
    for digit in reversed(cuerpo):
        suma += int(digit) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2
    
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_esperado = "0"
    elif dv_calculado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_calculado)
    
    if dv != dv_esperado:
        raise ValidationError(f"RUT inválido: dígito verificador incorrecto (esperado: {dv_esperado})")
    
    return True


def normalizar_rut(rut):
    """Normaliza el RUT al formato 12345678-9"""
    rut_limpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    if len(rut_limpio) < 2:
        return rut
    return f"{rut_limpio[:-1]}-{rut_limpio[-1]}"


# ============================================
# CATÁLOGOS BASE
# ============================================

class CatalogoSexo(models.Model):
    """Catálogo de sexos"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Sexo"
        verbose_name_plural = "Catálogo Sexos"
        ordering = ['orden', 'nombre']


class CatalogoNacionalidad(models.Model):
    """Catálogo de nacionalidades"""
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Nacionalidad"
        verbose_name_plural = "Catálogo Nacionalidades"
        ordering = ['orden', 'nombre']


class CatalogoPuebloOriginario(models.Model):
    """Catálogo de pueblos originarios de Chile"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Pueblo Originario"
        verbose_name_plural = "Catálogo Pueblos Originarios"
        ordering = ['orden', 'nombre']


class CatalogoEstadoCivil(models.Model):
    """Catálogo de estados civiles"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Estado Civil"
        verbose_name_plural = "Catálogo Estados Civiles"
        ordering = ['orden', 'nombre']


class CatalogoPrevision(models.Model):
    """Catálogo de previsiones de salud"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Previsión"
        verbose_name_plural = "Catálogo Previsiones"
        ordering = ['orden', 'nombre']


class CatalogoTurno(models.Model):
    """Catálogo de turnos hospitalarios"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Turno"
        verbose_name_plural = "Catálogo Turnos"
        ordering = ['orden', 'nombre']


# ============================================
# MODELO PRINCIPAL: PERSONA
# ============================================

class Persona(models.Model):
    """
    Modelo base para todas las personas del sistema.
    Incluye pacientes y personal de salud.
    """
    
    # ========== IDENTIFICACIÓN ==========
    Rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[validar_rut_chileno],
        verbose_name="RUT",
        help_text="Formato: 12345678-9"
    )
    Nombre = models.CharField(max_length=100, verbose_name="Nombre")
    Apellido_Paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    Apellido_Materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    Fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    
    # ========== DATOS DEMOGRÁFICOS (FK a Catálogos) ==========
    Sexo = models.ForeignKey(
        CatalogoSexo,
        on_delete=models.PROTECT,
        verbose_name="Sexo"
    )
    Nacionalidad = models.ForeignKey(
        CatalogoNacionalidad,
        on_delete=models.PROTECT,
        verbose_name="Nacionalidad",
        null=True,
        blank=True
    )
    Pueblos_originarios = models.ForeignKey(
        CatalogoPuebloOriginario,
        on_delete=models.PROTECT,
        verbose_name="Pueblo Originario",
        null=True,
        blank=True
    )
    Estado_civil = models.ForeignKey(
        CatalogoEstadoCivil,
        on_delete=models.PROTECT,
        verbose_name="Estado Civil",
        null=True,
        blank=True
    )
    
    # ========== CONDICIONES ESPECIALES ==========
    Inmigrante = models.BooleanField(
        default=False,
        verbose_name="¿Es Inmigrante?"
    )

    Privada_de_Libertad = models.BooleanField(
        default=False,
        verbose_name="¿Privada de Libertad?"
    )
    Trans_Masculino = models.BooleanField(
        default=False,
        verbose_name="¿Trans Masculino?"
    )
    
    # ========== CONTACTO ==========
    Telefono = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
        blank=True
    )
    Telefono_emergencia = models.CharField(
        max_length=20,
        verbose_name="Teléfono de Emergencia",
        blank=True
    )
    Direccion = models.CharField(
        max_length=200,
        verbose_name="Dirección",
        blank=True
    )
    Comuna = models.CharField(
        max_length=100,
        verbose_name="Comuna",
        blank=True
    )
    Email = models.EmailField(
        verbose_name="Email",
        blank=True,
        null=True
    )
    
    # ========== ESTADO Y AUDITORÍA ==========
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # ========== RELACIÓN OPCIONAL CON USER ==========
    usuario = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='persona',
        verbose_name="Usuario del Sistema",
        help_text="Solo para personal de salud que necesita acceso al sistema"
    )
    
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['Apellido_Paterno', 'Apellido_Materno', 'Nombre']
        indexes = [
            models.Index(fields=['Rut']),
            models.Index(fields=['Apellido_Paterno', 'Apellido_Materno']),
        ]
    
    def __str__(self):
        return f"{self.Apellido_Paterno} {self.Apellido_Materno}, {self.Nombre}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo"""
        return f"{self.Nombre} {self.Apellido_Paterno} {self.Apellido_Materno}"
    
    @property
    def edad(self):
        """Calcula la edad actual"""
        if not self.Fecha_nacimiento:
            return None
        hoy = date.today()
        return hoy.year - self.Fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.Fecha_nacimiento.month, self.Fecha_nacimiento.day)
        )
    
    @property
    def rut_formateado(self):
        """Retorna el RUT formateado con puntos y guión"""
        rut = self.Rut.replace(".", "").replace("-", "")
        if len(rut) < 2:
            return self.Rut
        cuerpo = rut[:-1]
        dv = rut[-1]
        # Formatear con puntos
        cuerpo_formateado = ""
        for i, digit in enumerate(reversed(cuerpo)):
            if i > 0 and i % 3 == 0:
                cuerpo_formateado = "." + cuerpo_formateado
            cuerpo_formateado = digit + cuerpo_formateado
        return f"{cuerpo_formateado}-{dv}"
    
    def clean(self):
        """Validaciones del modelo"""
        super().clean()
        # Normalizar RUT
        if self.Rut:
            self.Rut = normalizar_rut(self.Rut)
    
    def save(self, *args, **kwargs):
        # Normalizar RUT antes de guardar
        if self.Rut:
            self.Rut = normalizar_rut(self.Rut)
        super().save(*args, **kwargs)


# ============================================
# MODELO: PACIENTE
# ============================================

class Paciente(models.Model):
    """
    Modelo para pacientes obstétricas.
    Extiende Persona con datos específicos de atención médica.
    """
    
    # ========== RELACIÓN CON PERSONA ==========
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='paciente',
        verbose_name="Persona"
    )
    
    # ========== PREVISIÓN DE SALUD ==========
    prevision = models.ForeignKey(
        CatalogoPrevision,
        on_delete=models.PROTECT,
        verbose_name="Previsión de Salud",
        null=True,
        blank=True
    )
    
    # ========== NÚMERO DE FICHA ==========
    numero_ficha_hospital = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="N° Ficha Hospital",
        help_text="Número de ficha del hospital (si existe)"
    )
    
    # ========== GRUPO SANGUÍNEO ==========
    GRUPO_SANGUINEO_CHOICES = [
        ('A+', 'A Positivo'),
        ('A-', 'A Negativo'),
        ('B+', 'B Positivo'),
        ('B-', 'B Negativo'),
        ('AB+', 'AB Positivo'),
        ('AB-', 'AB Negativo'),
        ('O+', 'O Positivo'),
        ('O-', 'O Negativo'),
        ('DESCONOCIDO', 'Desconocido'),
    ]
    grupo_sanguineo = models.CharField(
        max_length=15,
        choices=GRUPO_SANGUINEO_CHOICES,
        default='DESCONOCIDO',
        verbose_name="Grupo Sanguíneo"
    )
    
    # ========== ALERGIAS ==========
    tiene_alergias = models.BooleanField(
        default=False,
        verbose_name="¿Tiene Alergias?"
    )
    alergias = models.TextField(
        blank=True,
        null=True,
        verbose_name="Detalle de Alergias",
        help_text="Especificar alergias a medicamentos, alimentos, etc."
    )
    
    # ========== ANTECEDENTES ==========
    antecedentes_morbidos = models.TextField(
        blank=True,
        null=True,
        verbose_name="Antecedentes Mórbidos",
        help_text="Enfermedades crónicas, cirugías previas, etc."
    )
    
    medicamentos_uso_habitual = models.TextField(
        blank=True,
        null=True,
        verbose_name="Medicamentos de Uso Habitual"
    )
    
    # ========== ESTADO ==========
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # ========== OBSERVACIONES ==========
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['persona__Apellido_Paterno', 'persona__Apellido_Materno']
    
    def __str__(self):
        return f"{self.persona.nombre_completo} - {self.persona.Rut}"
    
    @property
    def nombre_completo(self):
        return self.persona.nombre_completo
    
    @property
    def rut(self):
        return self.persona.Rut
    
    @property
    def edad(self):
        return self.persona.edad


# ============================================
# MODELO: PERFIL DE USUARIO (PERSONAL DE SALUD)
# ============================================

class PerfilUsuario(models.Model):
    """
    Perfil extendido para usuarios del sistema (personal de salud).
    Los roles se manejan con Django Groups:
    - Grupo "Médicos"
    - Grupo "Matronas"
    - Grupo "TENS"
    - Grupo "Administradores"
    """
    
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name="Usuario"
    )
    
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='perfil_usuario',
        verbose_name="Datos Personales",
        null=True,
        blank=True
    )
    
    # ========== DATOS LABORALES ==========
    cargo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cargo"
    )
    
    turno_actual = models.ForeignKey(
        CatalogoTurno,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Turno Actual"
    )
    
    disponible = models.BooleanField(
        default=True,
        verbose_name="¿Disponible?"
    )
    
    # ========== TELÉFONO INSTITUCIONAL ==========
    telefono_institucional = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono Institucional"
    )
    
    # ========== TELEGRAM ==========
    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Telegram Chat ID",
        help_text="ID de chat de Telegram para notificaciones"
    )
    
    # ========== AUDITORÍA ==========
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
    
    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.cargo}"
    
    @property
    def es_medico(self):
        """Verifica si el usuario pertenece al grupo Médicos"""
        return self.usuario.groups.filter(name='Medicos').exists()
    
    @property
    def es_matrona(self):
        """Verifica si el usuario pertenece al grupo Matronas"""
        return self.usuario.groups.filter(name='Matronas').exists()
    
    @property
    def es_tens(self):
        """Verifica si el usuario pertenece al grupo TENS"""
        return self.usuario.groups.filter(name='TENS').exists()
    
    @property
    def es_admin(self):
        """Verifica si el usuario es administrador"""
        return self.usuario.is_superuser or self.usuario.groups.filter(name='Administradores').exists()
    
    @property
    def rol_principal(self):
        """Retorna el rol principal del usuario"""
        if self.es_admin:
            return "Administrador"
        elif self.es_medico:
            return "Médico"
        elif self.es_matrona:
            return "Matrona"
        elif self.es_tens:
            return "TENS"
        else:
            return "Sin rol asignado"


# ============================================
# MODELO: LOG DE SISTEMA
# ============================================

class LogSistema(models.Model):
    """
    Registro de auditoría de acciones del sistema.
    Cumple con el requerimiento de registrar:
    - Qué se hizo (Acción/Detalle)
    - Quién lo hizo (Usuario/Rol)
    - Cuándo (Fecha/Hora)
    - Desde dónde (IP)
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario"
    )
    
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    
    accion = models.CharField(max_length=255, verbose_name="Acción")
    
    detalle = models.TextField(blank=True, null=True, verbose_name="Detalle")
    
    modulo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Módulo")
    
    rol_usuario = models.CharField(max_length=50, blank=True, null=True, verbose_name="Rol al momento de la acción")
    
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")
    
    class Meta:
        verbose_name = "Log del Sistema"
        verbose_name_plural = "Logs del Sistema"
        ordering = ['-fecha_hora']
        
    def __str__(self):
        return f"{self.fecha_hora} - {self.usuario} - {self.accion}"