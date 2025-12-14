# legacyApp/models.py
from django.db import models

class ControlesPrevios(models.Model):
    # Información General del Control
    paciente_rut = models.CharField(max_length=12)
    fecha_control = models.DateField()
    numero_control = models.IntegerField(null=True, blank=True)
    tipo_control = models.CharField(max_length=20, null=True, blank=True)
    consultorio_origen = models.CharField(max_length=100, null=True, blank=True)
    profesional_nombre = models.CharField(max_length=150, null=True, blank=True)
    profesional_tipo = models.CharField(max_length=20, null=True, blank=True)
    
    # Edad Gestacional
    semanas_gestacion = models.IntegerField(null=True, blank=True)
    dias_gestacion = models.IntegerField(null=True, blank=True)
    fur = models.DateField(null=True, blank=True)
    fpp = models.DateField(null=True, blank=True)
    
    # Antropometría
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    talla_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    imc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura_uterina_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ganancia_peso_total_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Signos Vitales Maternos
    presion_sistolica = models.IntegerField(null=True, blank=True)
    presion_diastolica = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca_materna = models.SmallIntegerField(null=True, blank=True)
    temperatura_c = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    saturacion_o2 = models.IntegerField(null=True, blank=True)
    
    # Evaluación Fetal
    fcf_lpm = models.IntegerField(null=True, blank=True)
    movimientos_fetales = models.CharField(max_length=20, null=True, blank=True)
    presentacion_fetal = models.CharField(max_length=20, null=True, blank=True)
    situacion_fetal = models.CharField(max_length=20, null=True, blank=True)
    
    # Exámenes de Laboratorio
    glucosa_mg_dl = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    hemoglobina_g_dl = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    hematocrito_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grupo_sanguineo = models.CharField(max_length=3, null=True, blank=True)
    factor_rh = models.CharField(max_length=10, null=True, blank=True)
    
    # Exámenes de Orina
    proteinuria = models.CharField(max_length=20, null=True, blank=True)
    leucocitos_orina = models.CharField(max_length=50, null=True, blank=True)
    
    # Exámenes Infecciosos - CRÍTICOS PARA PARTO
    vih_resultado = models.CharField(max_length=20, null=True, blank=True)
    vih_fecha_toma = models.DateField(null=True, blank=True)
    vih_orden = models.IntegerField(null=True, blank=True)
    vdrl_resultado = models.CharField(max_length=20, null=True, blank=True)
    vdrl_fecha = models.DateField(null=True, blank=True)
    sgb_resultado = models.CharField(max_length=20, null=True, blank=True)
    sgb_fecha_cultivo = models.DateField(null=True, blank=True)
    sgb_profilaxis = models.BooleanField(null=True, blank=True)
    toxoplasma_resultado = models.CharField(max_length=20, null=True, blank=True)
    toxoplasma_fecha = models.DateField(null=True, blank=True)
    hepatitis_b_resultado = models.CharField(max_length=20, null=True, blank=True)
    hepatitis_b_fecha = models.DateField(null=True, blank=True)
    
    # Patologías y Complicaciones - CRÍTICAS PARA PARTO
    diabetes_gestacional = models.BooleanField(null=True, blank=True)
    hipertension_arterial = models.BooleanField(null=True, blank=True)
    preeclampsia_leve = models.BooleanField(null=True, blank=True)
    preeclampsia_severa = models.BooleanField(null=True, blank=True)
    eclampsia = models.BooleanField(null=True, blank=True)
    anemia = models.BooleanField(null=True, blank=True)
    infeccion_urinaria = models.BooleanField(null=True, blank=True)
    corioamnionitis = models.BooleanField(null=True, blank=True)
    amenaza_parto_prematuro = models.BooleanField(null=True, blank=True)
    rotura_prematura_membranas = models.BooleanField(null=True, blank=True)
    otras_patologias = models.TextField(null=True, blank=True)
    
    # Tratamiento
    medicamentos_activos = models.TextField(null=True, blank=True)
    acido_folico = models.BooleanField(null=True, blank=True)
    sulfato_ferroso = models.BooleanField(null=True, blank=True)
    aspirina_profilactica = models.BooleanField(null=True, blank=True)
    otros_tratamientos = models.TextField(null=True, blank=True)
    
    # Historia Obstétrica - CRÍTICA PARA PARTO
    numero_gestas = models.IntegerField(null=True, blank=True)
    numero_partos = models.IntegerField(null=True, blank=True)
    partos_vaginales_previos = models.IntegerField(null=True, blank=True)
    cesareas_previas = models.IntegerField(null=True, blank=True)
    numero_abortos = models.IntegerField(null=True, blank=True)
    hijos_vivos = models.IntegerField(null=True, blank=True)
    paridad_formato = models.CharField(max_length=20, null=True, blank=True)
    
    # Examen Físico
    edema_grado = models.CharField(max_length=15, null=True, blank=True)
    edema_localizacion = models.CharField(max_length=100, null=True, blank=True)
    varices = models.BooleanField(null=True, blank=True)
    reflejos_osteotendinosos = models.CharField(max_length=50, null=True, blank=True)
    
    # Plan de Parto
    numero_aro = models.CharField(max_length=20, null=True, blank=True)
    nivel_riesgo = models.CharField(max_length=10, null=True, blank=True)
    tiene_plan_parto = models.BooleanField(null=True, blank=True)
    realizo_visita_guiada = models.BooleanField(null=True, blank=True)
    
    # Notas
    fecha_proximo_control = models.DateField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    indicaciones_medicas = models.TextField(null=True, blank=True)
    motivo_consulta = models.TextField(null=True, blank=True)
    turno = models.CharField(max_length=10, null=True, blank=True)
    fecha_hora_registro = models.DateTimeField(null=True, blank=True)
    sistema_origen = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'controles_previos'
        ordering = ['-fecha_control']

    def __str__(self):
        return f"Control {self.fecha_control} ({self.paciente_rut})"
