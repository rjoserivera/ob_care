"""
Modelos para la aplicación matronaApp
Gestión de fichas obstétricas, ingresos de pacientes y medicamentos
"""

from django.db import models
from gestionApp.models import Paciente, Matrona, TENS


class FichaObstetrica(models.Model):
    """Ficha clínica obstétrica de la paciente"""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    matrona_responsable = models.ForeignKey(Matrona, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Identificación
    numero_ficha = models.CharField(max_length=30, unique=True)
    nombre_acompanante = models.CharField(max_length=200, blank=True)
    
    # Historia obstétrica
    numero_gestas = models.PositiveIntegerField(default=0)
    numero_partos = models.PositiveIntegerField(default=0)
    partos_vaginales = models.PositiveIntegerField(default=0)
    partos_cesareas = models.PositiveIntegerField(default=0)
    numero_abortos = models.PositiveIntegerField(default=0)
    nacidos_vivos = models.PositiveIntegerField(default=0)
    
    # Embarazo actual
    fecha_ultima_regla = models.DateField(null=True, blank=True)
    fecha_probable_parto = models.DateField(null=True, blank=True)
    edad_gestacional_semanas = models.PositiveIntegerField(null=True, blank=True)
    edad_gestacional_dias = models.PositiveIntegerField(null=True, blank=True)
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    talla = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Exámenes y pruebas
    vih_tomado = models.BooleanField(default=False)
    vih_resultado = models.CharField(max_length=20, blank=True)
    vih_aro = models.CharField(max_length=50, blank=True)
    
    sgb_pesquisa = models.BooleanField(default=False)
    sgb_resultado = models.CharField(max_length=20, blank=True)
    sgb_antibiotico = models.CharField(max_length=100, blank=True)
    
    vdrl_resultado = models.CharField(max_length=20, blank=True)
    vdrl_tratamiento_atb = models.BooleanField(default=False)
    
    hepatitis_b_tomado = models.BooleanField(default=False)
    hepatitis_b_resultado = models.CharField(max_length=20, blank=True)
    hepatitis_b_derivacion = models.BooleanField(default=False)
    
    # Notas clínicas
    observaciones = models.TextField(blank=True)
    antecedentes_relevantes = models.TextField(blank=True)
    
    # Control
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'matronaApp'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Ficha {self.numero_ficha} - {self.paciente}"


class IngresoPaciente(models.Model):
    """Registro de ingreso de paciente a servicio"""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    
    numero_ficha = models.CharField(max_length=20, unique=True)
    motivo_ingreso = models.TextField()
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()
    
    edad_gestacional_semanas = models.IntegerField(null=True, blank=True)
    derivacion = models.CharField(max_length=200, blank=True)
    observaciones = models.TextField(blank=True)
    
    activo = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'matronaApp'
        ordering = ['-fecha_ingreso']
    
    def __str__(self):
        return f"Ingreso {self.numero_ficha} - {self.paciente}"


class MedicamentoFicha(models.Model):
    """Medicamentos prescritos en la ficha obstétrica"""
    ficha = models.ForeignKey(FichaObstetrica, on_delete=models.CASCADE, related_name='medicamentos')
    
    nombre_medicamento = models.CharField(max_length=200)
    dosis = models.CharField(max_length=100)
    via_administracion = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=50)
    
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    observaciones = models.TextField(blank=True)
    
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'matronaApp'
    
    def __str__(self):
        return f"{self.nombre_medicamento} - {self.ficha.numero_ficha}"


class AdministracionMedicamento(models.Model):
    """Registro de administración de medicamento a paciente"""
    ficha = models.ForeignKey(FichaObstetrica, on_delete=models.CASCADE, related_name='administraciones')
    medicamento_ficha = models.ForeignKey(MedicamentoFicha, on_delete=models.SET_NULL, null=True, blank=True)
    tens = models.ForeignKey(TENS, on_delete=models.SET_NULL, null=True, blank=True)
    
    fecha_hora_administracion = models.DateTimeField()
    dosis_administrada = models.CharField(max_length=100)
    observaciones = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'matronaApp'
        ordering = ['-fecha_hora_administracion']
    
    def __str__(self):
        return f"Admin. {self.medicamento_ficha.nombre_medicamento} - {self.fecha_hora_administracion}"
