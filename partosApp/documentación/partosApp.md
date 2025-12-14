# 📁 partosApp - Registro de Parto (9 Pasos)

## Descripción

La aplicación `partosApp` gestiona el registro completo del parto en 9 pasos secuenciales, desde la información básica hasta las observaciones finales, incluyendo datos obstétricos, alumbramiento, anestesia, apego y cumplimiento de la Ley Dominga.

---

## 📊 Modelos

### Catálogos

| Modelo | Descripción |
|--------|-------------|
| `CatalogoTipoParto` | Tipos de parto (Vaginal, Cesárea, Fórceps, Ventosa) |
| `CatalogoClasificacionRobson` | Clasificación de Robson (10 grupos) |
| `CatalogoPosicionParto` | Posiciones maternas durante el parto |
| `CatalogoEstadoPerine` | Estados del periné post-parto |
| `CatalogoCausaCesarea` | Causas de cesárea |
| `CatalogoMotivoPartoNoAcompanado` | Motivos de parto sin acompañante |
| `CatalogoPersonaAcompanante` | Tipo de persona acompañante |
| `CatalogoMetodoNoFarmacologico` | Métodos no farmacológicos de alivio |

### RegistroParto

```python
class RegistroParto(models.Model):
    """Registro completo del parto"""
    
    # ========================================
    # RELACIONES
    # ========================================
    ficha = models.ForeignKey('matronaApp.FichaObstetrica', on_delete=models.CASCADE)
    ficha_ingreso = models.OneToOneField('ingresoPartoApp.FichaParto', on_delete=models.PROTECT)
    
    # ========================================
    # IDENTIFICACIÓN
    # ========================================
    numero_registro = models.CharField(max_length=20, unique=True)  # PARTO-000001
    
    # ========================================
    # FECHAS Y HORAS
    # ========================================
    fecha_hora_admision = models.DateTimeField()
    fecha_hora_parto = models.DateTimeField(null=True)
    
    # ========================================
    # INFORMACIÓN OBSTÉTRICA
    # ========================================
    edad_gestacional_semanas = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(42)]
    )
    edad_gestacional_dias = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    
    tipo_parto = models.ForeignKey(CatalogoTipoParto, on_delete=models.PROTECT)
    clasificacion_robson = models.ForeignKey(CatalogoClasificacionRobson, on_delete=models.SET_NULL, null=True)
    posicion_parto = models.ForeignKey(CatalogoPosicionParto, on_delete=models.SET_NULL, null=True)
    ofrecimiento_posiciones_alternativas = models.BooleanField(default=False)
    
    # ========================================
    # ALUMBRAMIENTO
    # ========================================
    alumbramiento_dirigido = models.BooleanField(default=False)
    retira_placenta = models.BooleanField(default=False)
    estampado_placenta = models.BooleanField(default=False)
    
    # ========================================
    # PERINÉ
    # ========================================
    estado_perine = models.ForeignKey(CatalogoEstadoPerine, on_delete=models.SET_NULL, null=True)
    episiotomia = models.BooleanField(default=False)
    desgarro_grado = models.IntegerField(null=True)  # 1, 2, 3, 4
    sutura_realizada = models.BooleanField(default=False)
    
    # ========================================
    # ANESTESIA
    # ========================================
    anestesia_epidural = models.BooleanField(default=False)
    anestesia_raquidea = models.BooleanField(default=False)
    anestesia_general = models.BooleanField(default=False)
    anestesia_local = models.BooleanField(default=False)
    sin_anestesia = models.BooleanField(default=False)
    
    # ========================================
    # APEGO Y ACOMPAÑAMIENTO
    # ========================================
    apego_inmediato = models.BooleanField(default=False)
    tiempo_apego_minutos = models.IntegerField(null=True)
    parto_acompanado = models.BooleanField(default=False)
    persona_acompanante = models.ForeignKey(CatalogoPersonaAcompanante, on_delete=models.SET_NULL, null=True)
    motivo_no_acompanado = models.ForeignKey(CatalogoMotivoPartoNoAcompanado, on_delete=models.SET_NULL, null=True)
    
    # ========================================
    # LEY DOMINGA N° 21.372
    # ========================================
    informacion_ley_dominga = models.BooleanField(default=False)
    consentimiento_ley_dominga = models.BooleanField(default=False)
    
    # ========================================
    # OBSERVACIONES
    # ========================================
    observaciones = models.TextField(blank=True)
    
    # Control
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
```

---

## 🔗 URLs

```python
# partosApp/urls.py
app_name = 'partos'

urlpatterns = [
    # Menú
    path('', views.menu_partos, name='menu_partos'),
    
    # Registro en 9 pasos
    path('registro/<int:ficha_parto_pk>/paso1/', views.crear_registro_parto_paso1, name='crear_registro_parto_paso1'),
    path('registro/paso2/', views.crear_registro_parto_paso2, name='crear_registro_parto_paso2'),
    path('registro/paso3/', views.crear_registro_parto_paso3, name='crear_registro_parto_paso3'),
    path('registro/paso4/', views.crear_registro_parto_paso4, name='crear_registro_parto_paso4'),
    path('registro/paso5/', views.crear_registro_parto_paso5, name='crear_registro_parto_paso5'),
    path('registro/paso6/', views.crear_registro_parto_paso6, name='crear_registro_parto_paso6'),
    path('registro/paso7/', views.crear_registro_parto_paso7, name='crear_registro_parto_paso7'),
    path('registro/paso8/', views.crear_registro_parto_paso8, name='crear_registro_parto_paso8'),
    path('registro/paso9/', views.crear_registro_parto_paso9, name='crear_registro_parto_paso9'),
    
    # Detalle y lista
    path('registro/<int:registro_pk>/', views.detalle_registro_parto, name='detalle_registro'),
    path('registros/', views.lista_registros_parto, name='lista_registros'),
]
```

---

## 📋 Los 9 Pasos del Registro de Parto

| Paso | Nombre | Formulario | Descripción |
|------|--------|------------|-------------|
| 1 | Información Básica | `RegistroPartoBaseForm` | Fecha admisión, edad gestacional |
| 2 | Datos Obstétricos | `RegistroPartoObstetricoForm` | Tipo parto, Robson, posición |
| 3 | Alumbramiento | `RegistroPartoAlubramientoForm` | Placenta, alumbramiento dirigido |
| 4 | Periné | `RegistroPartoPerinealForm` | Estado periné, episiotomía, desgarros |
| 5 | Anestesia | `RegistroPartoAnestesiaForm` | Tipo de anestesia utilizada |
| 6 | Apego | `RegistroPartoApegoForm` | Apego inmediato, tiempo, acompañamiento |
| 7 | Profesionales | `RegistroPartoProfesionalesForm` | Equipo médico, causas intervención |
| 8 | Ley Dominga | `RegistroPartoLeyDomingaForm` | Información y consentimiento |
| 9 | Observaciones | `RegistroPartoObservacionesForm` | Notas finales |

---

## 🖼️ Templates

```
templates/Parto/
├── menu_partos.html                    # Menú principal
├── form_parto_paso1.html               # Paso 1: Info básica
├── form_parto_paso2.html               # Paso 2: Datos obstétricos
├── form_parto_paso3.html               # Paso 3: Alumbramiento
├── form_parto_paso4.html               # Paso 4: Periné
├── form_parto_paso5_anestesia.html     # Paso 5: Anestesia
├── form_parto_paso6_apego.html         # Paso 6: Apego
├── form_parto_paso7_profesionales.html # Paso 7: Profesionales
├── form_parto_paso8_ley_dominga.html   # Paso 8: Ley Dominga
├── form_parto_paso9_final.html         # Paso 9: Observaciones
├── detalle_registro_parto.html         # Detalle completo
└── lista_registros_parto.html          # Lista de registros
```

---

## 📊 Clasificación de Robson

| Grupo | Descripción |
|-------|-------------|
| 1 | Nulíparas, parto espontáneo, feto único, cefálico, ≥37 semanas |
| 2 | Nulíparas, inducción o cesárea antes del trabajo de parto |
| 3 | Multíparas sin cesárea previa, parto espontáneo |
| 4 | Multíparas sin cesárea previa, inducción o cesárea |
| 5 | Cesárea previa, feto único, cefálico, ≥37 semanas |
| 6 | Nulíparas, presentación podálica |
| 7 | Multíparas, presentación podálica |
| 8 | Embarazo múltiple |
| 9 | Presentación transversa u oblicua |
| 10 | Feto único, cefálico, <37 semanas |

---

## 📊 Diagrama de Relaciones

```
┌─────────────────┐      ┌─────────────────┐
│ FichaObstetrica │      │   FichaParto    │
└────────┬────────┘      └────────┬────────┘
         │                        │
         │ ForeignKey    OneToOne │
         │                        │
         └────────────┬───────────┘
                      │
                      ▼
              ┌───────────────┐
              │ RegistroParto │
              └───────┬───────┘
                      │
                      │ OneToOne
                      ▼
              ┌───────────────────┐
              │RegistroRecienNacido│
              └───────────────────┘
```

---

## ⚖️ Ley Dominga N° 21.372

La Ley Dominga establece derechos para madres y padres de recién nacidos fallecidos:

- **Información**: Derecho a ser informados sobre opciones de despedida
- **Acompañamiento**: Derecho a tiempo con el bebé fallecido
- **Documentos**: Derecho a recibir constancia de nacimiento
- **Sepultura**: Derecho a decidir sobre el destino del cuerpo

```python
# Campos relacionados
informacion_ley_dominga = models.BooleanField(default=False)
consentimiento_ley_dominga = models.BooleanField(default=False)
```

---

## 🔐 Permisos

| Acción | Médico | Matrona | TENS | Admin |
|--------|--------|---------|------|-------|
| Ver registros | ✅ | ✅ | ❌ | ✅ |
| Crear registros | ✅ | ✅ | ❌ | ✅ |
| Editar registros | ✅ | ✅ | ❌ | ✅ |
| Completar pasos | ✅ | ✅ | ❌ | ✅ |

---

## 📌 Notas Importantes

1. **Sesión**: Los pasos se mantienen en sesión del usuario.
2. **Secuencial**: Debe completarse paso a paso.
3. **Prerequisito**: Requiere FichaParto (ingresoPartoApp).
4. **Número Único**: Se genera automáticamente (PARTO-000001).

---

*Documentación de partosApp - OB_CARE v1.0*
