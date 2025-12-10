# 🏠 inicioApp

## Autenticación y Página de Inicio

La app `inicioApp` gestiona la autenticación de usuarios, la página de inicio con screensaver institucional, y la redirección a dashboards según el rol del usuario.

---

## 📋 Tabla de Contenidos

1. [Descripción General](#1-descripción-general)
2. [Modelos](#2-modelos)
3. [URLs](#3-urls)
4. [Vistas](#4-vistas)
5. [Formularios](#5-formularios)
6. [Utilidades de Autenticación](#6-utilidades-de-autenticación)
7. [Templates](#7-templates)
8. [Screensaver Institucional](#8-screensaver-institucional)
9. [Dashboards por Rol](#9-dashboards-por-rol)
10. [Seguridad](#10-seguridad)
11. [Configuración de Grupos](#11-configuración-de-grupos)
12. [Signals](#12-signals)
13. [Tests](#13-tests)

---

## 1. Descripción General

### Propósito

`inicioApp` es la puerta de entrada al sistema OB_CARE:

- **Screensaver institucional**: Pantalla atractiva para usuarios no autenticados
- **Login personalizado**: Autenticación con registro de IP y redirección por rol
- **Dashboards diferenciados**: Cada rol ve información relevante a sus funciones
- **Gestión de sesiones**: Control de sesiones activas y timeout

### Responsabilidades

| Responsabilidad | Descripción |
|-----------------|-------------|
| Autenticación | Login/logout de usuarios |
| Screensaver | Pantalla institucional con reloj y estadísticas |
| Redirección | Enviar a dashboard según rol del usuario |
| Registro de accesos | Log de IPs y horarios de login |
| Gestión de sesiones | Timeout, sesiones activas |

---

## 2. Modelos

### 2.1 RegistroAcceso

```python
# inicioApp/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RegistroAcceso(models.Model):
    """
    Registro de todos los accesos al sistema.
    Permite auditoría de logins y detección de anomalías.
    """
    
    TIPO_CHOICES = [
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('LOGIN_FALLIDO', 'Intento Fallido'),
        ('SESION_EXPIRADA', 'Sesión Expirada'),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registros_acceso',
        null=True,
        blank=True,
        verbose_name="Usuario"
    )
    
    username_intento = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Username Intentado",
        help_text="Para registrar intentos fallidos"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Acceso"
    )
    
    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y Hora"
    )
    
    ip_address = models.GenericIPAddressField(
        verbose_name="Dirección IP"
    )
    
    user_agent = models.TextField(
        blank=True,
        verbose_name="User Agent"
    )
    
    exitoso = models.BooleanField(
        default=True,
        verbose_name="Exitoso"
    )
    
    motivo_fallo = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Motivo del Fallo"
    )
    
    class Meta:
        verbose_name = "Registro de Acceso"
        verbose_name_plural = "Registros de Acceso"
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['usuario', '-fecha_hora']),
            models.Index(fields=['ip_address', '-fecha_hora']),
            models.Index(fields=['tipo', '-fecha_hora']),
        ]
    
    def __str__(self):
        usuario = self.usuario.username if self.usuario else self.username_intento
        return f"{self.tipo} - {usuario} - {self.fecha_hora}"


class SesionActiva(models.Model):
    """
    Registro de sesiones activas para control y monitoreo.
    """
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sesiones_activas',
        verbose_name="Usuario"
    )
    
    session_key = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="Clave de Sesión"
    )
    
    ip_address = models.GenericIPAddressField(
        verbose_name="Dirección IP"
    )
    
    user_agent = models.TextField(
        blank=True,
        verbose_name="User Agent"
    )
    
    inicio = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Inicio de Sesión"
    )
    
    ultima_actividad = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actividad"
    )
    
    class Meta:
        verbose_name = "Sesión Activa"
        verbose_name_plural = "Sesiones Activas"
        ordering = ['-ultima_actividad']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.ip_address}"
    
    @property
    def duracion(self):
        """Duración de la sesión en minutos"""
        delta = timezone.now() - self.inicio
        return int(delta.total_seconds() / 60)


class ConfiguracionPantalla(models.Model):
    """
    Configuración del screensaver y pantalla de inicio.
    """
    
    titulo = models.CharField(
        max_length=200,
        default="Sistema de Gestión Obstétrica",
        verbose_name="Título"
    )
    
    subtitulo = models.CharField(
        max_length=200,
        default="Hospital Clínico Herminda Martín",
        verbose_name="Subtítulo"
    )
    
    mensaje_bienvenida = models.TextField(
        default="Bienvenido al sistema OB-CARE",
        verbose_name="Mensaje de Bienvenida"
    )
    
    mostrar_estadisticas = models.BooleanField(
        default=True,
        verbose_name="Mostrar Estadísticas"
    )
    
    mostrar_reloj = models.BooleanField(
        default=True,
        verbose_name="Mostrar Reloj"
    )
    
    imagen_fondo = models.ImageField(
        upload_to='screensaver/',
        blank=True,
        null=True,
        verbose_name="Imagen de Fondo"
    )
    
    logo = models.ImageField(
        upload_to='screensaver/',
        blank=True,
        null=True,
        verbose_name="Logo"
    )
    
    tiempo_inactividad = models.PositiveIntegerField(
        default=300,
        verbose_name="Tiempo de Inactividad (seg)",
        help_text="Segundos antes de mostrar screensaver"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Configuración de Pantalla"
        verbose_name_plural = "Configuraciones de Pantalla"
    
    def __str__(self):
        return f"Configuración: {self.titulo}"
    
    @classmethod
    def get_activa(cls):
        """Obtiene la configuración activa"""
        return cls.objects.filter(activo=True).first()
```

---

## 3. URLs

```python
# inicioApp/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'inicio'

urlpatterns = [
    # ═══════════════════════════════════════════════════════════════
    # PÁGINA DE INICIO
    # ═══════════════════════════════════════════════════════════════
    path('', views.home, name='home'),
    path('screensaver/', views.screensaver, name='screensaver'),
    
    # ═══════════════════════════════════════════════════════════════
    # AUTENTICACIÓN
    # ═══════════════════════════════════════════════════════════════
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    # ═══════════════════════════════════════════════════════════════
    # DASHBOARDS POR ROL
    # ═══════════════════════════════════════════════════════════════
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/medico/', views.dashboard_medico, name='dashboard_medico'),
    path('dashboard/matrona/', views.dashboard_matrona, name='dashboard_matrona'),
    path('dashboard/tens/', views.dashboard_tens, name='dashboard_tens'),
    path('dashboard/coordinador/', views.dashboard_coordinador, name='dashboard_coordinador'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    
    # ═══════════════════════════════════════════════════════════════
    # PERFIL Y CONFIGURACIÓN
    # ═══════════════════════════════════════════════════════════════
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    
    # ═══════════════════════════════════════════════════════════════
    # API (AJAX)
    # ═══════════════════════════════════════════════════════════════
    path('api/estadisticas/', views.api_estadisticas, name='api_estadisticas'),
    path('api/sesion/renovar/', views.api_renovar_sesion, name='api_renovar_sesion'),
]
```

---

## 4. Vistas

### 4.1 Vistas Principales

```python
# inicioApp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

from .models import RegistroAcceso, SesionActiva, ConfiguracionPantalla
from .utils import get_client_ip, get_dashboard_url_for_user, registrar_acceso


def home(request):
    """
    Página de inicio.
    - Si no está autenticado: muestra screensaver
    - Si está autenticado: redirige a dashboard
    """
    
    if request.user.is_authenticated:
        return redirect('inicio:dashboard')
    
    return redirect('inicio:screensaver')


def screensaver(request):
    """
    Pantalla de screensaver institucional.
    Muestra reloj, estadísticas y botón de login.
    """
    
    config = ConfiguracionPantalla.get_activa()
    
    # Estadísticas del día
    from gestionProcesosApp.models import ProcesoParto
    from recienNacidoApp.models import RegistroRecienNacido
    
    hoy = timezone.now().date()
    
    estadisticas = {
        'partos_hoy': ProcesoParto.objects.filter(
            hora_nacimiento__date=hoy
        ).count(),
        'nacimientos_hoy': RegistroRecienNacido.objects.filter(
            created_at__date=hoy
        ).count(),
        'procesos_activos': ProcesoParto.objects.filter(
            estado__codigo__in=['INICIADO', 'CONFIRMADO', 'EN_CURSO']
        ).count(),
    }
    
    return render(request, 'inicioApp/screensaver.html', {
        'config': config,
        'estadisticas': estadisticas,
        'hospital': settings.HOSPITAL_CONFIG,
    })


class CustomLoginView(LoginView):
    """
    Vista de login personalizada con registro de IP y redirección por rol.
    """
    
    template_name = 'inicioApp/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Login exitoso"""
        response = super().form_valid(form)
        
        # Registrar acceso exitoso
        registrar_acceso(
            request=self.request,
            usuario=self.request.user,
            tipo='LOGIN',
            exitoso=True
        )
        
        # Crear sesión activa
        SesionActiva.objects.create(
            usuario=self.request.user,
            session_key=self.request.session.session_key,
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.success(
            self.request,
            f'Bienvenido/a, {self.request.user.get_full_name() or self.request.user.username}'
        )
        
        return response
    
    def form_invalid(self, form):
        """Login fallido"""
        username = form.cleaned_data.get('username', '')
        
        registrar_acceso(
            request=self.request,
            usuario=None,
            tipo='LOGIN_FALLIDO',
            exitoso=False,
            username_intento=username,
            motivo='Credenciales inválidas'
        )
        
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        
        return super().form_invalid(form)
    
    def get_success_url(self):
        """Redirige según el rol del usuario"""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        
        return get_dashboard_url_for_user(self.request.user)


def custom_logout(request):
    """
    Logout personalizado con registro de cierre de sesión.
    """
    
    if request.user.is_authenticated:
        # Registrar logout
        registrar_acceso(
            request=request,
            usuario=request.user,
            tipo='LOGOUT',
            exitoso=True
        )
        
        # Eliminar sesión activa
        SesionActiva.objects.filter(
            session_key=request.session.session_key
        ).delete()
        
        username = request.user.username
        logout(request)
        
        messages.info(request, f'Sesión cerrada correctamente. Hasta pronto, {username}.')
    
    return redirect('inicio:screensaver')


@login_required
def dashboard_redirect(request):
    """
    Redirige al dashboard correspondiente según el rol del usuario.
    """
    
    url = get_dashboard_url_for_user(request.user)
    return redirect(url)


@login_required
def dashboard_medico(request):
    """Dashboard específico para médicos"""
    
    from gestionProcesosApp.models import ProcesoParto
    
    # Procesos donde el médico es responsable
    mis_procesos = ProcesoParto.objects.filter(
        medico_responsable=request.user,
        estado__codigo__in=['EN_CURSO', 'CONFIRMADO']
    )
    
    # Procesos activos generales
    procesos_activos = ProcesoParto.objects.filter(
        estado__codigo__in=['INICIADO', 'CONFIRMADO', 'EN_CURSO']
    ).select_related('ficha_obstetrica__paciente', 'sala', 'estado')
    
    # Estadísticas del día
    hoy = timezone.now().date()
    partos_hoy = ProcesoParto.objects.filter(
        hora_nacimiento__date=hoy,
        medico_responsable=request.user
    ).count()
    
    return render(request, 'inicioApp/dashboard_medico.html', {
        'mis_procesos': mis_procesos,
        'procesos_activos': procesos_activos,
        'partos_hoy': partos_hoy,
    })


@login_required
def dashboard_matrona(request):
    """Dashboard específico para matronas"""
    
    from gestionProcesosApp.models import ProcesoParto, ConfirmacionPersonal
    from matronaApp.models import FichaObstetrica
    
    # Confirmaciones pendientes
    confirmaciones_pendientes = ConfirmacionPersonal.objects.filter(
        profesional=request.user,
        confirmado=False
    ).select_related('proceso')
    
    # Fichas obstétricas activas
    fichas_activas = FichaObstetrica.objects.filter(
        estado='ACTIVA'
    ).select_related('paciente').order_by('-created_at')[:10]
    
    # Pacientes próximas a 8cm
    fichas_proximas = FichaObstetrica.objects.filter(
        estado='ACTIVA',
        dilatacion_actual__gte=6,
        dilatacion_actual__lt=8
    ).select_related('paciente')
    
    # Procesos activos
    procesos_activos = ProcesoParto.objects.filter(
        estado__codigo__in=['INICIADO', 'CONFIRMADO', 'EN_CURSO']
    )
    
    return render(request, 'inicioApp/dashboard_matrona.html', {
        'confirmaciones_pendientes': confirmaciones_pendientes,
        'fichas_activas': fichas_activas,
        'fichas_proximas': fichas_proximas,
        'procesos_activos': procesos_activos,
    })


@login_required
def dashboard_tens(request):
    """Dashboard específico para TENS"""
    
    from gestionProcesosApp.models import ProcesoParto, ConfirmacionPersonal
    from tensApp.models import RegistroTens
    
    # Confirmaciones pendientes
    confirmaciones_pendientes = ConfirmacionPersonal.objects.filter(
        profesional=request.user,
        confirmado=False
    ).select_related('proceso')
    
    # Mis registros del día
    hoy = timezone.now().date()
    mis_registros_hoy = RegistroTens.objects.filter(
        registrado_por=request.user,
        created_at__date=hoy
    ).count()
    
    # Procesos donde estoy asignado
    from gestionProcesosApp.models import AsignacionPersonal
    mis_asignaciones = AsignacionPersonal.objects.filter(
        profesional=request.user,
        proceso__estado__codigo__in=['EN_CURSO', 'CONFIRMADO'],
        activo=True
    ).select_related('proceso', 'proceso__sala')
    
    return render(request, 'inicioApp/dashboard_tens.html', {
        'confirmaciones_pendientes': confirmaciones_pendientes,
        'mis_registros_hoy': mis_registros_hoy,
        'mis_asignaciones': mis_asignaciones,
    })


@login_required
def dashboard_coordinador(request):
    """Dashboard específico para coordinadores"""
    
    from gestionProcesosApp.models import ProcesoParto, SalaParto
    
    # Estado de salas
    salas = SalaParto.objects.all().select_related('estado', 'proceso_actual')
    
    # Procesos activos
    procesos_activos = ProcesoParto.objects.filter(
        estado__codigo__in=['INICIADO', 'CONFIRMADO', 'EN_CURSO']
    ).select_related('ficha_obstetrica__paciente', 'sala', 'estado', 'prioridad')
    
    # Estadísticas del día
    hoy = timezone.now().date()
    estadisticas = {
        'procesos_iniciados_hoy': ProcesoParto.objects.filter(
            hora_inicio_proceso__date=hoy
        ).count(),
        'procesos_finalizados_hoy': ProcesoParto.objects.filter(
            hora_cronometro_fin__date=hoy
        ).count(),
        'salas_disponibles': salas.filter(estado__codigo='DISPONIBLE').count(),
        'salas_ocupadas': salas.filter(estado__codigo='OCUPADA').count(),
    }
    
    return render(request, 'inicioApp/dashboard_coordinador.html', {
        'salas': salas,
        'procesos_activos': procesos_activos,
        'estadisticas': estadisticas,
    })


@login_required
def dashboard_admin(request):
    """Dashboard de administración"""
    
    from django.contrib.auth.models import User
    from gestionProcesosApp.models import ProcesoParto
    
    # Usuarios activos
    usuarios_activos = SesionActiva.objects.all().select_related('usuario')
    
    # Estadísticas generales
    estadisticas = {
        'usuarios_total': User.objects.filter(is_active=True).count(),
        'usuarios_conectados': usuarios_activos.count(),
        'procesos_total': ProcesoParto.objects.count(),
        'accesos_hoy': RegistroAcceso.objects.filter(
            fecha_hora__date=timezone.now().date()
        ).count(),
    }
    
    # Últimos accesos
    ultimos_accesos = RegistroAcceso.objects.all()[:20]
    
    return render(request, 'inicioApp/dashboard_admin.html', {
        'usuarios_activos': usuarios_activos,
        'estadisticas': estadisticas,
        'ultimos_accesos': ultimos_accesos,
    })


@login_required
def perfil_usuario(request):
    """Vista de perfil del usuario"""
    
    # Historial de accesos
    historial_accesos = RegistroAcceso.objects.filter(
        usuario=request.user
    )[:10]
    
    # Sesiones activas
    sesiones = SesionActiva.objects.filter(usuario=request.user)
    
    return render(request, 'inicioApp/perfil.html', {
        'historial_accesos': historial_accesos,
        'sesiones': sesiones,
    })


@login_required
def cambiar_password(request):
    """Vista para cambiar contraseña"""
    
    from django.contrib.auth.forms import PasswordChangeForm
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('inicio:perfil')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'inicioApp/cambiar_password.html', {
        'form': form,
    })


# ═══════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

def api_estadisticas(request):
    """API para obtener estadísticas en tiempo real (screensaver)"""
    
    from gestionProcesosApp.models import ProcesoParto
    from recienNacidoApp.models import RegistroRecienNacido
    
    hoy = timezone.now().date()
    
    data = {
        'partos_hoy': ProcesoParto.objects.filter(
            hora_nacimiento__date=hoy
        ).count(),
        'nacimientos_hoy': RegistroRecienNacido.objects.filter(
            created_at__date=hoy
        ).count(),
        'procesos_activos': ProcesoParto.objects.filter(
            estado__codigo__in=['INICIADO', 'CONFIRMADO', 'EN_CURSO']
        ).count(),
        'hora_servidor': timezone.now().strftime('%H:%M:%S'),
        'fecha_servidor': timezone.now().strftime('%d/%m/%Y'),
    }
    
    return JsonResponse(data)


@login_required
def api_renovar_sesion(request):
    """API para renovar sesión y evitar timeout"""
    
    # Actualizar última actividad
    SesionActiva.objects.filter(
        session_key=request.session.session_key
    ).update(ultima_actividad=timezone.now())
    
    return JsonResponse({'success': True, 'message': 'Sesión renovada'})
```

---

## 5. Formularios

```python
# inicioApp/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class CustomAuthenticationForm(AuthenticationForm):
    """Formulario de login personalizado"""
    
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese su usuario',
            'autofocus': True,
        })
    )
    
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese su contraseña',
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        label="Recordar sesión",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulario de cambio de contraseña personalizado"""
    
    old_password = forms.CharField(
        label="Contraseña Actual",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña actual',
        })
    )
    
    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña',
        })
    )
    
    new_password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme nueva contraseña',
        })
    )
```

---

## 6. Utilidades de Autenticación

```python
# inicioApp/utils.py

from django.urls import reverse


def get_client_ip(request):
    """Obtiene la IP real del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def get_dashboard_url_for_user(user):
    """
    Retorna la URL del dashboard según el rol del usuario.
    """
    
    ROLE_REDIRECT_MAP = {
        'administrador': 'inicio:dashboard_admin',
        'coordinador': 'inicio:dashboard_coordinador',
        'medico': 'inicio:dashboard_medico',
        'matrona': 'inicio:dashboard_matrona',
        'tens': 'inicio:dashboard_tens',
    }
    
    if user.is_superuser:
        return reverse('inicio:dashboard_admin')
    
    # Obtener roles del usuario
    roles = list(user.groups.values_list('name', flat=True))
    
    # Buscar el primer rol que coincida (en orden de prioridad)
    for role, url_name in ROLE_REDIRECT_MAP.items():
        if role in roles:
            return reverse(url_name)
    
    # Por defecto, redirigir al home
    return reverse('inicio:home')


def user_has_role(user, role):
    """Verifica si el usuario tiene un rol específico"""
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    return user.groups.filter(name=role).exists()


def user_has_any_role(user, roles):
    """Verifica si el usuario tiene alguno de los roles"""
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    return user.groups.filter(name__in=roles).exists()


def registrar_acceso(request, usuario, tipo, exitoso=True, username_intento='', motivo=''):
    """Registra un acceso en el sistema"""
    from .models import RegistroAcceso
    
    RegistroAcceso.objects.create(
        usuario=usuario,
        username_intento=username_intento,
        tipo=tipo,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        exitoso=exitoso,
        motivo_fallo=motivo
    )
```

---

## 7. Templates

### 7.1 Estructura de Templates

```
inicioApp/
└── templates/
    └── inicioApp/
        ├── base_auth.html
        ├── screensaver.html
        ├── login.html
        ├── perfil.html
        ├── cambiar_password.html
        ├── dashboard_medico.html
        ├── dashboard_matrona.html
        ├── dashboard_tens.html
        ├── dashboard_coordinador.html
        ├── dashboard_admin.html
        └── partials/
            ├── _stats_card.html
            ├── _proceso_card.html
            └── _confirmacion_alert.html
```

### 7.2 Template del Screensaver

```html
<!-- inicioApp/templates/inicioApp/screensaver.html -->

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ config.titulo }} | {{ hospital.NOMBRE }}</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    
    <style>
        body {
            background: linear-gradient(135deg, #1a237e 0%, #0d47a1 50%, #01579b 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .screensaver-container {
            text-align: center;
            padding: 2rem;
        }
        
        .logo {
            max-width: 150px;
            margin-bottom: 2rem;
        }
        
        .reloj {
            font-size: 5rem;
            font-weight: 300;
            letter-spacing: 0.1em;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        }
        
        .fecha {
            font-size: 1.5rem;
            opacity: 0.8;
            margin-bottom: 2rem;
        }
        
        .titulo {
            font-size: 2.5rem;
            font-weight: 300;
            margin-bottom: 0.5rem;
        }
        
        .subtitulo {
            font-size: 1.2rem;
            opacity: 0.7;
            margin-bottom: 3rem;
        }
        
        .stats-container {
            display: flex;
            justify-content: center;
            gap: 3rem;
            margin-bottom: 3rem;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.7;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        
        .btn-login {
            padding: 1rem 3rem;
            font-size: 1.2rem;
            border-radius: 50px;
            background: rgba(255,255,255,0.2);
            border: 2px solid white;
            color: white;
            transition: all 0.3s ease;
        }
        
        .btn-login:hover {
            background: white;
            color: #1a237e;
        }
        
        .hospital-info {
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0.6;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="screensaver-container">
        {% if config.logo %}
            <img src="{{ config.logo.url }}" alt="Logo" class="logo">
        {% else %}
            <i class="bi bi-heart-pulse" style="font-size: 5rem; margin-bottom: 1rem;"></i>
        {% endif %}
        
        <div class="reloj" id="reloj">--:--:--</div>
        <div class="fecha" id="fecha">--</div>
        
        <h1 class="titulo">{{ config.titulo|default:"Sistema de Gestión Obstétrica" }}</h1>
        <p class="subtitulo">{{ config.subtitulo|default:hospital.NOMBRE }}</p>
        
        {% if config.mostrar_estadisticas %}
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number" id="partos-hoy">{{ estadisticas.partos_hoy }}</div>
                <div class="stat-label">Partos Hoy</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" id="nacimientos-hoy">{{ estadisticas.nacimientos_hoy }}</div>
                <div class="stat-label">Nacimientos</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" id="procesos-activos">{{ estadisticas.procesos_activos }}</div>
                <div class="stat-label">Procesos Activos</div>
            </div>
        </div>
        {% endif %}
        
        <a href="{% url 'inicio:login' %}" class="btn btn-login">
            <i class="bi bi-box-arrow-in-right me-2"></i>
            Iniciar Sesión
        </a>
    </div>
    
    <div class="hospital-info">
        {{ hospital.NOMBRE }} | {{ hospital.CIUDAD }}, {{ hospital.REGION }}
    </div>
    
    <script>
        // Actualizar reloj
        function actualizarReloj() {
            const ahora = new Date();
            const horas = String(ahora.getHours()).padStart(2, '0');
            const minutos = String(ahora.getMinutes()).padStart(2, '0');
            const segundos = String(ahora.getSeconds()).padStart(2, '0');
            
            document.getElementById('reloj').textContent = `${horas}:${minutos}:${segundos}`;
            
            const opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            document.getElementById('fecha').textContent = ahora.toLocaleDateString('es-CL', opciones);
        }
        
        actualizarReloj();
        setInterval(actualizarReloj, 1000);
        
        // Actualizar estadísticas cada 30 segundos
        function actualizarEstadisticas() {
            fetch('{% url "inicio:api_estadisticas" %}')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('partos-hoy').textContent = data.partos_hoy;
                    document.getElementById('nacimientos-hoy').textContent = data.nacimientos_hoy;
                    document.getElementById('procesos-activos').textContent = data.procesos_activos;
                })
                .catch(error => console.error('Error:', error));
        }
        
        setInterval(actualizarEstadisticas, 30000);
    </script>
</body>
</html>
```

### 7.3 Template de Login

```html
<!-- inicioApp/templates/inicioApp/login.html -->

{% extends 'inicioApp/base_auth.html' %}

{% block auth_content %}
<div class="login-container">
    <div class="login-card">
        <div class="text-center mb-4">
            <i class="bi bi-heart-pulse text-primary" style="font-size: 3rem;"></i>
            <h2 class="mt-3">OB-CARE</h2>
            <p class="text-muted">Sistema de Gestión Obstétrica</p>
        </div>
        
        <form method="post" id="login-form">
            {% csrf_token %}
            
            <div class="mb-3">
                <label for="id_username" class="form-label">Usuario</label>
                <div class="input-group">
                    <span class="input-group-text">
                        <i class="bi bi-person"></i>
                    </span>
                    <input type="text" 
                           name="username" 
                           id="id_username" 
                           class="form-control form-control-lg"
                           placeholder="Ingrese su usuario"
                           autofocus
                           required>
                </div>
            </div>
            
            <div class="mb-4">
                <label for="id_password" class="form-label">Contraseña</label>
                <div class="input-group">
                    <span class="input-group-text">
                        <i class="bi bi-lock"></i>
                    </span>
                    <input type="password" 
                           name="password" 
                           id="id_password" 
                           class="form-control form-control-lg"
                           placeholder="Ingrese su contraseña"
                           required>
                    <button class="btn btn-outline-secondary" type="button" id="toggle-password">
                        <i class="bi bi-eye"></i>
                    </button>
                </div>
            </div>
            
            <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg">
                    <i class="bi bi-box-arrow-in-right me-2"></i>
                    Iniciar Sesión
                </button>
            </div>
        </form>
        
        <div class="text-center mt-4">
            <a href="{% url 'inicio:screensaver' %}" class="text-muted">
                <i class="bi bi-arrow-left me-1"></i>
                Volver al inicio
            </a>
        </div>
    </div>
</div>

<script>
    // Toggle mostrar/ocultar contraseña
    document.getElementById('toggle-password').addEventListener('click', function() {
        const passwordInput = document.getElementById('id_password');
        const icon = this.querySelector('i');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        } else {
            passwordInput.type = 'password';
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    });
</script>
{% endblock %}
```

---

## 8. Screensaver Institucional

### 8.1 Características

| Característica | Descripción |
|----------------|-------------|
| **Reloj en tiempo real** | Actualización cada segundo |
| **Fecha formateada** | En español, formato largo |
| **Estadísticas del día** | Partos, nacimientos, procesos activos |
| **Auto-actualización** | Estadísticas cada 30 segundos |
| **Diseño responsive** | Adaptable a diferentes pantallas |
| **Branding institucional** | Logo, colores, nombre del hospital |

### 8.2 API de Estadísticas

```python
# Endpoint: GET /api/estadisticas/
# Respuesta:
{
    "partos_hoy": 5,
    "nacimientos_hoy": 6,
    "procesos_activos": 2,
    "hora_servidor": "14:35:22",
    "fecha_servidor": "06/12/2025"
}
```

---

## 9. Dashboards por Rol

### 9.1 Mapeo de Dashboards

| Rol | Dashboard | Contenido Principal |
|-----|-----------|---------------------|
| **Médico** | `dashboard_medico` | Mis procesos, procesos activos, partos del día |
| **Matrona** | `dashboard_matrona` | Confirmaciones pendientes, fichas activas, próximas a 8cm |
| **TENS** | `dashboard_tens` | Confirmaciones, mis asignaciones, registros del día |
| **Coordinador** | `dashboard_coordinador` | Estado de salas, procesos activos, estadísticas |
| **Admin** | `dashboard_admin` | Usuarios conectados, accesos, estadísticas generales |

### 9.2 Redirección Automática

```python
ROLE_REDIRECT_MAP = {
    'administrador': 'inicio:dashboard_admin',      # Prioridad 1
    'coordinador': 'inicio:dashboard_coordinador',  # Prioridad 2
    'medico': 'inicio:dashboard_medico',            # Prioridad 3
    'matrona': 'inicio:dashboard_matrona',          # Prioridad 4
    'tens': 'inicio:dashboard_tens',                # Prioridad 5
}
```

---

## 10. Seguridad

### 10.1 Medidas Implementadas

| Medida | Descripción |
|--------|-------------|
| **Registro de IP** | Cada login registra IP del cliente |
| **Registro de intentos fallidos** | Se guardan intentos con username y motivo |
| **Sesiones activas** | Control de sesiones por usuario |
| **Timeout de sesión** | Configurable, por defecto 8 horas |
| **User Agent** | Se registra navegador/dispositivo |
| **CSRF Protection** | Token en todos los formularios |
| **Password hashing** | Django's PBKDF2 por defecto |

### 10.2 Tabla de Seguridad

```python
# Configuración en settings.py

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 28800  # 8 horas
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # En producción
```

---

## 11. Configuración de Grupos

### 11.1 Grupos del Sistema

| Grupo | Descripción | Dashboard |
|-------|-------------|-----------|
| `administrador` | Administración completa del sistema | Admin |
| `coordinador` | Coordinación de procesos y salas | Coordinador |
| `medico` | Médicos obstetras | Médico |
| `matrona` | Matronas | Matrona |
| `tens` | Técnicos en enfermería | TENS |

### 11.2 Script de Creación

```python
# Ejecutar: python manage.py crear_grupos

from django.contrib.auth.models import Group

grupos = [
    'administrador',
    'coordinador', 
    'medico',
    'matrona',
    'tens',
]

for nombre in grupos:
    Group.objects.get_or_create(name=nombre)
```

---

## 12. Signals

```python
# inicioApp/signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """Se ejecuta cuando un usuario inicia sesión"""
    from .utils import registrar_acceso
    
    registrar_acceso(
        request=request,
        usuario=user,
        tipo='LOGIN',
        exitoso=True
    )


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    """Se ejecuta cuando un usuario cierra sesión"""
    from .utils import registrar_acceso
    from .models import SesionActiva
    
    if user:
        registrar_acceso(
            request=request,
            usuario=user,
            tipo='LOGOUT',
            exitoso=True
        )
        
        # Eliminar sesión activa
        SesionActiva.objects.filter(
            session_key=request.session.session_key
        ).delete()


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    """Se ejecuta cuando falla un intento de login"""
    from .utils import registrar_acceso
    
    registrar_acceso(
        request=request,
        usuario=None,
        tipo='LOGIN_FALLIDO',
        exitoso=False,
        username_intento=credentials.get('username', ''),
        motivo='Credenciales inválidas'
    )
```

---

## 13. Tests

### 13.1 Casos de Prueba

| ID | Caso | Entrada | Resultado Esperado |
|----|------|---------|-------------------|
| CP-001 | Login exitoso | Credenciales válidas | Redirección a dashboard |
| CP-002 | Login fallido | Credenciales inválidas | Mensaje de error, registro de intento |
| CP-003 | Logout | Usuario autenticado | Sesión cerrada, registro de logout |
| CP-004 | Redirección médico | Usuario con rol médico | Dashboard médico |
| CP-005 | Redirección matrona | Usuario con rol matrona | Dashboard matrona |
| CP-006 | Screensaver | Usuario no autenticado | Pantalla de screensaver |
| CP-007 | API estadísticas | GET /api/estadisticas/ | JSON con estadísticas |
| CP-008 | Sesión expirada | Sesión timeout | Redirección a login |

### 13.2 Comandos de Test

```bash
# Ejecutar tests de inicioApp
pytest inicioApp/tests/ -v

# Test específico de login
pytest inicioApp/tests/test_views.py::TestLoginView -v

# Coverage
pytest inicioApp/tests/ --cov=inicioApp --cov-report=html
```

---

## 📊 Diagrama de Flujo de Autenticación

```
┌─────────────────────────────────────────────────────────────────────┐
│                     FLUJO DE AUTENTICACIÓN                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐                                               │
│  │ Usuario accede  │                                               │
│  │ al sistema      │                                               │
│  └────────┬────────┘                                               │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐     NO      ┌─────────────────┐              │
│  │ ¿Está           │────────────▶│   Screensaver   │              │
│  │ autenticado?    │             │   (login btn)   │              │
│  └────────┬────────┘             └────────┬────────┘              │
│           │ SÍ                            │                        │
│           │                               │ Click login            │
│           │                               ▼                        │
│           │                      ┌─────────────────┐              │
│           │                      │  Formulario de  │              │
│           │                      │     Login       │              │
│           │                      └────────┬────────┘              │
│           │                               │                        │
│           │               ┌───────────────┴───────────────┐       │
│           │               │                               │       │
│           │               ▼                               ▼       │
│           │      ┌─────────────────┐             ┌─────────────────┐
│           │      │ Credenciales    │             │ Credenciales    │
│           │      │ VÁLIDAS         │             │ INVÁLIDAS       │
│           │      └────────┬────────┘             └────────┬────────┘
│           │               │                               │       │
│           │               │ - Registrar acceso            │       │
│           │               │ - Crear sesión activa         │       │
│           │               │ - Determinar rol              │       │
│           │               │                               │       │
│           │               ▼                               ▼       │
│           │      ┌─────────────────┐             ┌─────────────────┐
│           └─────▶│ Redirección a   │             │ Mensaje error   │
│                  │ Dashboard       │             │ Registrar fallo │
│                  │ según ROL       │             └─────────────────┘
│                  └─────────────────┘                               │
│                          │                                         │
│         ┌────────────────┼────────────────┐                       │
│         │                │                │                        │
│         ▼                ▼                ▼                        │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐                 │
│  │ Dashboard │    │ Dashboard │    │ Dashboard │                 │
│  │  Médico   │    │  Matrona  │    │   TENS    │   ...          │
│  └───────────┘    └───────────┘    └───────────┘                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Permisos

| Acción | Público | Médico | Matrona | TENS | Coord. | Admin |
|--------|:-------:|:------:|:-------:|:----:|:------:|:-----:|
| Ver screensaver | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Login | ✅ | - | - | - | - | - |
| Ver dashboard propio | - | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver perfil | - | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cambiar contraseña | - | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver usuarios conectados | - | ❌ | ❌ | ❌ | ✅ | ✅ |
| Ver historial accesos | - | ❌ | ❌ | ❌ | ❌ | ✅ |

---

*Documentación inicioApp - OB_CARE v1.0*
