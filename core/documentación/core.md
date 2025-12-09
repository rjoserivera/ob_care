# 🔧 core

## Utilidades Compartidas del Sistema

La app `core` contiene componentes reutilizables, mixins, decoradores, context processors y utilidades que son compartidas por todas las demás aplicaciones del sistema OB_CARE.

---

## 📋 Tabla de Contenidos

1. [Estructura](#1-estructura)
2. [Modelos Base](#2-modelos-base)
3. [Mixins](#3-mixins)
4. [Decoradores](#4-decoradores)
5. [Context Processors](#5-context-processors)
6. [Middleware](#6-middleware)
7. [Template Tags](#7-template-tags)
8. [Utilidades](#8-utilidades)
9. [Validadores](#9-validadores)
10. [API Base](#10-api-base)
11. [Management Commands](#11-management-commands)
12. [Templates Base](#12-templates-base)
13. [Constantes](#13-constantes)

---

## 1. Estructura

```
core/
├── __init__.py
├── apps.py
├── admin.py
├── models.py               # Modelos base abstractos
├── views.py                # Vistas genéricas
├── urls.py
├── mixins.py               # Mixins para vistas y modelos
├── decorators.py           # Decoradores personalizados
├── context_processors.py   # Context processors
├── middleware.py           # Middleware personalizado
├── validators.py           # Validadores reutilizables
├── utils.py                # Funciones utilitarias
├── constants.py            # Constantes del sistema
├── exceptions.py           # Excepciones personalizadas
├── api/
│   ├── __init__.py
│   ├── urls.py
│   ├── views.py
│   ├── serializers.py
│   └── permissions.py
├── management/
│   └── commands/
│       ├── crear_grupos.py
│       ├── cargar_catalogos.py
│       └── generar_datos_prueba.py
├── templatetags/
│   ├── __init__.py
│   └── core_tags.py
└── templates/
    └── core/
        ├── base.html
        ├── base_dashboard.html
        ├── partials/
        │   ├── _navbar.html
        │   ├── _sidebar.html
        │   ├── _messages.html
        │   ├── _pagination.html
        │   └── _confirm_modal.html
        └── errors/
            ├── 403.html
            ├── 404.html
            └── 500.html
```

---

## 2. Modelos Base

```python
# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Modelo abstracto que agrega campos de auditoría de tiempo.
    Heredar de este modelo para tener created_at y updated_at automáticos.
    """
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización"
    )
    
    class Meta:
        abstract = True


class AuditedModel(TimeStampedModel):
    """
    Modelo abstracto con auditoría completa.
    Incluye timestamps + usuario que creó/modificó.
    """
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_created',
        verbose_name="Creado Por",
        null=True,
        blank=True
    )
    
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_updated',
        verbose_name="Actualizado Por",
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        # El usuario debe ser pasado como kwarg 'user'
        user = kwargs.pop('user', None)
        
        if user:
            if not self.pk:
                self.created_by = user
            self.updated_by = user
        
        super().save(*args, **kwargs)


class SoftDeleteModel(models.Model):
    """
    Modelo abstracto con borrado lógico (soft delete).
    En lugar de eliminar, marca como inactivo.
    """
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Eliminación"
    )
    
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_deleted',
        null=True,
        blank=True,
        verbose_name="Eliminado Por"
    )
    
    class Meta:
        abstract = True
    
    def soft_delete(self, user=None):
        """Realiza borrado lógico"""
        self.is_active = False
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()
    
    def restore(self):
        """Restaura un registro eliminado"""
        self.is_active = True
        self.deleted_at = None
        self.deleted_by = None
        self.save()


class CatalogoBase(models.Model):
    """
    Modelo base para todos los catálogos del sistema.
    Proporciona estructura consistente.
    """
    
    codigo = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Código"
    )
    
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre"
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        abstract = True
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre


class CatalogoConColor(CatalogoBase):
    """Catálogo base con campo de color para UI"""
    
    color = models.CharField(
        max_length=7,
        default='#6c757d',
        verbose_name="Color (Hex)",
        help_text="Color en formato hexadecimal, ej: #28a745"
    )
    
    icono = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icono",
        help_text="Clase de Bootstrap Icons, ej: bi-check-circle"
    )
    
    class Meta:
        abstract = True
```

---

## 3. Mixins

```python
# core/mixins.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse


class RoleRequiredMixin(UserPassesTestMixin):
    """
    Mixin que requiere que el usuario tenga uno de los roles especificados.
    
    Uso:
        class MiVista(RoleRequiredMixin, View):
            roles_requeridos = ['medico', 'matrona']
    """
    
    roles_requeridos = []
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        if self.request.user.is_superuser:
            return True
        
        user_groups = set(self.request.user.groups.values_list('name', flat=True))
        return bool(user_groups.intersection(set(self.roles_requeridos)))
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            'No tiene permisos para acceder a esta página.'
        )
        return redirect('inicio:home')


class MedicoRequiredMixin(RoleRequiredMixin):
    """Requiere rol de médico"""
    roles_requeridos = ['medico']


class MatronaRequiredMixin(RoleRequiredMixin):
    """Requiere rol de matrona"""
    roles_requeridos = ['matrona']


class TensRequiredMixin(RoleRequiredMixin):
    """Requiere rol de TENS"""
    roles_requeridos = ['tens']


class PersonalClinicoMixin(RoleRequiredMixin):
    """Requiere cualquier rol clínico"""
    roles_requeridos = ['medico', 'matrona', 'tens']


class AjaxResponseMixin:
    """
    Mixin para vistas que pueden responder con JSON en requests AJAX.
    
    Uso:
        class MiVista(AjaxResponseMixin, View):
            def get(self, request):
                data = {'mensaje': 'Hola'}
                return self.render_ajax_or_template(data, 'template.html')
    """
    
    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    def render_ajax_or_template(self, data, template_name, context=None):
        if self.is_ajax():
            return JsonResponse(data)
        
        context = context or {}
        context.update(data)
        return self.render_to_response(context)
    
    def ajax_success(self, message='Operación exitosa', data=None):
        response = {'success': True, 'message': message}
        if data:
            response['data'] = data
        return JsonResponse(response)
    
    def ajax_error(self, message='Error en la operación', errors=None):
        response = {'success': False, 'message': message}
        if errors:
            response['errors'] = errors
        return JsonResponse(response, status=400)


class FormMessageMixin:
    """
    Mixin que agrega mensajes automáticos después de operaciones de formulario.
    """
    
    success_message = "Operación realizada con éxito."
    error_message = "Error al procesar el formulario."
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, self.error_message)
        return response


class AuditMixin:
    """
    Mixin para vistas que trabajan con modelos auditados.
    Automáticamente pasa el usuario al guardar.
    """
    
    def form_valid(self, form):
        form.instance.save(user=self.request.user)
        return super().form_valid(form)


class PaginationMixin:
    """
    Mixin que agrega paginación configurable a vistas de lista.
    """
    
    paginate_by = 20
    
    def get_paginate_by(self, queryset):
        # Permitir cambiar paginación por query param
        per_page = self.request.GET.get('per_page')
        if per_page and per_page.isdigit():
            return min(int(per_page), 100)  # Máximo 100
        return self.paginate_by


class SearchMixin:
    """
    Mixin que agrega búsqueda a vistas de lista.
    
    Uso:
        class MiListView(SearchMixin, ListView):
            search_fields = ['nombre', 'apellido', 'rut']
    """
    
    search_fields = []
    search_param = 'q'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get(self.search_param, '').strip()
        
        if query and self.search_fields:
            from django.db.models import Q
            
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__icontains': query})
            
            queryset = queryset.filter(q_objects)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get(self.search_param, '')
        return context


class ExportMixin:
    """
    Mixin para exportar datos a diferentes formatos.
    """
    
    export_filename = 'export'
    
    def export_csv(self, queryset, fields):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.export_filename}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(fields)
        
        for obj in queryset:
            row = [getattr(obj, field, '') for field in fields]
            writer.writerow(row)
        
        return response
    
    def export_excel(self, queryset, fields):
        import openpyxl
        from django.http import HttpResponse
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(fields)
        
        for obj in queryset:
            row = [getattr(obj, field, '') for field in fields]
            ws.append(row)
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{self.export_filename}.xlsx"'
        
        wb.save(response)
        return response
```

---

## 4. Decoradores

```python
# core/decorators.py

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied


def role_required(roles):
    """
    Decorador que requiere que el usuario tenga uno de los roles especificados.
    
    Uso:
        @role_required(['medico', 'matrona'])
        def mi_vista(request):
            ...
    """
    if isinstance(roles, str):
        roles = [roles]
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            user_groups = set(request.user.groups.values_list('name', flat=True))
            
            if not user_groups.intersection(set(roles)):
                messages.error(request, 'No tiene permisos para esta acción.')
                return redirect('inicio:home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def roles_required(roles):
    """Alias de role_required para consistencia"""
    return role_required(roles)


def medico_required(view_func):
    """Decorador que requiere rol de médico"""
    return role_required(['medico'])(view_func)


def matrona_required(view_func):
    """Decorador que requiere rol de matrona"""
    return role_required(['matrona'])(view_func)


def tens_required(view_func):
    """Decorador que requiere rol de TENS"""
    return role_required(['tens'])(view_func)


def ajax_required(view_func):
    """
    Decorador que requiere que la petición sea AJAX.
    
    Uso:
        @ajax_required
        def mi_vista_ajax(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return JsonResponse(
                {'error': 'Se requiere petición AJAX'},
                status=400
            )
        return view_func(request, *args, **kwargs)
    return wrapper


def log_action(action_name):
    """
    Decorador que registra acciones en el log.
    
    Uso:
        @log_action('crear_proceso')
        def crear_proceso(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            import logging
            logger = logging.getLogger('obstetric_care')
            
            logger.info(
                f"Acción: {action_name} | "
                f"Usuario: {request.user.username} | "
                f"IP: {get_client_ip(request)}"
            )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def get_client_ip(request):
    """Obtiene la IP real del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def cache_response(timeout=300, key_prefix=''):
    """
    Decorador para cachear respuestas.
    
    Uso:
        @cache_response(timeout=600, key_prefix='dashboard')
        def dashboard(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            from django.core.cache import cache
            
            cache_key = f"{key_prefix}:{request.path}:{request.user.id}"
            
            response = cache.get(cache_key)
            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(cache_key, response, timeout)
            
            return response
        return wrapper
    return decorator


def transaction_atomic(view_func):
    """
    Decorador que envuelve la vista en una transacción atómica.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        from django.db import transaction
        
        with transaction.atomic():
            return view_func(request, *args, **kwargs)
    
    return wrapper
```

---

## 5. Context Processors

```python
# core/context_processors.py

from django.conf import settings


def hospital_info(request):
    """
    Agrega información del hospital al contexto de todos los templates.
    """
    return {
        'hospital': settings.HOSPITAL_CONFIG,
        'sistema_nombre': 'OB-CARE',
        'sistema_version': '1.0.0',
    }


def user_permissions(request):
    """
    Agrega información de permisos del usuario al contexto.
    """
    context = {
        'is_medico': False,
        'is_matrona': False,
        'is_tens': False,
        'is_admin': False,
        'is_coordinador': False,
        'user_roles': [],
    }
    
    if request.user.is_authenticated:
        roles = list(request.user.groups.values_list('name', flat=True))
        context.update({
            'is_medico': 'medico' in roles,
            'is_matrona': 'matrona' in roles,
            'is_tens': 'tens' in roles,
            'is_admin': 'administrador' in roles or request.user.is_superuser,
            'is_coordinador': 'coordinador' in roles,
            'user_roles': roles,
        })
    
    return context


def proceso_parto_config(request):
    """
    Agrega configuración de procesos de parto al contexto.
    """
    return {
        'proceso_config': settings.PROCESO_PARTO_CONFIG,
    }


def menu_items(request):
    """
    Genera los items del menú según el rol del usuario.
    """
    if not request.user.is_authenticated:
        return {'menu_items': []}
    
    roles = set(request.user.groups.values_list('name', flat=True))
    
    items = [
        {
            'nombre': 'Inicio',
            'url': 'inicio:home',
            'icono': 'bi-house',
            'roles': ['medico', 'matrona', 'tens', 'administrador', 'coordinador'],
        },
        {
            'nombre': 'Procesos',
            'url': 'procesos:dashboard',
            'icono': 'bi-activity',
            'roles': ['medico', 'matrona', 'tens', 'coordinador'],
            'submenu': [
                {'nombre': 'Activos', 'url': 'procesos:activos'},
                {'nombre': 'Historial', 'url': 'procesos:historial'},
                {'nombre': 'Salas', 'url': 'procesos:salas'},
            ]
        },
        {
            'nombre': 'Pacientes',
            'url': 'gestion:pacientes',
            'icono': 'bi-people',
            'roles': ['medico', 'matrona', 'administrador'],
        },
        {
            'nombre': 'Fichas Obstétricas',
            'url': 'matrona:fichas',
            'icono': 'bi-file-medical',
            'roles': ['medico', 'matrona'],
        },
        {
            'nombre': 'Registros TENS',
            'url': 'tens:registros',
            'icono': 'bi-heart-pulse',
            'roles': ['tens', 'matrona', 'medico'],
        },
        {
            'nombre': 'Partos',
            'url': 'partos:lista',
            'icono': 'bi-person-plus',
            'roles': ['medico', 'matrona'],
        },
        {
            'nombre': 'Recién Nacidos',
            'url': 'recien_nacido:lista',
            'icono': 'bi-emoji-smile',
            'roles': ['medico', 'matrona'],
        },
        {
            'nombre': 'Personal',
            'url': 'gestion:personal',
            'icono': 'bi-person-badge',
            'roles': ['administrador'],
        },
    ]
    
    # Filtrar según roles del usuario
    menu_filtrado = []
    for item in items:
        if roles.intersection(set(item['roles'])) or request.user.is_superuser:
            menu_filtrado.append(item)
    
    return {'menu_items': menu_filtrado}
```

---

## 6. Middleware

```python
# core/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger('obstetric_care')


class LoginRequiredMiddleware:
    """
    Middleware que requiere login para todas las vistas excepto las públicas.
    """
    
    EXEMPT_URLS = [
        '/login/',
        '/logout/',
        '/admin/',
        '/static/',
        '/media/',
        '/api/auth/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            
            if not any(path.startswith(url) for url in self.EXEMPT_URLS):
                login_url = reverse('login')
                return redirect(f"{login_url}?next={path}")
        
        return self.get_response(request)


class RoleMiddleware:
    """
    Middleware que agrega información de rol al request.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            request.user_roles = list(
                request.user.groups.values_list('name', flat=True)
            )
            request.is_medico = 'medico' in request.user_roles
            request.is_matrona = 'matrona' in request.user_roles
            request.is_tens = 'tens' in request.user_roles
            request.is_admin = 'administrador' in request.user_roles
            request.is_coordinador = 'coordinador' in request.user_roles
        else:
            request.user_roles = []
            request.is_medico = False
            request.is_matrona = False
            request.is_tens = False
            request.is_admin = False
            request.is_coordinador = False
        
        return self.get_response(request)


class RequestLoggingMiddleware:
    """
    Middleware que registra información de cada request.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Antes del request
        request._start_time = timezone.now()
        
        response = self.get_response(request)
        
        # Después del request
        if request.user.is_authenticated:
            duration = timezone.now() - request._start_time
            
            logger.info(
                f"Request: {request.method} {request.path} | "
                f"User: {request.user.username} | "
                f"Status: {response.status_code} | "
                f"Duration: {duration.total_seconds():.3f}s"
            )
        
        return response


class TimezoneMiddleware:
    """
    Middleware que configura la zona horaria del usuario.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Por defecto, usar zona horaria de Chile
        timezone.activate('America/Santiago')
        return self.get_response(request)


class SecurityHeadersMiddleware:
    """
    Middleware que agrega headers de seguridad adicionales.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
```

---

## 7. Template Tags

```python
# core/templatetags/core_tags.py

from django import template
from django.utils.safestring import mark_safe
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter
def has_role(user, role):
    """
    Verifica si el usuario tiene un rol específico.
    
    Uso: {% if user|has_role:"medico" %}
    """
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    return user.groups.filter(name=role).exists()


@register.filter
def has_any_role(user, roles):
    """
    Verifica si el usuario tiene alguno de los roles.
    
    Uso: {% if user|has_any_role:"medico,matrona" %}
    """
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    role_list = [r.strip() for r in roles.split(',')]
    return user.groups.filter(name__in=role_list).exists()


@register.simple_tag
def estado_badge(estado):
    """
    Genera un badge de Bootstrap para un estado.
    
    Uso: {% estado_badge proceso.estado %}
    """
    if hasattr(estado, 'color'):
        color = estado.color
        nombre = estado.nombre
    else:
        color = '#6c757d'
        nombre = str(estado)
    
    return mark_safe(
        f'<span class="badge" style="background-color: {color}">{nombre}</span>'
    )


@register.simple_tag
def prioridad_badge(prioridad):
    """
    Genera un badge para la prioridad.
    """
    colores = {
        'P1_EMERGENCIA': 'danger',
        'P2_ALTA': 'warning',
        'P3_PRIORITARIA': 'info',
        'P4_NORMAL': 'success',
    }
    
    codigo = prioridad.codigo if hasattr(prioridad, 'codigo') else str(prioridad)
    color = colores.get(codigo, 'secondary')
    nombre = prioridad.nombre if hasattr(prioridad, 'nombre') else str(prioridad)
    
    return mark_safe(f'<span class="badge bg-{color}">{nombre}</span>')


@register.filter
def tiempo_transcurrido(fecha):
    """
    Muestra tiempo transcurrido de forma legible.
    
    Uso: {{ proceso.created_at|tiempo_transcurrido }}
    """
    if not fecha:
        return ''
    
    ahora = timezone.now()
    diff = ahora - fecha
    
    if diff < timedelta(minutes=1):
        return 'hace un momento'
    elif diff < timedelta(hours=1):
        minutos = int(diff.total_seconds() / 60)
        return f'hace {minutos} minuto{"s" if minutos > 1 else ""}'
    elif diff < timedelta(days=1):
        horas = int(diff.total_seconds() / 3600)
        return f'hace {horas} hora{"s" if horas > 1 else ""}'
    elif diff < timedelta(days=30):
        dias = diff.days
        return f'hace {dias} día{"s" if dias > 1 else ""}'
    else:
        return fecha.strftime('%d/%m/%Y')


@register.filter
def formato_rut(rut):
    """
    Formatea un RUT chileno.
    
    Uso: {{ paciente.rut|formato_rut }}
    """
    if not rut:
        return ''
    
    rut = str(rut).replace('.', '').replace('-', '').upper()
    
    if len(rut) < 2:
        return rut
    
    cuerpo = rut[:-1]
    dv = rut[-1]
    
    # Agregar puntos
    cuerpo_formateado = ''
    for i, char in enumerate(reversed(cuerpo)):
        if i > 0 and i % 3 == 0:
            cuerpo_formateado = '.' + cuerpo_formateado
        cuerpo_formateado = char + cuerpo_formateado
    
    return f'{cuerpo_formateado}-{dv}'


@register.filter
def duracion_minutos(minutos):
    """
    Formatea duración en minutos a formato legible.
    
    Uso: {{ proceso.duracion|duracion_minutos }}
    """
    if not minutos:
        return '--'
    
    if minutos < 60:
        return f'{minutos} min'
    
    horas = minutos // 60
    mins = minutos % 60
    
    if mins == 0:
        return f'{horas}h'
    
    return f'{horas}h {mins}min'


@register.inclusion_tag('core/partials/_pagination.html')
def pagination(page_obj, request):
    """
    Renderiza paginación con Bootstrap.
    
    Uso: {% pagination page_obj request %}
    """
    return {
        'page_obj': page_obj,
        'request': request,
    }


@register.inclusion_tag('core/partials/_messages.html')
def show_messages(messages):
    """
    Renderiza mensajes de Django con Bootstrap alerts.
    
    Uso: {% show_messages messages %}
    """
    return {'messages': messages}


@register.simple_tag(takes_context=True)
def query_string(context, **kwargs):
    """
    Modifica query string manteniendo parámetros existentes.
    
    Uso: <a href="?{% query_string page=2 %}">Página 2</a>
    """
    request = context['request']
    params = request.GET.copy()
    
    for key, value in kwargs.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value
    
    return params.urlencode()
```

---

## 8. Utilidades

```python
# core/utils.py

from django.utils import timezone
from django.conf import settings
import re


def formatear_rut(rut):
    """Formatea RUT con puntos y guión"""
    rut = limpiar_rut(rut)
    if len(rut) < 2:
        return rut
    
    cuerpo = rut[:-1]
    dv = rut[-1]
    
    cuerpo_formateado = ''
    for i, char in enumerate(reversed(cuerpo)):
        if i > 0 and i % 3 == 0:
            cuerpo_formateado = '.' + cuerpo_formateado
        cuerpo_formateado = char + cuerpo_formateado
    
    return f'{cuerpo_formateado}-{dv}'


def limpiar_rut(rut):
    """Limpia RUT dejando solo números y K"""
    if not rut:
        return ''
    return re.sub(r'[^0-9Kk]', '', str(rut)).upper()


def validar_rut(rut):
    """Valida RUT chileno con módulo 11"""
    rut = limpiar_rut(rut)
    
    if len(rut) < 2:
        return False
    
    cuerpo = rut[:-1]
    dv = rut[-1]
    
    try:
        cuerpo_int = int(cuerpo)
    except ValueError:
        return False
    
    suma = 0
    multiplicador = 2
    
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2
    
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_esperado = '0'
    elif dv_calculado == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(dv_calculado)
    
    return dv == dv_esperado


def calcular_edad(fecha_nacimiento):
    """Calcula edad a partir de fecha de nacimiento"""
    if not fecha_nacimiento:
        return None
    
    hoy = timezone.now().date()
    edad = hoy.year - fecha_nacimiento.year
    
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    
    return edad


def generar_codigo_unico(prefijo, modelo, campo='codigo'):
    """
    Genera un código único para un modelo.
    
    Uso:
        codigo = generar_codigo_unico('MT', ProcesoParto)
        # Retorna: MT-0001, MT-0002, etc.
    """
    from django.db.models import Max
    
    ultimo = modelo.objects.aggregate(Max('id'))['id__max'] or 0
    return f"{prefijo}-{(ultimo + 1):04d}"


def get_client_ip(request):
    """Obtiene la IP real del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def truncate_string(text, length=100, suffix='...'):
    """Trunca un string a una longitud máxima"""
    if not text:
        return ''
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def format_currency(amount, symbol='$'):
    """Formatea un número como moneda chilena"""
    if amount is None:
        return f'{symbol} 0'
    
    formatted = '{:,.0f}'.format(amount).replace(',', '.')
    return f'{symbol} {formatted}'


def fecha_a_texto(fecha):
    """Convierte fecha a texto en español"""
    if not fecha:
        return ''
    
    meses = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    
    return f'{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}'
```

---

## 9. Validadores

```python
# core/validators.py

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


class RutValidator:
    """
    Validador de RUT chileno.
    
    Uso:
        rut = models.CharField(validators=[RutValidator()])
    """
    
    message = 'RUT inválido. Verifique el número ingresado.'
    code = 'invalid_rut'
    
    def __call__(self, value):
        from .utils import validar_rut
        
        if not validar_rut(value):
            raise ValidationError(self.message, code=self.code)


class TelefonoChilenoValidator(RegexValidator):
    """Validador de teléfono chileno"""
    
    regex = r'^(\+56)?[29]\d{8}$'
    message = 'Ingrese un teléfono válido (ej: +56912345678 o 912345678)'


class RangoValidator:
    """
    Validador de rango numérico.
    
    Uso:
        temperatura = models.DecimalField(
            validators=[RangoValidator(34.0, 42.0, 'Temperatura')]
        )
    """
    
    def __init__(self, min_val, max_val, field_name='Valor'):
        self.min_val = min_val
        self.max_val = max_val
        self.field_name = field_name
    
    def __call__(self, value):
        if value < self.min_val or value > self.max_val:
            raise ValidationError(
                f'{self.field_name} debe estar entre {self.min_val} y {self.max_val}. '
                f'Valor ingresado: {value}'
            )


class ApgarValidator(RangoValidator):
    """Validador para puntaje APGAR (0-10)"""
    
    def __init__(self):
        super().__init__(0, 10, 'Puntaje APGAR')


class PesoRecienNacidoValidator(RangoValidator):
    """Validador para peso de recién nacido (300g - 6000g)"""
    
    def __init__(self):
        super().__init__(300, 6000, 'Peso del recién nacido')


class TallaRecienNacidoValidator(RangoValidator):
    """Validador para talla de recién nacido (20cm - 60cm)"""
    
    def __init__(self):
        super().__init__(20, 60, 'Talla del recién nacido')


class DilatacionValidator(RangoValidator):
    """Validador para dilatación cervical (0-10 cm)"""
    
    def __init__(self):
        super().__init__(0, 10, 'Dilatación')


class TemperaturaValidator(RangoValidator):
    """Validador para temperatura corporal (34-42 °C)"""
    
    def __init__(self):
        super().__init__(34.0, 42.0, 'Temperatura')


class FrecuenciaCardiacaValidator(RangoValidator):
    """Validador para frecuencia cardíaca (30-200 bpm)"""
    
    def __init__(self):
        super().__init__(30, 200, 'Frecuencia cardíaca')


class SaturacionOxigenoValidator(RangoValidator):
    """Validador para saturación de oxígeno (0-100%)"""
    
    def __init__(self):
        super().__init__(0, 100, 'Saturación de oxígeno')
```

---

## 10. API Base

```python
# core/api/permissions.py

from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """Requiere autenticación"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsMedico(BasePermission):
    """Requiere rol de médico"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='medico').exists()


class IsMatrona(BasePermission):
    """Requiere rol de matrona"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='matrona').exists()


class IsTens(BasePermission):
    """Requiere rol de TENS"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='tens').exists()


class IsPersonalClinico(BasePermission):
    """Requiere cualquier rol clínico"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(
            name__in=['medico', 'matrona', 'tens']
        ).exists()


class IsCoordinador(BasePermission):
    """Requiere rol de coordinador"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='coordinador').exists()


# core/api/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer base para usuarios"""
    
    nombre_completo = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nombre_completo', 'roles']
    
    def get_nombre_completo(self, obj):
        return obj.get_full_name() or obj.username
    
    def get_roles(self, obj):
        return list(obj.groups.values_list('name', flat=True))


class ResponseSerializer(serializers.Serializer):
    """Serializer base para respuestas estandarizadas"""
    
    success = serializers.BooleanField()
    message = serializers.CharField(required=False)
    data = serializers.DictField(required=False)
```

---

## 11. Management Commands

```python
# core/management/commands/crear_grupos.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Crea los grupos de usuarios y asigna permisos'
    
    def handle(self, *args, **options):
        grupos = [
            {
                'nombre': 'administrador',
                'descripcion': 'Administrador del sistema'
            },
            {
                'nombre': 'medico',
                'descripcion': 'Médico obstetra'
            },
            {
                'nombre': 'matrona',
                'descripcion': 'Matrona'
            },
            {
                'nombre': 'tens',
                'descripcion': 'Técnico en Enfermería'
            },
            {
                'nombre': 'coordinador',
                'descripcion': 'Coordinador de procesos'
            },
        ]
        
        for grupo_data in grupos:
            grupo, created = Group.objects.get_or_create(
                name=grupo_data['nombre']
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Grupo creado: {grupo.name}')
                )
            else:
                self.stdout.write(f'Grupo existente: {grupo.name}')
        
        self.stdout.write(self.style.SUCCESS('Grupos creados exitosamente'))


# core/management/commands/cargar_catalogos.py

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Carga los catálogos iniciales del sistema'
    
    def handle(self, *args, **options):
        from gestionProcesosApp.models import (
            CatalogoEstadoProceso, CatalogoEstadoSala,
            CatalogoTipoPaciente, CatalogoTipoProceso,
            CatalogoPrioridad, CatalogoNivelRiesgo, CatalogoRolProceso
        )
        
        # Cargar estados de proceso
        estados_proceso = [
            {'codigo': 'CREADO', 'nombre': 'Creado', 'color': '#6c757d', 'orden': 1},
            {'codigo': 'INICIADO', 'nombre': 'Iniciado', 'color': '#17a2b8', 'orden': 2},
            {'codigo': 'CONFIRMADO', 'nombre': 'Confirmado', 'color': '#28a745', 'orden': 3},
            {'codigo': 'EN_CURSO', 'nombre': 'En Curso', 'color': '#007bff', 'orden': 4},
            {'codigo': 'CERRADO', 'nombre': 'Cerrado', 'color': '#28a745', 'orden': 5},
            {'codigo': 'CERRADO_DERIVACION', 'nombre': 'Cerrado con Derivación', 'color': '#6f42c1', 'orden': 6},
        ]
        
        for data in estados_proceso:
            CatalogoEstadoProceso.objects.update_or_create(
                codigo=data['codigo'],
                defaults=data
            )
        
        self.stdout.write(self.style.SUCCESS('Catálogos cargados exitosamente'))
```

---

## 12. Templates Base

### 12.1 Template Base Principal

```html
<!-- core/templates/core/base.html -->

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token }}">
    
    <title>{% block title %}OB-CARE{% endblock %} | {{ hospital.NOMBRE }}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link href="{% static 'css/custom.css' %}" rel="stylesheet">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'core/partials/_navbar.html' %}
    
    <div class="container-fluid">
        <div class="row">
            {% if user.is_authenticated %}
                {% include 'core/partials/_sidebar.html' %}
                
                <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                    {% include 'core/partials/_messages.html' %}
                    
                    {% block content %}{% endblock %}
                </main>
            {% else %}
                <main class="col-12">
                    {% include 'core/partials/_messages.html' %}
                    
                    {% block content %}{% endblock %}
                </main>
            {% endif %}
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script src="{% static 'js/main.js' %}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## 13. Constantes

```python
# core/constants.py

# ═══════════════════════════════════════════════════════════════
# CONSTANTES DEL SISTEMA OB-CARE
# ═══════════════════════════════════════════════════════════════

# Configuración de procesos de parto
DILATACION_MINIMA_INICIO = 8  # cm
TIMEOUT_CONFIRMACION = 60      # segundos
DURACION_APEGO = 5             # minutos
TIEMPO_LIMPIEZA_SALA = 15      # minutos

# Prefijos de códigos
PREFIJO_PROCESO = 'MT'
PREFIJO_RECIEN_NACIDO = 'RN'
PREFIJO_FICHA = 'FO'

# Rangos de validación - Signos vitales
TEMPERATURA_MIN = 34.0
TEMPERATURA_MAX = 42.0
FC_MIN = 30
FC_MAX = 200
FR_MIN = 10
FR_MAX = 60
SATURACION_MIN = 0
SATURACION_MAX = 100

# Rangos de validación - Recién nacido
PESO_RN_MIN = 300   # gramos
PESO_RN_MAX = 6000  # gramos
TALLA_RN_MIN = 20   # cm
TALLA_RN_MAX = 60   # cm
APGAR_MIN = 0
APGAR_MAX = 10

# Roles del sistema
ROLES = {
    'MEDICO': 'medico',
    'MATRONA': 'matrona',
    'TENS': 'tens',
    'ADMINISTRADOR': 'administrador',
    'COORDINADOR': 'coordinador',
}

# Estados de proceso
ESTADOS_PROCESO = {
    'CREADO': 'CREADO',
    'INICIADO': 'INICIADO',
    'CONFIRMADO': 'CONFIRMADO',
    'EN_CURSO': 'EN_CURSO',
    'CERRADO': 'CERRADO',
    'CERRADO_DERIVACION': 'CERRADO_DERIVACION',
}

# Estados de sala
ESTADOS_SALA = {
    'DISPONIBLE': 'DISPONIBLE',
    'OCUPADA': 'OCUPADA',
    'LIMPIEZA': 'LIMPIEZA',
    'MANTENIMIENTO': 'MANTENIMIENTO',
}

# Prioridades
PRIORIDADES = {
    'P1': 'P1_EMERGENCIA',
    'P2': 'P2_ALTA',
    'P3': 'P3_PRIORITARIA',
    'P4': 'P4_NORMAL',
}

# Tipos de notificación
TIPOS_NOTIFICACION = {
    'URGENTE': 'URGENTE',
    'CODIGO_ROJO': 'CODIGO_ROJO',
    'EMERGENCIA_EXTERNA': 'EMERGENCIA_EXTERNA',
    'INFORMATIVO': 'INFORMATIVO',
}
```

---

## 📊 Diagrama de Dependencias

```
┌─────────────────────────────────────────────────────────────────────┐
│                              CORE                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐      ┌─────────────────┐                      │
│  │    models.py    │      │    mixins.py    │                      │
│  │  (Base Models)  │      │  (View Mixins)  │                      │
│  └────────┬────────┘      └────────┬────────┘                      │
│           │                        │                                │
│           ▼                        ▼                                │
│  ┌─────────────────────────────────────────────────────┐           │
│  │                  OTRAS APPS                          │           │
│  │  gestionApp, matronaApp, medicoApp, tensApp, etc.   │           │
│  └─────────────────────────────────────────────────────┘           │
│                                                                     │
│  ┌─────────────────┐      ┌─────────────────┐                      │
│  │  decorators.py  │      │  validators.py  │                      │
│  │ (@role_required)│      │  (RutValidator) │                      │
│  └─────────────────┘      └─────────────────┘                      │
│                                                                     │
│  ┌─────────────────┐      ┌─────────────────┐                      │
│  │  middleware.py  │      │   utils.py      │                      │
│  │ (RoleMiddleware)│      │ (formatear_rut) │                      │
│  └─────────────────┘      └─────────────────┘                      │
│                                                                     │
│  ┌─────────────────┐      ┌─────────────────┐                      │
│  │ context_proc.py │      │ templatetags/   │                      │
│  │ (hospital_info) │      │ (core_tags.py)  │                      │
│  └─────────────────┘      └─────────────────┘                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

*Documentación core - OB_CARE v1.0*
