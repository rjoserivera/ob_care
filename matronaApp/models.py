"""
Modelos para la aplicación matronaApp
Gestión de fichas obstétricas, ingresos de pacientes y medicamentos
"""

from django.db import models
from gestionApp.models import Paciente, Matrona, Tens


class CatalogoViaAdministracion(models.Model):
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


class FichaObstetrica(models.Model):
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

    class Meta:
        app_label = 'matronaApp'

    def __str__(self):
        return self.numero_ficha


class MedicamentoFicha(models.Model):
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
    ficha = models.ForeignKey(FichaObstetrica, on_delete=models.CASCADE, related_name='administraciones')
    medicamento_ficha = models.ForeignKey(MedicamentoFicha, on_delete=models.SET_NULL, null=True, blank=True)
    tens = models.ForeignKey(Tens, on_delete=models.SET_NULL, null=True, blank=True)

    fecha_hora_administracion = models.DateTimeField()
    dosis_administrada = models.CharField(max_length=100)
    observaciones = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'matronaApp'
        ordering = ['-fecha_hora_administracion']

    def __str__(self):
        return f"Admin. {self.medicamento_ficha.nombre_medicamento} - {self.fecha_hora_administracion}"
