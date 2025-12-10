# 📁 ingresoPartoApp - Ficha de Ingreso a Parto

## Descripción

La aplicación `ingresoPartoApp` gestiona el proceso de ingreso de la paciente al área de parto, registrando información crítica como exámenes de laboratorio (VIH, SGB, VDRL, Hepatitis B), condiciones de ingreso y patologías activas.

---

## 📊 Modelos

### Catálogos

| Modelo | Descripción |
|--------|-------------|
| `CatalogoEstadoCervical` | Estados del cuello uterino |
| `CatalogoEstadoFetal` | Estados del bienestar fetal |

### FichaParto

```python
class FichaParto(models.Model):
    """Ficha de ingreso a parto - Información al momento del ingreso"""
    
    # Relación
    ficha_obstetrica = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.CASCADE,
        related_name='fichas_parto'
    )
    
    # Identificación
    numero_ficha_parto = models.CharField(max_length=20, unique=True)
    
    # Tipo de ingreso
    tipo_paciente = models.CharField(max_length=30)  # URGENCIA, PROGRAMADA, DERIVADA
    origen_ingreso = models.CharField(max_length=20)  # URGENCIAS, CONSULTA, DERIVACION
    
    # Fechas
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()
    
    # Control prenatal
    plan_de_parto = models.BooleanField(default=False)
    visita_guiada = models.BooleanField(default=False)
    control_prenatal = models.BooleanField(default=False)
    consultorio_origen = models.CharField(max_length=200)
    
    # ========================================
    # PATOLOGÍAS ACTIVAS
    # ========================================
    preeclampsia_severa = models.BooleanField(default=False)
    eclampsia = models.BooleanField(default=False)
    sepsis_infeccion_grave = models.BooleanField(default=False)
    infeccion_ovular = models.BooleanField(default=False)
    otra_patologia = models.CharField(max_length=300, blank=True)
    
    # ========================================
    # VIH
    # ========================================
    numero_aro = models.CharField(max_length=20, blank=True)
    vih_tomado_prepartos = models.BooleanField(default=False)
    vih_tomado_sala = models.BooleanField(default=False)
    vih_orden_toma = models.CharField(max_length=1)  # '1', '2', '3'
    
    # ========================================
    # STREPTOCOCCUS GRUPO B (SGB)
    # ========================================
    sgb_pesquisa = models.BooleanField(default=False)
    sgb_resultado = models.CharField(max_length=10)  # POSITIVO, NEGATIVO, PENDIENTE
    antibiotico_sgb = models.BooleanField(default=False)
    
    # ========================================
    # SÍFILIS (VDRL)
    # ========================================
    vdrl_resultado = models.CharField(max_length=15)  # POSITIVO, NEGATIVO, PENDIENTE
    tratamiento_sifilis = models.BooleanField(default=False)
    
    # ========================================
    # HEPATITIS B
    # ========================================
    hepatitis_b_tomado = models.BooleanField(default=False)
    derivacion_gastro = models.BooleanField(default=False)
    
    # Control
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ficha de Parto (Ingreso)'
        verbose_name_plural = 'Fichas de Parto (Ingreso)'
        indexes = [
            models.Index(fields=['numero_ficha_parto']),
            models.Index(fields=['ficha_obstetrica', '-fecha_creacion']),
        ]
```

---

## 🔗 URLs

```python
# ingresoPartoApp/urls.py
app_name = 'ingreso_parto'

urlpatterns = [
    # Menú
    path('', views.menu_ingreso_parto, name='menu'),
    
    # Fichas
    path('fichas/', views.lista_fichas_parto, name='lista_fichas'),
    path('ficha/crear/<int:ficha_obstetrica_pk>/', views.crear_ficha_parto, name='crear_ficha'),
    path('ficha/<int:pk>/', views.detalle_ficha_parto, name='detalle_ficha'),
    path('ficha/<int:pk>/editar/', views.editar_ficha_parto, name='editar_ficha'),
]
```

---

## 🖼️ Templates

```
templates/IngresoParto/
├── menu_ingreso_parto.html    # Menú principal
├── lista_fichas_parto.html    # Lista de fichas
├── ficha_parto_form.html      # Crear/editar ficha
└── detalle_ficha_parto.html   # Detalle de ficha
```

---

## 📋 Flujo de Ingreso a Parto

```
1. Paciente llega a Urgencias/Programada
              ↓
2. Verificar Ficha Obstétrica existente
              ↓
3. Crear Ficha de Ingreso a Parto
   - Tipo de paciente
   - Origen de ingreso
   - Plan de parto
              ↓
4. Registrar Patologías Activas
   - Preeclampsia
   - Eclampsia
   - Sepsis
   - Infección ovular
              ↓
5. Registrar Exámenes de Laboratorio
   - VIH (tomado en prepartos/sala)
   - SGB (pesquisa + resultado)
   - VDRL (resultado + tratamiento)
   - Hepatitis B
              ↓
6. Confirmar Ingreso
              ↓
7. Continuar a Registro de Parto (partosApp)
```

---

## 📊 Diagrama de Relaciones

```
┌─────────────────┐
│ FichaObstetrica │
└────────┬────────┘
         │
         │ ForeignKey
         ▼
┌─────────────────┐
│   FichaParto    │
│  (Ingreso)      │
└────────┬────────┘
         │
         │ OneToOne
         ▼
┌─────────────────┐
│ RegistroParto   │
└─────────────────┘
```

---

## 🔬 Exámenes de Laboratorio

### VIH
| Campo | Descripción |
|-------|-------------|
| `vih_tomado_prepartos` | Examen tomado antes del parto |
| `vih_tomado_sala` | Examen tomado en sala de partos |
| `vih_orden_toma` | Orden de toma (1°, 2°, 3°) |
| `numero_aro` | Número ARO si positivo |

### Streptococcus Grupo B (SGB)
| Campo | Descripción |
|-------|-------------|
| `sgb_pesquisa` | ¿Se realizó pesquisa? |
| `sgb_resultado` | POSITIVO / NEGATIVO / PENDIENTE |
| `antibiotico_sgb` | ¿Se administró antibiótico? |

### VDRL (Sífilis)
| Campo | Descripción |
|-------|-------------|
| `vdrl_resultado` | POSITIVO / NEGATIVO / PENDIENTE |
| `tratamiento_sifilis` | ¿Recibió tratamiento? |

### Hepatitis B
| Campo | Descripción |
|-------|-------------|
| `hepatitis_b_tomado` | ¿Examen tomado? |
| `derivacion_gastro` | ¿Derivada a gastroenterología? |

---

## 🔐 Permisos

| Acción | Médico | Matrona | TENS | Admin |
|--------|--------|---------|------|-------|
| Ver fichas | ✅ | ✅ | ❌ | ✅ |
| Crear fichas | ✅ | ✅ | ❌ | ✅ |
| Editar fichas | ✅ | ✅ | ❌ | ✅ |
| Iniciar parto | ✅ | ✅ | ❌ | ✅ |

---

## 📌 Notas Importantes

1. **Prerequisito**: Debe existir una FichaObstetrica antes de crear FichaParto.
2. **Exámenes Obligatorios**: VIH, SGB, VDRL, Hepatitis B son obligatorios según protocolo.
3. **Patologías Críticas**: Se heredan de la ficha obstétrica y se confirman al ingreso.
4. **Índices**: La BD tiene índices para búsqueda rápida.

---

*Documentación de ingresoPartoApp - OB_CARE v1.0*
