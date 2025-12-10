# gestionApp/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from utilidad.rut_validator import validar_rut, normalizar_rut, validar_rut_chileno
from datetime import date
from django.utils import timezone


# ============================================
# TABLAS CATÁLOGO (reemplazan los CHOICES)
# ============================================

class CatalogoSexo(models.Model):
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
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Turno"
        verbose_name_plural = "Catálogo Turnos"
        ordering = ['orden', 'nombre']


class CatalogoEspecialidad(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Especialidad"
        verbose_name_plural = "Catálogo Especialidades"
        ordering = ['orden', 'nombre']


class CatalogoNivelTens(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Nivel TENS"
        verbose_name_plural = "Catálogo Niveles TENS"
        ordering = ['orden', 'nombre']


class CatalogoCertificacion(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Catálogo Certificación"
        verbose_name_plural = "Catálogo Certificaciones"
        ordering = ['orden', 'nombre']


# ============================================
# MODELO BASE: PERSONA
# ============================================
class Persona(models.Model):
    # Campos principales
    Rut = models.CharField(max_length=100, unique=True, validators=[validar_rut_chileno], verbose_name="RUT")
    Nombre = models.CharField(max_length=100, verbose_name="Nombre")
    Apellido_Paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    Apellido_Materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    Fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    
    # FK a catálogos (reemplazan CHOICES)
    Sexo = models.ForeignKey(CatalogoSexo, on_delete=models.PROTECT, verbose_name="Sexo")
    Nacionalidad = models.ForeignKey(CatalogoNacionalidad, on_delete=models.PROTECT, verbose_name="Nacionalidad", null=True, blank=True)
    Pueblos_originarios = models.ForeignKey(CatalogoPuebloOriginario, on_delete=models.PROTECT, verbose_name="Pueblos originarios", null=True, blank=True)
    
    # Campos booleanos (Si/No se quedan como Boolean, no necesitan catálogo)
    Inmigrante = models.BooleanField(default=False, verbose_name="Inmigrante")
    Discapacidad = models.BooleanField(default=False, verbose_name="Discapacidad")
    Tipo_de_Discapacidad = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tipo de Discapacidad")
    Privada_de_Libertad = models.BooleanField(default=False, verbose_name="Privada de Libertad")
    Trans_Masculino = models.BooleanField(default=False, verbose_name="Trans Masculino")
    
    # Contacto
    Telefono = models.CharField(max_length=100, verbose_name="Telefono", blank=True)
    Direccion = models.CharField(max_length=100, verbose_name="Direccion", blank=True)
    Email = models.CharField(max_length=100, verbose_name="Email", blank=True)
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    
    # ============================================
    # @PROPERTY - ALIAS EN MINÚSCULAS
    # ============================================
    @property
    def rut(self):
        return self.Rut
    
    @property
    def nombre(self):
        return self.Nombre
    
    @property
    def apellido_paterno(self):
        return self.Apellido_Paterno
    
    @property
    def apellido_materno(self):
        return self.Apellido_Materno
    
    @property
    def fecha_nacimiento(self):
        return self.Fecha_nacimiento
    
    @property
    def sexo(self):
        return self.Sexo.nombre if self.Sexo else None
    
    @property
    def nacionalidad(self):
        return self.Nacionalidad.nombre if self.Nacionalidad else None
    
    @property
    def telefono(self):
        return self.Telefono
    
    @property
    def direccion(self):
        return self.Direccion
    
    @property
    def email(self):
        return self.Email
    
    @property
    def activo(self):
        return self.Activo
    
    @property
    def nombre_completo(self):
        return f"{self.Nombre} {self.Apellido_Paterno} {self.Apellido_Materno}"
    
    @property
    def edad(self):
        if not self.Fecha_nacimiento:
            return None
        hoy = date.today()
        return hoy.year - self.Fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.Fecha_nacimiento.month, self.Fecha_nacimiento.day))
    
    def clean(self):
        super().clean()
        if self.Discapacidad:
            if not self.Tipo_de_Discapacidad or self.Tipo_de_Discapacidad.strip() == '':
                raise ValidationError({'Tipo_de_Discapacidad': 'Debe especificar el tipo de discapacidad'})
        if not self.Discapacidad:
            self.Tipo_de_Discapacidad = None
        if self.Fecha_nacimiento and self.edad and self.edad < 0:
            raise ValidationError({'Fecha_nacimiento': 'La fecha de nacimiento no puede ser futura.'})
    
    def __str__(self):
        return f"{self.Nombre} {self.Apellido_Paterno} {self.Apellido_Materno} - {self.Rut}"
    
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['-id']


# ============================================
# MODELO: PACIENTE
# ============================================
class Paciente(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, primary_key=True, verbose_name="Persona")
    
    # FK a catálogos
    Estado_civil = models.ForeignKey(CatalogoEstadoCivil, on_delete=models.PROTECT, verbose_name="Estado Civil", null=True, blank=True)
    Previcion = models.ForeignKey(CatalogoPrevision, on_delete=models.PROTECT, verbose_name="Previsión", null=True, blank=True)
    
    # Campos clínicos
    paridad = models.CharField(max_length=50, blank=True, verbose_name="Paridad")
    Ductus_Venosus = models.CharField(max_length=70, blank=True, verbose_name="Ductus Venosus")
    control_prenatal = models.BooleanField(default=False, verbose_name="Control Prenatal")
    Consultorio = models.CharField(max_length=100, blank=True, verbose_name="Consultorio")
    Preeclampsia_Severa = models.BooleanField(default=False, verbose_name="Preeclampsia Severa")
    Eclampsia = models.BooleanField(default=False, verbose_name="Eclampsia")
    Sepsis_o_Infeccion_SiST = models.BooleanField(default=False, verbose_name="Sepsis o Infección Sistémica")
    Infeccion_Ovular_o_Corioamnionitis = models.BooleanField(default=False, verbose_name="Infección Ovular")
    Acompañante = models.CharField(max_length=120, blank=True, verbose_name="Acompañante")
    Contacto_emergencia = models.CharField(max_length=30, blank=True, verbose_name="Contacto Emergencia")
    Fecha_y_Hora_Ingreso = models.DateTimeField(default=timezone.now, verbose_name="Fecha y Hora de Ingreso")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    # ============================================
    # @PROPERTY - ALIAS EN MINÚSCULAS
    # ============================================
    @property
    def estado_civil(self):
        return self.Estado_civil.nombre if self.Estado_civil else None
    
    @property
    def prevision(self):
        return self.Previcion.nombre if self.Previcion else None
    
    @property
    def consultorio(self):
        return self.Consultorio
    
    @property
    def contacto_emergencia(self):
        return self.Contacto_emergencia
    
    def __str__(self):
        return f"Paciente: {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno}"
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"


# ============================================
# MODELO: MEDICO
# ============================================
class Medico(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Especialidad = models.ForeignKey(CatalogoEspecialidad, on_delete=models.PROTECT, verbose_name="Especialidad")
    Registro_medico = models.CharField(max_length=100, unique=True, verbose_name="Registro Médico")
    Años_experiencia = models.IntegerField(verbose_name="Años de Experiencia")
    Turno = models.ForeignKey(CatalogoTurno, on_delete=models.PROTECT, verbose_name="Turno")
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    
    # @property
    @property
    def especialidad(self):
        return self.Especialidad.nombre if self.Especialidad else None
    
    @property
    def turno(self):
        return self.Turno.nombre if self.Turno else None
    
    @property
    def registro_medico(self):
        return self.Registro_medico
    
    @property
    def años_experiencia(self):
        return self.Años_experiencia
    
    def __str__(self):
        return f"Dr(a). {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno}"
    
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"


# ============================================
# MODELO: MATRONA
# ============================================
class Matrona(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Especialidad = models.ForeignKey(CatalogoEspecialidad, on_delete=models.PROTECT, verbose_name="Especialidad")
    Registro_medico = models.CharField(max_length=100, unique=True, verbose_name="Registro Médico")
    Años_experiencia = models.IntegerField(verbose_name="Años de Experiencia")
    Turno = models.ForeignKey(CatalogoTurno, on_delete=models.PROTECT, verbose_name="Turno")
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    
    # @property
    @property
    def especialidad(self):
        return self.Especialidad.nombre if self.Especialidad else None
    
    @property
    def turno(self):
        return self.Turno.nombre if self.Turno else None
    
    @property
    def registro_medico(self):
        return self.Registro_medico
    
    def __str__(self):
        return f"Matrona: {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno}"
    
    class Meta:
        verbose_name = "Matrona"
        verbose_name_plural = "Matronas"


# ============================================
# MODELO: TENS
# ============================================
class Tens(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Nivel = models.ForeignKey(CatalogoNivelTens, on_delete=models.PROTECT, verbose_name="Nivel")
    Años_experiencia = models.IntegerField(verbose_name="Años de Experiencia")
    Turno = models.ForeignKey(CatalogoTurno, on_delete=models.PROTECT, verbose_name="Turno")
    Certificaciones = models.ForeignKey(CatalogoCertificacion, on_delete=models.PROTECT, verbose_name="Certificaciones")
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    
    # @property
    @property
    def nivel(self):
        return self.Nivel.nombre if self.Nivel else None
    
    @property
    def turno(self):
        return self.Turno.nombre if self.Turno else None
    
    @property
    def certificaciones(self):
        return self.Certificaciones.nombre if self.Certificaciones else None
    
    def __str__(self):
        return f"TENS: {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno}"
    
    class Meta:
        verbose_name = "TENS"
        verbose_name_plural = "TENS"