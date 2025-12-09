# 📁 legacyApp - Integración con Sistema Heredado

## Descripción

La aplicación `legacyApp` permite la integración con el sistema heredado del hospital, facilitando la consulta de datos históricos como controles prenatales previos y antecedentes de pacientes que fueron registrados en el sistema anterior.

---

## 📊 Modelos

### ControlesPrevios

```python
class ControlesPrevios(models.Model):
    """
    Modelo para consultar controles previos del sistema legacy
    Solo lectura - No se modifican estos datos
    """
    
    # Identificación del paciente (legacy)
    rut_paciente = models.CharField(
        max_length=20,
        verbose_name='RUT Paciente'
    )
    
    # Datos del control
    fecha_control = models.DateField(
        verbose_name='Fecha del Control'
    )
    
    semana_gestacional = models.IntegerField(
        null=True, blank=True,
        verbose_name='Semana Gestacional'
    )
    
    peso = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        verbose_name='Peso (kg)'
    )
    
    presion_arterial = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Presión Arterial'
    )
    
    altura_uterina = models.DecimalField(
        max_digits=4, decimal_places=1,
        null=True, blank=True,
        verbose_name='Altura Uterina (cm)'
    )
    
    fcf = models.IntegerField(
        null=True, blank=True,
        verbose_name='FCF (latidos/min)'
    )
    
    movimientos_fetales = models.BooleanField(
        default=False,
        verbose_name='Movimientos Fetales'
    )
    
    presentacion = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Presentación'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    profesional = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Profesional que Realizó el Control'
    )
    
    establecimiento = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Establecimiento'
    )
    
    class Meta:
        app_label = 'legacyApp'
        managed = False  # Django no gestiona esta tabla
        db_table = 'legacy_controles_previos'
        verbose_name = 'Control Previo (Legacy)'
        verbose_name_plural = 'Controles Previos (Legacy)'
        ordering = ['-fecha_control']
```

---

## ⚙️ Configuración de Base de Datos Dual

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'obstetric_care',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'legacy': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital_legacy',
        'USER': os.environ.get('LEGACY_DB_USER'),
        'PASSWORD': os.environ.get('LEGACY_DB_PASSWORD'),
        'HOST': os.environ.get('LEGACY_DB_HOST', 'localhost'),
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/legacy.cnf',
        }
    }
}

# Router para bases de datos
DATABASE_ROUTERS = ['legacyApp.routers.LegacyRouter']
```

### Router de Base de Datos

```python
# legacyApp/routers.py
class LegacyRouter:
    """Router para dirigir consultas legacy a la BD correcta"""
    
    legacy_apps = {'legacyApp'}
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.legacy_apps:
            return 'legacy'
        return 'default'
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.legacy_apps:
            return None  # No permitir escritura en legacy
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.legacy_apps:
            return False  # No migrar modelos legacy
        return db == 'default'
```

---

## 🔗 URLs

```python
# legacyApp/urls.py
app_name = 'legacy'

urlpatterns = [
    # Consulta de controles previos
    path('controles/<str:rut>/', views.consultar_controles_previos, name='consultar_controles'),
    
    # API
    path('api/controles/<str:rut>/', views.api_controles_previos, name='api_controles'),
]
```

---

## 📋 Vistas

### consultar_controles_previos

```python
@login_required
def consultar_controles_previos(request, rut):
    """
    Consultar controles previos de un paciente en sistema legacy
    """
    # Normalizar RUT
    rut_normalizado = normalizar_rut(rut)
    
    # Buscar en BD legacy
    controles = ControlesPrevios.objects.using('legacy').filter(
        rut_paciente=rut_normalizado
    ).order_by('-fecha_control')
    
    # Buscar paciente actual si existe
    try:
        persona = Persona.objects.get(Rut=rut_normalizado)
        paciente = Paciente.objects.get(persona=persona)
    except (Persona.DoesNotExist, Paciente.DoesNotExist):
        paciente = None
    
    context = {
        'rut': rut,
        'controles': controles,
        'paciente': paciente,
        'total_controles': controles.count(),
        'titulo': f'Controles Previos - {rut}'
    }
    return render(request, 'Legacy/controles_previos.html', context)
```

---

## 🖼️ Templates

```
templates/Legacy/
├── controles_previos.html     # Lista de controles previos
├── detalle_control.html       # Detalle de un control
└── buscar_legacy.html         # Formulario de búsqueda
```

---

## 📊 Flujo de Integración

```
1. Usuario busca paciente por RUT
              ↓
2. Sistema busca en BD principal (obstetric_care)
              ↓
3. Si existe, muestra datos actuales
              ↓
4. Paralelamente consulta BD legacy
              ↓
5. Muestra controles previos del sistema anterior
              ↓
6. Usuario puede importar datos relevantes
```

---

## 📊 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────┐
│                   OB_CARE                        │
│                  (Django)                        │
└─────────────────────┬───────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   obstetric_care │     │  hospital_legacy │
│   (MySQL - RW)   │     │   (MySQL - RO)   │
│                 │     │                 │
│ - gestionApp    │     │ - controles     │
│ - matronaApp    │     │ - antecedentes  │
│ - partosApp     │     │ - historico     │
│ - etc.          │     │                 │
└─────────────────┘     └─────────────────┘
```

---

## 🔐 Seguridad

| Aspecto | Implementación |
|---------|----------------|
| Solo lectura | `managed = False`, Router bloquea escritura |
| Autenticación | Solo usuarios autenticados |
| Logging | Registro de cada consulta legacy |
| Sanitización | RUT normalizado antes de consultar |

---

## 📌 Notas Importantes

1. **Solo Lectura**: Los datos legacy nunca se modifican desde OB_CARE.
2. **managed = False**: Django no crea/modifica tablas legacy.
3. **Router**: Dirige automáticamente las consultas a la BD correcta.
4. **Migración Gradual**: Permite operar mientras se migran datos.

---

*Documentación de legacyApp - OB_CARE v1.0*
