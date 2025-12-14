# 📁 medicoApp - Gestión de Patologías CIE-10

## Descripción

La aplicación `medicoApp` gestiona el catálogo de patologías según la Clasificación Internacional de Enfermedades (CIE-10), permitiendo a los médicos registrar y asociar diagnósticos a las fichas obstétricas.

---

## 📊 Modelos

### Patologias

```python
class Patologias(models.Model):
    """Catálogo de patologías según CIE-10"""
    
    codigo_cie10 = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Código CIE-10'
    )
    
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre de la Patología'
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    
    categoria = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Categoría'
    )
    
    es_critica = models.BooleanField(
        default=False,
        verbose_name='Patología Crítica',
        help_text='Indica si requiere atención inmediata'
    )
    
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['codigo_cie10']
        verbose_name = 'Patología'
        verbose_name_plural = 'Patologías'
```

---

## 🔗 URLs

```python
# medicoApp/urls.py
app_name = 'medico'

urlpatterns = [
    # Menú
    path('', views.menu_medico, name='menu_medico'),
    
    # Patologías
    path('patologias/', views.lista_patologias, name='lista_patologias'),
    path('patologia/crear/', views.crear_patologia, name='crear_patologia'),
    path('patologia/<int:pk>/', views.detalle_patologia, name='detalle_patologia'),
    path('patologia/<int:pk>/editar/', views.editar_patologia, name='editar_patologia'),
    
    # API
    path('api/buscar-patologia/', views.api_buscar_patologia, name='api_buscar_patologia'),
]
```

---

## 🖼️ Templates

```
templates/Medico/
├── menu_medico.html           # Menú principal
├── lista_patologias.html      # Lista de patologías
├── patologia_form.html        # Crear/editar patología
├── detalle_patologia.html     # Detalle de patología
└── Data/
    └── dashboard_medico.html  # Dashboard
```

---

## 📋 Patologías Obstétricas Comunes (CIE-10)

| Código | Nombre | Crítica |
|--------|--------|---------|
| O14.1 | Preeclampsia severa | ✅ |
| O15.0 | Eclampsia en el embarazo | ✅ |
| O85 | Sepsis puerperal | ✅ |
| O41.1 | Corioamnionitis | ✅ |
| O24.4 | Diabetes gestacional | ❌ |
| O13 | Hipertensión gestacional | ❌ |
| O36.4 | Muerte intrauterina | ✅ |
| O42.0 | Rotura prematura de membranas | ❌ |
| O60.0 | Trabajo de parto prematuro | ❌ |
| O72.0 | Hemorragia postparto | ✅ |

---

## 📊 Relación con Ficha Obstétrica

```python
# matronaApp/models.py
class FichaObstetrica(models.Model):
    # ...
    patologias = models.ManyToManyField(
        'medicoApp.Patologias',
        blank=True,
        related_name='fichas_obstetrica'
    )
    
    descripcion_patologias = models.TextField(
        blank=True,
        verbose_name='Descripción de Patologías'
    )
    
    patologias_criticas = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Patologías Críticas'
    )
```

---

## 📊 Diagrama de Relaciones

```
┌─────────────────┐
│   Patologias    │
│    (CIE-10)     │
└────────┬────────┘
         │
         │ ManyToMany
         ▼
┌─────────────────┐
│ FichaObstetrica │
└─────────────────┘
```

---

## 🔐 Permisos

| Acción | Médico | Matrona | TENS | Admin |
|--------|--------|---------|------|-------|
| Ver patologías | ✅ | ✅ | ❌ | ✅ |
| Crear patologías | ✅ | ❌ | ❌ | ✅ |
| Editar patologías | ✅ | ❌ | ❌ | ✅ |
| Asignar a ficha | ✅ | ✅ | ❌ | ✅ |

---

## 📌 Notas Importantes

1. **CIE-10**: Se utiliza la clasificación internacional estándar.
2. **Patologías Críticas**: Se marcan para alertar al personal.
3. **ManyToMany**: Una ficha puede tener múltiples patologías.
4. **Búsqueda**: API disponible para autocompletado.

---

*Documentación de medicoApp - OB_CARE v1.0*
