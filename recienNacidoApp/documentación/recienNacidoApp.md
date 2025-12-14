# 📁 recienNacidoApp - Registro de Recién Nacido

## Descripción

La aplicación `recienNacidoApp` gestiona el registro completo del recién nacido en 9 pasos, incluyendo datos básicos, puntuación Apgar, cordón umbilical, apego, acompañamiento, alimentación, evaluaciones, complicaciones y documentos de parto.

---

## 📊 Modelos

### Catálogos

| Modelo | Descripción |
|--------|-------------|
| `CatalogoSexoRN` | Sexo del recién nacido |

### RegistroRecienNacido

```python
class RegistroRecienNacido(models.Model):
    """Registro completo del recién nacido"""
    
    # ========================================
    # RELACIONES
    # ========================================
    registro_parto = models.ForeignKey(
        'partosApp.RegistroParto',
        on_delete=models.CASCADE,
        related_name='recien_nacidos'
    )
    
    # ========================================
    # DATOS BÁSICOS
    # ========================================
    sexo = models.ForeignKey(CatalogoSexoRN, on_delete=models.PROTECT)
    
    peso = models.DecimalField(
        max_digits=6, decimal_places=2,
        validators=[MinValueValidator(300), MaxValueValidator(6000)],
        verbose_name='Peso (gramos)'
    )
    
    talla = models.DecimalField(
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(20), MaxValueValidator(60)],
        verbose_name='Talla (cm)'
    )
    
    perimetro_cefalico = models.DecimalField(
        max_digits=4, decimal_places=1,
        null=True, blank=True,
        verbose_name='Perímetro Cefálico (cm)'
    )
    
    # ========================================
    # APGAR
    # ========================================
    apgar_1_minuto = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar al 1 minuto'
    )
    
    apgar_5_minutos = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar a los 5 minutos'
    )
    
    apgar_10_minutos = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar a los 10 minutos'
    )
    
    # ========================================
    # CORDÓN UMBILICAL
    # ========================================
    clampeo_oportuno = models.BooleanField(
        default=False,
        verbose_name='Clampeo Oportuno (>1 min)'
    )
    
    tiempo_clampeo_segundos = models.IntegerField(
        null=True, blank=True,
        verbose_name='Tiempo de Clampeo (segundos)'
    )
    
    sangre_cordon_recolectada = models.BooleanField(
        default=False,
        verbose_name='Sangre de Cordón Recolectada'
    )
    
    # ========================================
    # APEGO
    # ========================================
    contacto_piel_piel = models.BooleanField(
        default=False,
        verbose_name='Contacto Piel a Piel'
    )
    
    tiempo_piel_piel_minutos = models.IntegerField(
        null=True, blank=True,
        verbose_name='Tiempo Piel a Piel (minutos)'
    )
    
    lactancia_primera_hora = models.BooleanField(
        default=False,
        verbose_name='Lactancia en Primera Hora'
    )
    
    # ========================================
    # ACOMPAÑAMIENTO
    # ========================================
    padre_presente = models.BooleanField(
        default=False,
        verbose_name='Padre Presente'
    )
    
    otro_acompanante = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Otro Acompañante'
    )
    
    # ========================================
    # ALIMENTACIÓN
    # ========================================
    tipo_alimentacion = models.CharField(
        max_length=50,
        verbose_name='Tipo de Alimentación'
    )  # LACTANCIA_EXCLUSIVA, FORMULA, MIXTA
    
    # ========================================
    # EVALUACIONES
    # ========================================
    vitamina_k_administrada = models.BooleanField(default=False)
    profilaxis_ocular = models.BooleanField(default=False)
    vacuna_hepatitis_b = models.BooleanField(default=False)
    tamizaje_auditivo = models.BooleanField(default=False)
    tamizaje_cardiaco = models.BooleanField(default=False)
    
    # ========================================
    # COMPLICACIONES
    # ========================================
    requirio_reanimacion = models.BooleanField(default=False)
    tipo_reanimacion = models.CharField(max_length=200, blank=True)
    ingreso_neonatologia = models.BooleanField(default=False)
    motivo_ingreso_neo = models.TextField(blank=True)
    
    # ========================================
    # OBSERVACIONES
    # ========================================
    observaciones = models.TextField(blank=True)
    
    # Control
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
```

### DocumentosParto

```python
class DocumentosParto(models.Model):
    """Documentos generados del parto"""
    
    registro_recien_nacido = models.OneToOneField(
        RegistroRecienNacido,
        on_delete=models.CASCADE,
        related_name='documentos'
    )
    
    certificado_nacimiento = models.BooleanField(default=False)
    constancia_parto = models.BooleanField(default=False)
    carnet_control = models.BooleanField(default=False)
    
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

---

## 🔗 URLs

```python
# recienNacidoApp/urls.py
app_name = 'recien_nacido'

urlpatterns = [
    # Registro en 9 pasos
    path('crear/<int:registro_parto_pk>/paso1/', views.crear_registro_rn_paso1, name='crear_rn_paso1'),
    path('paso2/', views.crear_registro_rn_paso2, name='crear_rn_paso2'),
    path('paso3/', views.crear_registro_rn_paso3, name='crear_rn_paso3'),
    path('paso4/', views.crear_registro_rn_paso4, name='crear_rn_paso4'),
    path('paso5/', views.crear_registro_rn_paso5, name='crear_rn_paso5'),
    path('paso6/', views.crear_registro_rn_paso6, name='crear_rn_paso6'),
    path('paso7/', views.crear_registro_rn_paso7, name='crear_rn_paso7'),
    path('paso8/', views.crear_registro_rn_paso8, name='crear_rn_paso8'),
    path('paso9/', views.crear_registro_rn_paso9, name='crear_rn_paso9'),
    
    # Detalle
    path('<int:pk>/', views.detalle_registro_rn, name='detalle'),
]
```

---

## 📋 Los 9 Pasos del Registro de Recién Nacido

| Paso | Nombre | Formulario | Descripción |
|------|--------|------------|-------------|
| 1 | Datos Básicos | `RegistroRecienNacidoDatosForm` | Sexo, peso, talla, PC |
| 2 | Apgar | `RegistroRecienNacidoApgarForm` | Apgar 1', 5', 10' |
| 3 | Cordón | `RegistroRecienNacidoCordónForm` | Clampeo, sangre cordón |
| 4 | Apego | `RegistroRecienNacidoApegoForm` | Piel a piel, lactancia |
| 5 | Acompañamiento | `RegistroRecienNacidoAcompañamientoForm` | Padre, acompañante |
| 6 | Alimentación | `RegistroRecienNacidoAlimentacionForm` | Tipo de alimentación |
| 7 | Evaluaciones | `RegistroRecienNacidoEvaluacionesForm` | Vitamina K, tamizajes |
| 8 | Complicaciones | `RegistroRecienNacidoComplicacionesForm` | Reanimación, neo |
| 9 | Documentos | `DocumentosPartoForm` | Certificados, carnet |

---

## 🖼️ Templates

```
templates/RecienNacido/
├── form_rn_paso1_datos.html        # Paso 1: Datos básicos
├── form_rn_paso2_apgar.html        # Paso 2: Apgar
├── form_rn_paso3_cordon.html       # Paso 3: Cordón
├── form_rn_paso4_apego.html        # Paso 4: Apego
├── form_rn_paso5_acompanamiento.html # Paso 5: Acompañamiento
├── form_rn_paso6_alimentacion.html # Paso 6: Alimentación
├── form_rn_paso7_evaluaciones.html # Paso 7: Evaluaciones
├── form_rn_paso8_complicaciones.html # Paso 8: Complicaciones
├── form_rn_paso9_documentos.html   # Paso 9: Documentos
└── detalle_rn.html                 # Detalle completo
```

---

## 📊 Puntuación Apgar

| Criterio | 0 | 1 | 2 |
|----------|---|---|---|
| **A**pariencia (color) | Azul/pálido | Cuerpo rosado, extremidades azules | Completamente rosado |
| **P**ulso | Ausente | <100 lpm | ≥100 lpm |
| **G**esticulación (reflejos) | Sin respuesta | Mueca | Llanto vigoroso |
| **A**ctividad (tono) | Flácido | Alguna flexión | Movimiento activo |
| **R**espiración | Ausente | Lenta, irregular | Llanto fuerte |

**Interpretación:**
- 7-10: Normal
- 4-6: Depresión moderada
- 0-3: Depresión severa

---

## 📊 Rangos Normales

| Parámetro | Mínimo | Máximo | Unidad |
|-----------|--------|--------|--------|
| Peso | 300 | 6000 | gramos |
| Talla | 20 | 60 | cm |
| PC | 30 | 40 | cm |
| Apgar | 0 | 10 | puntos |

---

## 📊 Diagrama de Relaciones

```
┌─────────────────┐
│ RegistroParto   │
└────────┬────────┘
         │
         │ ForeignKey
         ▼
┌─────────────────────┐
│RegistroRecienNacido │
└────────┬────────────┘
         │
         │ OneToOne
         ▼
┌─────────────────┐
│ DocumentosParto │
└─────────────────┘
```

---

## 🔐 Permisos

| Acción | Médico | Matrona | TENS | Admin |
|--------|--------|---------|------|-------|
| Ver registros | ✅ | ✅ | ❌ | ✅ |
| Crear registros | ✅ | ✅ | ❌ | ✅ |
| Editar registros | ✅ | ✅ | ❌ | ✅ |
| Generar documentos | ✅ | ✅ | ❌ | ✅ |

---

## 📌 Notas Importantes

1. **Prerequisito**: Requiere RegistroParto completado.
2. **Apgar Obligatorio**: 1' y 5' son obligatorios, 10' opcional.
3. **Múltiples RN**: Un parto puede tener múltiples recién nacidos (gemelar).
4. **Documentos**: Se generan al finalizar el registro.

---

*Documentación de recienNacidoApp - OB_CARE v1.0*
