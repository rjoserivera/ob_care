# 📁 matronaApp - Fichas Obstétricas y Medicamentos

## Descripción

La aplicación `matronaApp` gestiona las fichas obstétricas de las pacientes, el ingreso hospitalario, la asignación de medicamentos y el control del embarazo por parte de las matronas.

---

## 📊 Modelos

### Catálogos

| Modelo | Descripción |
|--------|-------------|
| `CatalogoViaAdministracion` | Vías de administración de medicamentos (oral, IV, IM, etc.) |
| `CatalogoConsultorioOrigen` | Consultorios de referencia |

### FichaObstetrica

```python
class FichaObstetrica(models.Model):
    """Ficha obstétrica - Información completa de la gestante"""
    
    # Relaciones
    paciente = models.OneToOneField('gestionApp.Paciente', on_delete=models.CASCADE)
    matrona_responsable = models.ForeignKey('gestionApp.Matrona', on_delete=models.PROTECT)
    patologias = models.ManyToManyField('medicoApp.Patologias', blank=True)
    
    # Identificación
    numero_ficha = models.CharField(max_length=20, unique=True)
    nombre_acompanante = models.CharField(max_length=200)
    
    # Antecedentes obstétricos
    numero_gestas = models.IntegerField()          # Gestaciones totales
    numero_partos = models.IntegerField()          # Partos totales
    partos_vaginales = models.IntegerField()       # Partos vaginales
    partos_cesareas = models.IntegerField()        # Cesáreas
    numero_abortos = models.IntegerField()         # Abortos
    nacidos_vivos = models.IntegerField()          # Nacidos vivos
    
    # Fechas
    fecha_ultima_regla = models.DateField(null=True)
    fecha_probable_parto = models.DateField(null=True)
    
    # Edad gestacional
    edad_gestacional_semanas = models.IntegerField(null=True)
    edad_gestacional_dias = models.IntegerField(null=True)
    
    # Datos antropométricos
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    talla = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Exámenes de laboratorio
    vih_tomado = models.BooleanField(default=False)
    vih_resultado = models.CharField(max_length=20)
    sgb_pesquisa = models.BooleanField(default=False)
    sgb_resultado = models.CharField(max_length=20)
    vdrl_resultado = models.CharField(max_length=20)
    hepatitis_b_tomado = models.BooleanField(default=False)
    hepatitis_b_resultado = models.CharField(max_length=20)
    
    # Control
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
```

### IngresoPaciente

```python
class IngresoPaciente(models.Model):
    """Registro de ingreso hospitalario de paciente"""
    
    paciente = models.ForeignKey('gestionApp.Paciente', on_delete=models.CASCADE)
    numero_ficha = models.CharField(max_length=20, unique=True)
    
    motivo_ingreso = models.TextField()
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()
    edad_gestacional_semanas = models.IntegerField(null=True)
    derivacion = models.CharField(max_length=200)
    observaciones = models.TextField()
    activo = models.BooleanField(default=True)
```

### MedicamentoFicha

```python
class MedicamentoFicha(models.Model):
    """Medicamentos asignados a una ficha obstétrica"""
    
    ficha = models.ForeignKey(FichaObstetrica, on_delete=models.CASCADE, related_name='medicamentos')
    
    medicamento = models.CharField(max_length=200)
    dosis = models.CharField(max_length=100)
    via_administracion = models.ForeignKey(CatalogoViaAdministracion, on_delete=models.PROTECT)
    frecuencia = models.CharField(max_length=100)  # "Cada 6 horas", "Cada 8 horas"
    
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField(null=True, blank=True)
    indicaciones = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

### AdministracionMedicamento

```python
class AdministracionMedicamento(models.Model):
    """Registro de administración de medicamentos"""
    
    medicamento_ficha = models.ForeignKey(MedicamentoFicha, on_delete=models.CASCADE, related_name='administraciones')
    tens = models.ForeignKey('gestionApp.Tens', on_delete=models.SET_NULL, null=True)
    
    fecha_hora_administracion = models.DateTimeField(default=timezone.now)
    se_realizo_lavado = models.BooleanField(default=False)
    observaciones = models.TextField()
    reacciones_adversas = models.TextField()
    administrado_exitosamente = models.BooleanField(default=True)
    motivo_no_administracion = models.TextField()
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
```

---

## 🔗 URLs

```python
# matronaApp/urls.py
app_name = 'matrona'

urlpatterns = [
    # Menú principal
    path('', views.menu_matrona, name='menu_matrona'),
    
    # Pacientes
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('buscar/', views.buscar_paciente, name='buscar_paciente'),
    
    # Fichas Obstétricas
    path('fichas/', views.lista_fichas_obstetrica, name='lista_fichas'),
    path('ficha/<int:ficha_pk>/', views.detalle_ficha_obstetrica, name='detalle_ficha'),
    path('ficha/crear-persona/<int:persona_pk>/', views.crear_ficha_obstetrica_persona, name='crear_ficha_persona'),
    path('ficha/<int:ficha_pk>/editar/', views.editar_ficha_obstetrica, name='editar_ficha'),
    
    # Medicamentos
    path('ficha/<int:ficha_pk>/medicamento/agregar/', views.agregar_medicamento, name='agregar_medicamento'),
    path('medicamento/<int:medicamento_pk>/eliminar/', views.eliminar_medicamento, name='eliminar_medicamento'),
]
```

---

## 🖼️ Templates

```
templates/Matrona/
├── menu_matrona.html              # Menú principal
├── lista_pacientes.html           # Lista de pacientes
├── buscar_paciente.html           # Búsqueda por RUT
├── lista_fichas_obstetrica.html   # Lista de fichas
├── detalle_ficha_obstetrica.html  # Detalle de ficha
├── form_obstetrica_materna.html   # Crear/editar ficha
├── medicamento_form.html          # Agregar medicamento
├── medicamento_confirmar_delete.html  # Confirmar eliminación
└── Data/
    └── dashboard_matrona.html     # Dashboard
```

---

## 📊 Flujo de Trabajo

```
1. Buscar/Crear Paciente
         ↓
2. Crear Ficha Obstétrica
         ↓
3. Registrar Antecedentes
   - Gestas, partos, abortos
   - Fecha última regla
   - Patologías
         ↓
4. Agregar Medicamentos
         ↓
5. TENS Administra Medicamentos
         ↓
6. Seguimiento y Control
```

---

## 📋 Vistas Principales

### menu_matrona
```python
@login_required
def menu_matrona(request):
    """Menú principal de matrona"""
    total_fichas = FichaObstetrica.objects.filter(activa=True).count()
    fichas_recientes = FichaObstetrica.objects.filter(activa=True).order_by('-fecha_creacion')[:5]
    
    context = {
        'titulo': 'Matrona - Control Prenatal',
        'total_fichas': total_fichas,
        'fichas_recientes': fichas_recientes
    }
    return render(request, 'Matrona/menu_matrona.html', context)
```

### crear_ficha_obstetrica_persona
```python
@login_required
def crear_ficha_obstetrica_persona(request, persona_pk):
    """Crear ficha a partir de una persona"""
    persona = get_object_or_404(Persona, pk=persona_pk)
    
    # Obtener o crear paciente
    paciente, created = Paciente.objects.get_or_create(
        persona=persona,
        defaults={'activo': True}
    )
    
    # Calcular edad
    edad = calcular_edad(persona.Fecha_nacimiento)
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.paciente = paciente
            ficha.save()
            return redirect('matrona:detalle_ficha', ficha_pk=ficha.pk)
    # ...
```

---

## 📊 Diagrama de Relaciones

```
┌─────────────────┐
│    Paciente     │
└────────┬────────┘
         │
         │ OneToOne
         ▼
┌─────────────────┐      ┌─────────────────┐
│ FichaObstetrica │──────│    Patologias   │
└────────┬────────┘      └─────────────────┘
         │                   (ManyToMany)
         │ ForeignKey
         ▼
┌─────────────────┐
│MedicamentoFicha │
└────────┬────────┘
         │
         │ ForeignKey
         ▼
┌─────────────────┐      ┌─────────────────┐
│Administracion   │──────│      TENS       │
│  Medicamento    │      └─────────────────┘
└─────────────────┘
```

---

## 🔐 Permisos

| Acción | Matrona | Médico | TENS | Admin |
|--------|---------|--------|------|-------|
| Ver fichas | ✅ | ✅ | ❌ | ✅ |
| Crear fichas | ✅ | ✅ | ❌ | ✅ |
| Editar fichas | ✅ | ✅ | ❌ | ✅ |
| Agregar medicamentos | ✅ | ✅ | ❌ | ✅ |
| Administrar medicamentos | ❌ | ❌ | ✅ | ✅ |

---

## 📌 Notas Importantes

1. **Ficha Única**: Cada paciente tiene una sola ficha obstétrica activa.
2. **Trazabilidad de Medicamentos**: Cada administración queda registrada con TENS responsable.
3. **Exámenes de Laboratorio**: VIH, SGB, VDRL, Hepatitis B son obligatorios.
4. **Edad Gestacional**: Se calcula automáticamente desde la fecha de última regla.

---

*Documentación de matronaApp - OB_CARE v1.0*
