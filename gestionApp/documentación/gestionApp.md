## 📁 gestionApp - Gestión de Personas y Personal

## Descripción

La aplicación `gestionApp` es el núcleo del sistema OB_CARE. Gestiona todas las entidades de personas del sistema: pacientes, médicos, matronas y técnicos en enfermería (TENS).

---

## 📊 Modelos

### Catálogos Base

| Modelo | Campos | Descripción |
|--------|--------|-------------|
| `CatalogoSexo` | codigo, nombre, activo, orden | Sexo biológico |
| `CatalogoNacionalidad` | codigo, nombre, activo, orden | Nacionalidades |
| `CatalogoPuebloOriginario` | codigo, nombre, activo, orden | Pueblos originarios de Chile |
| `CatalogoEstadoCivil` | codigo, nombre, activo, orden | Estados civiles |
| `CatalogoPrevision` | codigo, nombre, descripcion, activo | Previsión de salud |
| `CatalogoTurno` | codigo, nombre, activo, orden | Turnos laborales |
| `CatalogoEspecialidad` | codigo, nombre, activo, orden | Especialidades médicas |
| `CatalogoNivelTens` | codigo, nombre, activo, orden | Niveles de TENS |
| `CatalogoCertificacion` | codigo, nombre, activo, orden | Certificaciones |

### Persona (Modelo Base)

```python
class Persona(models.Model):
    # Identificación
    Rut = models.CharField(max_length=100, unique=True, validators=[validar_rut_chileno])
    Nombre = models.CharField(max_length=100)
    Apellido_Paterno = models.CharField(max_length=100)
    Apellido_Materno = models.CharField(max_length=100)
    Fecha_nacimiento = models.DateField()
    
    # FK a catálogos
    Sexo = models.ForeignKey(CatalogoSexo, on_delete=models.PROTECT)
    Nacionalidad = models.ForeignKey(CatalogoNacionalidad, on_delete=models.PROTECT)
    Pueblos_originarios = models.ForeignKey(CatalogoPuebloOriginario, on_delete=models.PROTECT)
    
    # Condiciones especiales
    Inmigrante = models.BooleanField(default=False)
    Discapacidad = models.BooleanField(default=False)
    Tipo_de_Discapacidad = models.CharField(max_length=200, blank=True)
    Privada_de_Libertad = models.BooleanField(default=False)
    Trans_Masculino = models.BooleanField(default=False)
    
    # Contacto
    Telefono = models.CharField(max_length=100)
    Direccion = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Activo = models.BooleanField(default=True)
```

### Paciente

```python
class Paciente(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, primary_key=True)
    
    # FK a catálogos
    Estado_civil = models.ForeignKey(CatalogoEstadoCivil, on_delete=models.PROTECT)
    Previcion = models.ForeignKey(CatalogoPrevision, on_delete=models.PROTECT)
    
    # Datos clínicos
    paridad = models.CharField(max_length=50)
    Ductus_Venosus = models.CharField(max_length=70)
    control_prenatal = models.BooleanField(default=False)
    Consultorio = models.CharField(max_length=100)
    
    # Patologías
    Preeclampsia_Severa = models.BooleanField(default=False)
    Eclampsia = models.BooleanField(default=False)
    Sepsis_o_Infeccion_SiST = models.BooleanField(default=False)
    Infeccion_Ovular_o_Corioamnionitis = models.BooleanField(default=False)
    
    # Acompañamiento
    Acompañante = models.CharField(max_length=120)
    Contacto_emergencia = models.CharField(max_length=30)
    Fecha_y_Hora_Ingreso = models.DateTimeField()
    activo = models.BooleanField(default=True)
```

### Medico

```python
class Medico(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    Especialidad = models.ForeignKey(CatalogoEspecialidad, on_delete=models.PROTECT)
    Registro_medico = models.CharField(max_length=100, unique=True)
    Años_experiencia = models.IntegerField()
    Turno = models.ForeignKey(CatalogoTurno, on_delete=models.PROTECT)
    Activo = models.BooleanField(default=True)
```

### Matrona

```python
class Matrona(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    Especialidad = models.ForeignKey(CatalogoEspecialidad, on_delete=models.PROTECT)
    Registro_medico = models.CharField(max_length=100, unique=True)
    Años_experiencia = models.IntegerField()
    Turno = models.ForeignKey(CatalogoTurno, on_delete=models.PROTECT)
    Activo = models.BooleanField(default=True)
```

### Tens

```python
class Tens(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    Nivel = models.ForeignKey(CatalogoNivelTens, on_delete=models.PROTECT)
    Años_experiencia = models.IntegerField()
    Turno = models.ForeignKey(CatalogoTurno, on_delete=models.PROTECT)
    Certificaciones = models.ForeignKey(CatalogoCertificacion, on_delete=models.PROTECT)
    Activo = models.BooleanField(default=True)
```

---

## 🔗 URLs

```python
# gestionApp/urls.py
app_name = 'gestion'

urlpatterns = [
    # PERSONAS
    path('registrar-persona/', views.registrar_persona, name='registrar_persona'),
    path('persona/<int:pk>/', views.detalle_persona, name='detalle_persona'),
    path('persona/<int:pk>/editar/', views.editar_persona, name='editar_persona'),
    path('persona/<int:pk>/desactivar/', views.desactivar_persona, name='desactivar_persona'),
    path('persona/<int:pk>/activar/', views.activar_persona, name='activar_persona'),
    path('personas/', views.persona_list, name='persona_list'),
    path('buscar-persona/', views.buscar_persona, name='buscar_persona'),
    
    # API
    path('api/buscar-persona/', views.api_buscar_persona, name='api_buscar_persona'),
]
```

---

## 📝 Formularios

| Formulario | Modelo | Descripción |
|------------|--------|-------------|
| `PersonaForm` | Persona | Registro y edición de personas |
| `BuscarPersonaForm` | - | Búsqueda por RUT |
| `PacienteForm` | Paciente | Datos adicionales del paciente |
| `MedicoForm` | Medico | Registro de médicos |
| `MatronaForm` | Matrona | Registro de matronas |
| `TensForm` | Tens | Registro de TENS |

---

## 🔐 Validadores

### Validación de RUT Chileno

```python
from utilidad.rut_validator import validar_rut_chileno, RutValidator

# Uso en modelo
Rut = models.CharField(validators=[validar_rut_chileno])

# Uso manual
rut = "12345678-5"
if RutValidator.validar(rut):
    print("RUT válido")

# Calcular dígito verificador
dv = RutValidator.calcular_dv("12345678")  # Retorna "5"
```

---

## 🖼️ Templates

```
templates/Gestion/
├── Formularios/
│   ├── persona_form.html      # Formulario de persona
│   ├── paciente_form.html     # Formulario de paciente
│   ├── medico_form.html       # Formulario de médico
│   ├── matrona_form.html      # Formulario de matrona
│   └── tens_form.html         # Formulario de TENS
├── Data/
│   ├── dashboard_admin.html   # Dashboard administrador
│   └── persona_list.html      # Lista de personas
└── gestionar_roles.html       # Asignación de roles
```

---

## 📊 Diagrama de Relaciones

```
┌─────────────┐
│   Persona   │
└──────┬──────┘
       │
       │ OneToOne
       │
┌──────┴──────┬──────────────┬──────────────┐
│             │              │              │
▼             ▼              ▼              ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Paciente │ │ Medico  │ │ Matrona │ │  Tens   │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
     │           │           │           │
     │           │           │           │
     ▼           ▼           ▼           ▼
┌────────────────────────────────────────────┐
│           Catálogos Normalizados           │
│ (Sexo, Nacionalidad, Turno, Especialidad)  │
└────────────────────────────────────────────┘
```

---

## 🛠️ Administración Django

```python
# gestionApp/admin.py
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['Rut', 'Nombre', 'Apellido_Paterno', 'Sexo', 'Activo']
    list_filter = ['Activo', 'Sexo', 'Nacionalidad']
    search_fields = ['Rut', 'Nombre', 'Apellido_Paterno']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('Rut', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno')
        }),
        ('Datos Personales', {
            'fields': ('Fecha_nacimiento', 'Sexo', 'Nacionalidad')
        }),
        # ...
    )
```

---

## 🧪 Tests

```python
# Casos de prueba relacionados
class TestFuncionalidadesCore:
    def test_registro_persona_valida(self):
        """CP-001: Registro exitoso de persona"""
        
    def test_rut_invalido(self):
        """CP-002: Rechazo de RUT inválido"""
        
    def test_persona_duplicada(self):
        """CP-003: Rechazo de persona duplicada"""
        
    def test_campos_obligatorios(self):
        """CP-004: Validación de campos obligatorios"""
        
    def test_formato_rut(self):
        """CP-005: Normalización de formato RUT"""
```

---

## 📌 Notas Importantes

1. **RUT Único**: El RUT es la clave principal para identificar personas, no puede duplicarse.
2. **Herencia**: Paciente, Médico, Matrona y TENS heredan de Persona mediante `OneToOneField`.
3. **Catálogos**: Se usan FK en lugar de CHOICES para permitir mantenimiento sin modificar código.
4. **Soft Delete**: Se usa `activo=False` en lugar de eliminar registros.

---

*Documentación de gestionApp - OB_CARE v1.0*
