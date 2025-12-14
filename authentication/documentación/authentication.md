# 📁 inicioApp - Página Principal y Screensaver

## Descripción

La aplicación `inicioApp` gestiona la página principal del sistema, incluyendo la pantalla de descanso (screensaver) que se muestra cuando no hay usuario autenticado, y la redirección al dashboard correspondiente según el rol del usuario.

---

## 📋 Vistas

### home

```python
def home(request):
    """
    Vista principal de inicio
    - Si está autenticado → Redirige a su dashboard
    - Si NO está autenticado → Muestra pantalla de descanso/screensaver
    """
    # Si el usuario está autenticado, redirigir a su dashboard
    if request.user.is_authenticated:
        destino = get_dashboard_url_for_user(request.user)
        if destino:
            return redirect(destino)
    
    # Si NO está autenticado, mostrar pantalla de descanso
    ahora = timezone.now()

    context = {
        "pacientes_activos": Paciente.objects.filter(activo=True).count(),
        "medicos_activos": Medico.objects.filter(Activo=True).count(),
        "matronas_activas": Matrona.objects.filter(Activo=True).count(),
        "tens_activos": Tens.objects.filter(Activo=True).count(),
        "fecha_actual": ahora.strftime("%d de %B de %Y"),
        "hora_actual": ahora.strftime("%H:%M"),
    }

    return render(request, "screensaver.html", context)
```

---

## 🔗 URLs

```python
# inicioApp/urls.py
app_name = 'inicio'

urlpatterns = [
    path('', views.home, name='home'),
]
```

---

## 🖼️ Templates

### screensaver.html

Pantalla de descanso para terminales del hospital con:
- Logo del hospital
- Fecha y hora actual (actualización en tiempo real)
- Estadísticas del sistema
- Botón para iniciar sesión

```html
<!-- templates/screensaver.html -->
{% extends 'base.html' %}

{% block content %}
<div class="screensaver-container">
    <div class="hospital-logo">
        <img src="{% static 'img/logo_hospital.png' %}" alt="Hospital Herminda Martín">
    </div>
    
    <div class="clock" id="clock">
        {{ hora_actual }}
    </div>
    
    <div class="date">
        {{ fecha_actual }}
    </div>
    
    <div class="stats">
        <div class="stat-item">
            <span class="stat-number">{{ pacientes_activos }}</span>
            <span class="stat-label">Pacientes</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">{{ medicos_activos }}</span>
            <span class="stat-label">Médicos</span>
        </div>
    </div>
    
    <a href="{% url 'authentication:login' %}" class="btn-login">
        Iniciar Sesión
    </a>
</div>

<script>
// Actualizar reloj cada segundo
setInterval(function() {
    const now = new Date();
    document.getElementById('clock').textContent = 
        now.toLocaleTimeString('es-CL', {hour: '2-digit', minute: '2-digit'});
}, 1000);
</script>
{% endblock %}
```

---

## 📊 Flujo de Navegación

```
Usuario accede a /
        │
        ├── ¿Autenticado?
        │       │
        │       ├── SÍ → Obtener rol del usuario
        │       │           │
        │       │           ├── Admin → /admin/dashboard/
        │       │           ├── Médico → /medico/dashboard/
        │       │           ├── Matrona → /matrona/dashboard/
        │       │           └── TENS → /tens/dashboard/
        │       │
        │       └── NO → Mostrar screensaver.html
        │
        └── Click en "Iniciar Sesión" → /login/
```

---

## 📌 Notas

1. **Screensaver**: Ideal para terminales públicos del hospital.
2. **Auto-redirección**: Usuarios autenticados van directo a su dashboard.
3. **Estadísticas en vivo**: Muestra contadores actualizados.

---

---

# 📁 authentication - Sistema de Autenticación

## Descripción

La aplicación `authentication` gestiona todo el sistema de autenticación y autorización del sistema OB_CARE, incluyendo login, logout, dashboards por rol, decoradores de permisos y logging de accesos.

---

## 📋 Vistas

### CustomLoginView

```python
class CustomLoginView(LoginView):
    """Vista de login personalizada con logging"""
    
    template_name = 'authentication/login.html'
    
    def form_valid(self, form):
        # Logging de login exitoso
        logger.info(
            f"Login exitoso: {form.get_user().username} "
            f"desde IP: {self.get_client_ip()}"
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Logging de intento fallido
        logger.warning(
            f"Login fallido para usuario: {form.data.get('username')} "
            f"desde IP: {self.get_client_ip()}"
        )
        return super().form_invalid(form)
    
    def get_success_url(self):
        # Redirección según rol
        user = self.request.user
        return get_dashboard_url_for_user(user)
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return self.request.META.get('REMOTE_ADDR')
```

---

## 🔐 Decoradores de Permisos

### role_required

```python
def role_required(role_name):
    """
    Decorador que verifica si el usuario tiene un rol específico
    Uso: @role_required('medico')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login')
            
            if not user_has_role(request.user, role_name):
                messages.error(request, f'No tienes permisos de {role_name}')
                return redirect('inicio:home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### roles_required

```python
def roles_required(*role_names):
    """
    Decorador que verifica si el usuario tiene alguno de los roles
    Uso: @roles_required('medico', 'matrona')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login')
            
            for role in role_names:
                if user_has_role(request.user, role):
                    return view_func(request, *args, **kwargs)
            
            messages.error(request, 'No tienes permisos para esta acción')
            return redirect('inicio:home')
        return wrapper
    return decorator
```

---

## 🔧 Utilidades

### user_has_role

```python
def user_has_role(user, role_name):
    """Verifica si un usuario tiene un rol específico"""
    if user.is_superuser:
        return True
    return user.groups.filter(name__iexact=role_name).exists()
```

### get_dashboard_url_for_user

```python
ROLE_REDIRECT_MAP = {
    'administrador': 'gestion:dashboard_admin',
    'medico': 'gestion:dashboard_medico',
    'matrona': 'gestion:dashboard_matrona',
    'tens': 'gestion:dashboard_tens',
}

def get_dashboard_url_for_user(user):
    """Obtiene la URL del dashboard según el rol del usuario"""
    if user.is_superuser:
        return reverse('gestion:dashboard_admin')
    
    for role, url_name in ROLE_REDIRECT_MAP.items():
        if user_has_role(user, role):
            return reverse(url_name)
    
    return reverse('inicio:home')
```

---

## 🔗 URLs

```python
# authentication/urls.py
app_name = 'authentication'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='inicio:home'), name='logout'),
]
```

---

## 🖼️ Templates

```
templates/authentication/
├── login.html              # Página de login
└── logout.html             # Confirmación de logout (opcional)

templates/Gestion/Data/
├── dashboard_admin.html    # Dashboard administrador
├── dashboard_medico.html   # Dashboard médico
├── dashboard_matrona.html  # Dashboard matrona
└── dashboard_tens.html     # Dashboard TENS
```

### login.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="login-container">
    <div class="login-card">
        <div class="login-header">
            <img src="{% static 'img/logo.png' %}" alt="OB_CARE">
            <h1>Sistema de Trazabilidad Obstétrica</h1>
        </div>
        
        <form method="post" class="login-form">
            {% csrf_token %}
            
            <div class="form-group">
                <label for="username">Usuario</label>
                <input type="text" name="username" id="username" 
                       class="form-control" required autofocus>
            </div>
            
            <div class="form-group">
                <label for="password">Contraseña</label>
                <input type="password" name="password" id="password" 
                       class="form-control" required>
            </div>
            
            <button type="submit" class="btn btn-primary btn-block">
                Iniciar Sesión
            </button>
        </form>
        
        <div class="login-footer">
            <p>Hospital Clínico Herminda Martín</p>
            <p id="current-time"></p>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 👥 Grupos de Django

| Grupo | Permisos |
|-------|----------|
| `administrador` | Acceso total, gestión de usuarios |
| `medico` | Fichas, patologías, partos, medicamentos |
| `matrona` | Fichas obstétricas, control de parto |
| `tens` | Signos vitales, administración de medicamentos |

### Crear grupos (script)

```python
# utilidad/crear_usuarios_roles.py
from django.contrib.auth.models import Group

grupos = ['administrador', 'medico', 'matrona', 'tens']
for nombre in grupos:
    group, created = Group.objects.get_or_create(name=nombre)
    if created:
        print(f"Grupo creado: {nombre}")
```

---

## 📊 Matriz de Permisos

| Funcionalidad | Admin | Médico | Matrona | TENS |
|---------------|-------|--------|---------|------|
| Gestión de usuarios | ✅ | ❌ | ❌ | ❌ |
| Gestión de personas | ✅ | ✅ | ✅ | ❌ |
| Fichas obstétricas | ✅ | ✅ | ✅ | ❌ |
| Registro de parto | ✅ | ✅ | ✅ | ❌ |
| Registro RN | ✅ | ✅ | ✅ | ❌ |
| Signos vitales | ✅ | ❌ | ❌ | ✅ |
| Administrar medicamentos | ✅ | ❌ | ❌ | ✅ |
| Consulta legacy | ✅ | ✅ | ✅ | ❌ |

---

## 🛡️ Seguridad

| Aspecto | Implementación |
|---------|----------------|
| CSRF | Token en todos los formularios |
| Logging | IP + usuario en cada intento |
| Sesiones | Timeout configurable |
| Contraseñas | Hasheadas con PBKDF2 |

---

## 📌 Notas Importantes

1. **Superuser**: Tiene acceso a todo sin importar grupos.
2. **Grupos**: Un usuario puede pertenecer a múltiples grupos.
3. **Logging**: Todos los accesos quedan registrados.
4. **Redirección**: Automática según rol al iniciar sesión.

---

*Documentación de inicioApp y authentication - OB_CARE v1.0*
