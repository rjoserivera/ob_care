# 📁 tensApp - Signos Vitales y Tratamientos

## Descripción

La aplicación `tensApp` permite a los Técnicos en Enfermería de Nivel Superior (TENS) registrar signos vitales de las pacientes y documentar la aplicación de tratamientos/medicamentos.

---

## 📊 Modelos

### RegistroTens

```python
class RegistroTens(models.Model):
    """Registro de signos vitales por TENS"""
    
    # Relaciones
    ficha = models.ForeignKey('matronaApp.FichaObstetrica', on_delete=models.CASCADE, related_name='registros_tens')
    tens_responsable = models.ForeignKey('gestionApp.Tens', on_delete=models.PROTECT)
    
    # Fecha y turno
    fecha = models.DateField()
    turno = models.CharField(max_length=10)  # 'MAÑANA', 'TARDE', 'NOCHE'
    
    # Signos vitales
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1,
        null=True, blank=True,
        validators=[MinValueValidator(34.0), MaxValueValidator(42.0)]  # °C
    )
    
    frecuencia_cardiaca = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(200)]  # lpm
    )
    
    presion_arterial_sistolica = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(60), MaxValueValidator(250)]  # mmHg
    )
    
    presion_arterial_diastolica = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(150)]  # mmHg
    )
    
    frecuencia_respiratoria = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(8), MaxValueValidator(40)]  # rpm
    )
    
    saturacion_oxigeno = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(50), MaxValueValidator(100)]  # %
    )
    
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    @property
    def presion_arterial(self):
        """Retorna presión arterial en formato 120/80"""
        if self.presion_arterial_sistolica and self.presion_arterial_diastolica:
            return f"{self.presion_arterial_sistolica}/{self.presion_arterial_diastolica}"
        return "No registrada"
    
    class Meta:
        ordering = ['-fecha', '-fecha_registro']
        indexes = [
            models.Index(fields=['ficha', '-fecha']),
            models.Index(fields=['tens_responsable', '-fecha']),
        ]
```

### Tratamiento_aplicado

```python
class Tratamiento_aplicado(models.Model):
    """Registro de tratamientos/medicamentos aplicados por TENS"""
    
    # Relaciones
    ficha = models.ForeignKey('matronaApp.FichaObstetrica', on_delete=models.CASCADE, related_name='tratamientos_aplicados')
    paciente = models.ForeignKey('gestionApp.Paciente', on_delete=models.CASCADE, related_name='tratamientos_recibidos')
    tens = models.ForeignKey('gestionApp.Tens', on_delete=models.PROTECT, related_name='tratamientos_aplicados')
    medicamento_ficha = models.ForeignKey('matronaApp.MedicamentoFicha', on_delete=models.CASCADE)
    
    # Datos del tratamiento
    fecha_aplicacion = models.DateTimeField(default=timezone.now)
    dosis_aplicada = models.CharField(max_length=100)
    via_administracion = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True)
    
    # Control
    fecha_registro = models.DateTimeField(auto_now_add=True)
```

---

## 🔗 URLs

```python
# tensApp/urls.py
app_name = 'tens'

urlpatterns = [
    # Menú principal
    path('', views.menu_tens, name='menu_tens'),
    
    # Registros de signos vitales
    path('registro/<int:ficha_pk>/', views.registrar_signos_vitales, name='registrar_signos'),
    path('historial/<int:ficha_pk>/', views.historial_signos, name='historial_signos'),
    
    # Tratamientos
    path('tratamiento/<int:ficha_pk>/', views.registrar_tratamiento, name='registrar_tratamiento'),
]
```

---

## 🖼️ Templates

```
templates/Tens/
├── menu_tens.html              # Menú principal
├── registrar_signos.html       # Formulario de signos vitales
├── historial_signos.html       # Historial de registros
├── registrar_tratamiento.html  # Aplicar tratamiento
└── Data/
    └── dashboard_tens.html     # Dashboard
```

---

## 📋 Vistas Principales

### menu_tens
```python
def menu_tens(request):
    """Menú principal del módulo TENS"""
    hoy = timezone.now().date()
    
    administraciones_hoy = AdministracionMedicamento.objects.filter(
        fecha_hora_administracion__date=hoy
    ).count()
    
    context = {
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'total_fichas_activas': FichaObstetrica.objects.filter(activa=True).count(),
        'administraciones_hoy': administraciones_hoy,
    }
    return render(request, 'Tens/menu_tens.html', context)
```

---

## 📊 Rangos de Valores Normales

| Signo Vital | Mínimo | Máximo | Unidad |
|-------------|--------|--------|--------|
| Temperatura | 34.0 | 42.0 | °C |
| Frecuencia Cardíaca | 30 | 200 | lpm |
| Presión Sistólica | 60 | 250 | mmHg |
| Presión Diastólica | 30 | 150 | mmHg |
| Frecuencia Respiratoria | 8 | 40 | rpm |
| Saturación O2 | 50 | 100 | % |

---

## 📊 Flujo de Trabajo TENS

```
1. Seleccionar Paciente/Ficha
           ↓
2. Registrar Signos Vitales
   - Temperatura
   - Frecuencia cardíaca
   - Presión arterial
   - Saturación O2
           ↓
3. Verificar Medicamentos Pendientes
           ↓
4. Administrar Medicamento
   - Verificar indicación
   - Registrar hora
   - Documentar observaciones
           ↓
5. Confirmar Registro
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
┌─────────────────┐      ┌─────────────────┐
│  RegistroTens   │──────│      TENS       │
└─────────────────┘      └────────┬────────┘
                                  │
                                  │
┌─────────────────┐               │
│  Tratamiento    │───────────────┘
│    Aplicado     │
└────────┬────────┘
         │
         │ ForeignKey
         ▼
┌─────────────────┐
│MedicamentoFicha │
└─────────────────┘
```

---

## 🔐 Permisos

| Acción | TENS | Matrona | Médico | Admin |
|--------|------|---------|--------|-------|
| Ver fichas asignadas | ✅ | ✅ | ✅ | ✅ |
| Registrar signos vitales | ✅ | ❌ | ❌ | ✅ |
| Aplicar tratamientos | ✅ | ❌ | ❌ | ✅ |
| Ver historial | ✅ | ✅ | ✅ | ✅ |

---

## 📌 Notas Importantes

1. **Validadores**: Los signos vitales tienen rangos validados para detectar valores anómalos.
2. **Trazabilidad**: Cada registro queda asociado al TENS responsable.
3. **Turno**: Se registra el turno (mañana/tarde/noche) para seguimiento.
4. **Índices**: La BD tiene índices optimizados para búsquedas por ficha y fecha.

---

*Documentación de tensApp - OB_CARE v1.0*
