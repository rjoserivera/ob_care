# ⚙️ obstetric_care (Proyecto Principal)

## Configuración del Proyecto Django

El proyecto `obstetric_care` es el contenedor principal de Django que configura y orquesta todas las aplicaciones del sistema de gestión obstétrica.

---

## 📋 Tabla de Contenidos

1. [Estructura del Proyecto](#1-estructura-del-proyecto)
2. [Configuración (settings.py)](#2-configuración-settingspy)
3. [URLs Principales (urls.py)](#3-urls-principales-urlspy)
4. [ASGI y WebSocket (asgi.py)](#4-asgi-y-websocket-asgipy)
5. [WSGI (wsgi.py)](#5-wsgi-wsgipy)
6. [Variables de Entorno](#6-variables-de-entorno)
7. [Base de Datos](#7-base-de-datos)
8. [Configuración de Apps](#8-configuración-de-apps)
9. [Middleware](#9-middleware)
10. [Configuración de Seguridad](#10-configuración-de-seguridad)
11. [Archivos Estáticos y Media](#11-archivos-estáticos-y-media)
12. [Logging](#12-logging)
13. [Celery (Tareas Asíncronas)](#13-celery-tareas-asíncronas)
14. [Despliegue](#14-despliegue)

---

## 1. Estructura del Proyecto

```
obstetric_care/
├── __init__.py
├── settings/
│   ├── __init__.py
│   ├── base.py          # Configuración base compartida
│   ├── development.py   # Configuración de desarrollo
│   ├── production.py    # Configuración de producción
│   └── testing.py       # Configuración para tests
├── urls.py              # URLs raíz del proyecto
├── asgi.py              # Configuración ASGI (WebSocket)
├── wsgi.py              # Configuración WSGI
├── celery.py            # Configuración de Celery
└── routing.py           # Rutas WebSocket
```

---

## 2. Configuración (settings.py)

### 2.1 Settings Base

```python
# obstetric_care/settings/base.py

import os
from pathlib import Path
from datetime import timedelta

# ═══════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ═══════════════════════════════════════════════════════════════
# APLICACIONES INSTALADAS
# ═══════════════════════════════════════════════════════════════
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    'django_extensions',
    'auditlog',
    'channels',
    'rest_framework',
    'corsheaders',
    'django_filters',
]

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'gestionApp.apps.GestionappConfig',
    'matronaApp.apps.MatronaappConfig',
    'medicoApp.apps.MedicoappConfig',
    'tensApp.apps.TensappConfig',
    'ingresoPartoApp.apps.IngresopartoappConfig',
    'partosApp.apps.PartosappConfig',
    'recienNacidoApp.apps.ReciennacidoappConfig',
    'legacyApp.apps.LegacyappConfig',
    'inicioApp.apps.InicioappConfig',
    'gestionProcesosApp.apps.GestionprocesosappConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ═══════════════════════════════════════════════════════════════
# MIDDLEWARE
# ═══════════════════════════════════════════════════════════════
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'core.middleware.LoginRequiredMiddleware',
    'core.middleware.RoleMiddleware',
]

# ═══════════════════════════════════════════════════════════════
# URLS Y TEMPLATES
# ═══════════════════════════════════════════════════════════════
ROOT_URLCONF = 'obstetric_care.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.hospital_info',
                'core.context_processors.user_permissions',
            ],
        },
    },
]

# ═══════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ═══════════════════════════════════════════════════════════════
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio:home'
LOGOUT_REDIRECT_URL = 'login'

# Sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 28800  # 8 horas
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# ═══════════════════════════════════════════════════════════════
# INTERNACIONALIZACIÓN
# ═══════════════════════════════════════════════════════════════
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Formatos de fecha/hora para Chile
DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i:s'
TIME_FORMAT = 'H:i:s'
DATE_INPUT_FORMATS = ['%d/%m/%Y', '%Y-%m-%d']

# ═══════════════════════════════════════════════════════════════
# ARCHIVOS ESTÁTICOS Y MEDIA
# ═══════════════════════════════════════════════════════════════
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise para servir estáticos en producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ═══════════════════════════════════════════════════════════════
# CRISPY FORMS
# ═══════════════════════════════════════════════════════════════
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ═══════════════════════════════════════════════════════════════
# DJANGO REST FRAMEWORK
# ═══════════════════════════════════════════════════════════════
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DATETIME_FORMAT': '%d/%m/%Y %H:%M:%S',
    'DATE_FORMAT': '%d/%m/%Y',
}

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

# ═══════════════════════════════════════════════════════════════
# CHANNELS (WebSocket)
# ═══════════════════════════════════════════════════════════════
ASGI_APPLICATION = 'obstetric_care.asgi.application'

# ═══════════════════════════════════════════════════════════════
# AUDITLOG
# ═══════════════════════════════════════════════════════════════
AUDITLOG_INCLUDE_ALL_MODELS = True

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DEL HOSPITAL
# ═══════════════════════════════════════════════════════════════
HOSPITAL_CONFIG = {
    'NOMBRE': 'Hospital Clínico Herminda Martín',
    'CIUDAD': 'Chillán',
    'REGION': 'Ñuble',
    'CODIGO': 'HCHM',
    'TELEFONO': '+56 42 123 4567',
}

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PROCESOS DE PARTO
# ═══════════════════════════════════════════════════════════════
PROCESO_PARTO_CONFIG = {
    'DILATACION_MINIMA_INICIO': 8,  # cm
    'TIMEOUT_CONFIRMACION': 60,     # segundos
    'DURACION_APEGO': 5,            # minutos
    'CODIGO_PREFIJO_PROCESO': 'MT',
    'CODIGO_PREFIJO_RN': 'RN',
}

# ═══════════════════════════════════════════════════════════════
# DEFAULT PRIMARY KEY
# ═══════════════════════════════════════════════════════════════
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### 2.2 Settings de Desarrollo

```python
# obstetric_care/settings/development.py

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Base de datos local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'obstetric_care',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
    'legacy': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital_legacy',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

DATABASE_ROUTERS = ['legacyApp.routers.LegacyRouter']

# Channels con In-Memory para desarrollo
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Cache local
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Email a consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS permisivo en desarrollo
CORS_ALLOW_ALL_ORIGINS = True

# Debug toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']
```

### 2.3 Settings de Producción

```python
# obstetric_care/settings/production.py

from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

SECRET_KEY = os.environ.get('SECRET_KEY')

# Base de datos de producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'ssl': {'ca': '/path/to/ca-cert.pem'},
        },
        'CONN_MAX_AGE': 600,
    },
    'legacy': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('LEGACY_DB_NAME'),
        'USER': os.environ.get('LEGACY_DB_USER'),
        'PASSWORD': os.environ.get('LEGACY_DB_PASSWORD'),
        'HOST': os.environ.get('LEGACY_DB_HOST'),
        'PORT': os.environ.get('LEGACY_DB_PORT', '3306'),
    }
}

DATABASE_ROUTERS = ['legacyApp.routers.LegacyRouter']

# Redis para Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.environ.get('REDIS_HOST', 'localhost'), 6379)],
        },
    },
}

# Cache con Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
    }
}

# Seguridad
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS restringido
CORS_ALLOWED_ORIGINS = [
    'https://obcare.hospital.cl',
]

# Logging a archivo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/obstetric_care/app.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/obstetric_care/error.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'obstetric_care': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

---

## 3. URLs Principales (urls.py)

```python
# obstetric_care/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ═══════════════════════════════════════════════════════════════
    # ADMINISTRACIÓN
    # ═══════════════════════════════════════════════════════════════
    path('admin/', admin.site.urls),
    
    # ═══════════════════════════════════════════════════════════════
    # AUTENTICACIÓN
    # ═══════════════════════════════════════════════════════════════
    path('', include('inicioApp.urls')),
    
    # ═══════════════════════════════════════════════════════════════
    # APLICACIONES PRINCIPALES
    # ═══════════════════════════════════════════════════════════════
    path('gestion/', include('gestionApp.urls', namespace='gestion')),
    path('matrona/', include('matronaApp.urls', namespace='matrona')),
    path('medico/', include('medicoApp.urls', namespace='medico')),
    path('tens/', include('tensApp.urls', namespace='tens')),
    path('ingreso-parto/', include('ingresoPartoApp.urls', namespace='ingreso_parto')),
    path('partos/', include('partosApp.urls', namespace='partos')),
    path('recien-nacido/', include('recienNacidoApp.urls', namespace='recien_nacido')),
    path('legacy/', include('legacyApp.urls', namespace='legacy')),
    
    # ═══════════════════════════════════════════════════════════════
    # GESTIÓN DE PROCESOS (NUEVO)
    # ═══════════════════════════════════════════════════════════════
    path('procesos/', include('gestionProcesosApp.urls', namespace='procesos')),
    
    # ═══════════════════════════════════════════════════════════════
    # CORE (Utilidades compartidas)
    # ═══════════════════════════════════════════════════════════════
    path('core/', include('core.urls', namespace='core')),
    
    # ═══════════════════════════════════════════════════════════════
    # API REST
    # ═══════════════════════════════════════════════════════════════
    path('api/v1/', include('core.api.urls', namespace='api')),
    path('api/auth/', include('rest_framework.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Personalización del admin
admin.site.site_header = 'OB-CARE Administración'
admin.site.site_title = 'OB-CARE Admin'
admin.site.index_title = 'Panel de Administración'
```

---

## 4. ASGI y WebSocket (asgi.py)

```python
# obstetric_care/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings.production')

# Inicializar Django ASGI application primero
django_asgi_app = get_asgi_application()

# Importar routing después de inicializar Django
from obstetric_care.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # HTTP requests
    "http": django_asgi_app,
    
    # WebSocket requests
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
```

### 4.1 Routing WebSocket

```python
# obstetric_care/routing.py

from django.urls import re_path
from gestionProcesosApp.consumers import ProcesoConsumer, SalasConsumer

websocket_urlpatterns = [
    # WebSocket para un proceso específico
    re_path(r'ws/proceso/(?P<codigo>\w+)/$', ProcesoConsumer.as_asgi()),
    
    # WebSocket para estado de salas (dashboard)
    re_path(r'ws/salas/$', SalasConsumer.as_asgi()),
]
```

---

## 5. WSGI (wsgi.py)

```python
# obstetric_care/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings.production')

application = get_wsgi_application()
```

---

## 6. Variables de Entorno

### 6.1 Archivo .env de Ejemplo

```bash
# .env.example

# ═══════════════════════════════════════════════════════════════
# DJANGO
# ═══════════════════════════════════════════════════════════════
DJANGO_SETTINGS_MODULE=obstetric_care.settings.development
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ═══════════════════════════════════════════════════════════════
# BASE DE DATOS PRINCIPAL
# ═══════════════════════════════════════════════════════════════
DB_NAME=obstetric_care
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3306

# ═══════════════════════════════════════════════════════════════
# BASE DE DATOS LEGACY
# ═══════════════════════════════════════════════════════════════
LEGACY_DB_NAME=hospital_legacy
LEGACY_DB_USER=readonly_user
LEGACY_DB_PASSWORD=readonly_password
LEGACY_DB_HOST=legacy-server.hospital.cl
LEGACY_DB_PORT=3306

# ═══════════════════════════════════════════════════════════════
# REDIS
# ═══════════════════════════════════════════════════════════════
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_URL=redis://localhost:6379/1

# ═══════════════════════════════════════════════════════════════
# CELERY
# ═══════════════════════════════════════════════════════════════
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# ═══════════════════════════════════════════════════════════════
# FIREBASE (Push Notifications)
# ═══════════════════════════════════════════════════════════════
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json

# ═══════════════════════════════════════════════════════════════
# EMAIL
# ═══════════════════════════════════════════════════════════════
EMAIL_HOST=smtp.hospital.cl
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@hospital.cl
EMAIL_HOST_PASSWORD=email_password
EMAIL_USE_TLS=True
```

---

## 7. Base de Datos

### 7.1 Diagrama de Bases de Datos

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ARQUITECTURA DE DATOS                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────┐      ┌─────────────────────────┐      │
│  │                         │      │                         │      │
│  │    obstetric_care       │      │    hospital_legacy      │      │
│  │    (Base Principal)     │      │    (Solo Lectura)       │      │
│  │                         │      │                         │      │
│  │  - Pacientes            │      │  - Controles previos    │      │
│  │  - Personal             │      │  - Historial médico     │      │
│  │  - Fichas obstétricas   │      │  - Exámenes antiguos    │      │
│  │  - Procesos de parto    │      │                         │      │
│  │  - Recién nacidos       │      │                         │      │
│  │  - Catálogos            │      │                         │      │
│  │  - Auditoría            │      │                         │      │
│  │                         │      │                         │      │
│  └───────────┬─────────────┘      └───────────┬─────────────┘      │
│              │                                │                     │
│              │         LegacyRouter           │                     │
│              │    (Solo lectura, managed=False)                     │
│              │                                │                     │
│              └────────────────┬───────────────┘                     │
│                               │                                     │
│                               ▼                                     │
│                    ┌─────────────────────┐                         │
│                    │   Django ORM        │                         │
│                    │   (Router Auto)     │                         │
│                    └─────────────────────┘                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 Comandos de Migración

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones (solo a base principal)
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations

# Migración específica de una app
python manage.py migrate gestionProcesosApp
```

---

## 8. Configuración de Apps

### 8.1 Orden de Apps

| Orden | App | Descripción |
|-------|-----|-------------|
| 1 | `core` | Utilidades compartidas, mixins, decoradores |
| 2 | `gestionApp` | Personas, Pacientes, Personal base |
| 3 | `matronaApp` | Fichas obstétricas, medicamentos |
| 4 | `medicoApp` | Patologías CIE-10 |
| 5 | `tensApp` | Signos vitales, tratamientos |
| 6 | `ingresoPartoApp` | Ficha de ingreso a parto |
| 7 | `partosApp` | Registro de parto (9 pasos) |
| 8 | `recienNacidoApp` | Registro de recién nacido |
| 9 | `gestionProcesosApp` | Flujos de proceso de parto |
| 10 | `legacyApp` | Integración sistema heredado |
| 11 | `inicioApp` | Autenticación, dashboards |

---

## 9. Middleware

### 9.1 Middleware Personalizado

```python
# core/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class LoginRequiredMiddleware:
    """Requiere login para todas las vistas excepto las públicas"""
    
    EXEMPT_URLS = [
        '/login/',
        '/logout/',
        '/admin/',
        '/static/',
        '/media/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            
            if not any(path.startswith(url) for url in self.EXEMPT_URLS):
                return redirect(f"{reverse('login')}?next={path}")
        
        return self.get_response(request)


class RoleMiddleware:
    """Agrega información de rol al request"""
    
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
        
        return self.get_response(request)
```

---

## 10. Configuración de Seguridad

### 10.1 Headers de Seguridad

```python
# En producción (settings/production.py)

# HTTPS obligatorio
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookies seguras
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Otros headers
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
```

### 10.2 CSRF

```python
# Dominios confiables para CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://obcare.hospital.cl',
    'https://*.hospital.cl',
]
```

---

## 11. Archivos Estáticos y Media

### 11.1 Estructura

```
project_root/
├── static/                  # Archivos estáticos de desarrollo
│   ├── css/
│   │   └── custom.css
│   ├── js/
│   │   ├── main.js
│   │   └── websocket.js
│   └── img/
│       └── logo.png
├── staticfiles/             # Archivos recolectados (collectstatic)
└── media/                   # Archivos subidos por usuarios
    ├── documentos/
    └── huellas/
```

### 11.2 Collectstatic

```bash
# Recolectar archivos estáticos para producción
python manage.py collectstatic --noinput
```

---

## 12. Logging

### 12.1 Configuración de Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/obstetric_care/app.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'proceso_parto': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/obstetric_care/procesos.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'gestionProcesosApp': {
            'handlers': ['console', 'proceso_parto'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

---

## 13. Celery (Tareas Asíncronas)

### 13.1 Configuración de Celery

```python
# obstetric_care/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings.production')

app = Celery('obstetric_care')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configuración
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Santiago',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    worker_prefetch_multiplier=1,
)
```

### 13.2 Tareas del Sistema

```python
# gestionProcesosApp/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def verificar_confirmaciones_timeout():
    """
    Tarea periódica que verifica confirmaciones pendientes
    y escala si pasó el timeout de 60 segundos.
    """
    from .models import ProcesoParto, ConfirmacionPersonal
    
    ahora = timezone.now()
    timeout = timedelta(seconds=60)
    
    # Buscar procesos con confirmaciones pendientes
    procesos = ProcesoParto.objects.filter(
        estado__codigo='INICIADO',
        hora_notificaciones__lte=ahora - timeout
    )
    
    for proceso in procesos:
        pendientes = proceso.confirmaciones.filter(confirmado=False)
        for conf in pendientes:
            buscar_reemplazo.delay(conf.id)


@shared_task
def buscar_reemplazo(confirmacion_id):
    """Busca reemplazo para una confirmación que no llegó"""
    from .models import ConfirmacionPersonal
    from .services import PersonalService, NotificacionService
    
    confirmacion = ConfirmacionPersonal.objects.get(id=confirmacion_id)
    
    # Buscar reemplazo disponible
    reemplazo = PersonalService.buscar_disponibles(
        confirmacion.rol.grupo_django, 
        cantidad=1
    )
    
    if reemplazo:
        # Crear nueva confirmación como reemplazo
        nueva = ConfirmacionPersonal.objects.create(
            proceso=confirmacion.proceso,
            profesional=reemplazo[0],
            rol=confirmacion.rol,
            hora_notificacion=timezone.now(),
            es_reemplazo=True,
            reemplaza_a=confirmacion
        )
        
        # Notificar al reemplazo
        NotificacionService.enviar_notificacion_proceso(
            confirmacion.proceso,
            reemplazo[0],
            confirmacion.rol
        )


@shared_task
def limpiar_salas():
    """Marca salas en limpieza como disponibles después de tiempo establecido"""
    from .models import SalaParto
    
    tiempo_limpieza = timedelta(minutes=15)
    ahora = timezone.now()
    
    salas = SalaParto.objects.filter(
        estado__codigo='LIMPIEZA',
        updated_at__lte=ahora - tiempo_limpieza
    )
    
    for sala in salas:
        sala.marcar_disponible()
```

### 13.3 Celery Beat (Tareas Programadas)

```python
# En settings
CELERY_BEAT_SCHEDULE = {
    'verificar-confirmaciones': {
        'task': 'gestionProcesosApp.tasks.verificar_confirmaciones_timeout',
        'schedule': 10.0,  # Cada 10 segundos
    },
    'limpiar-salas': {
        'task': 'gestionProcesosApp.tasks.limpiar_salas',
        'schedule': 60.0,  # Cada minuto
    },
}
```

---

## 14. Despliegue

### 14.1 Docker Compose

```yaml
# docker-compose.yml

version: '3.8'

services:
  web:
    build: .
    command: daphne -b 0.0.0.0 -p 8000 obstetric_care.asgi:application
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
    
  db:
    image: mysql:8.0
    volumes:
      - mysql_data:/var/lib/mysql
    environment:
      MYSQL_DATABASE: obstetric_care
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
    ports:
      - "3306:3306"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  celery:
    build: .
    command: celery -A obstetric_care worker -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
  
  celery-beat:
    build: .
    command: celery -A obstetric_care beat -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

volumes:
  mysql_data:
  static_volume:
  media_volume:
```

### 14.2 Dockerfile

```dockerfile
# Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Recolectar estáticos
RUN python manage.py collectstatic --noinput

# Puerto
EXPOSE 8000

# Comando por defecto
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "obstetric_care.asgi:application"]
```

### 14.3 Nginx

```nginx
# nginx.conf

upstream obstetric_care {
    server web:8000;
}

server {
    listen 80;
    server_name obcare.hospital.cl;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name obcare.hospital.cl;
    
    ssl_certificate /etc/ssl/certs/hospital.crt;
    ssl_certificate_key /etc/ssl/private/hospital.key;
    
    location /static/ {
        alias /app/staticfiles/;
    }
    
    location /media/ {
        alias /app/media/;
    }
    
    location /ws/ {
        proxy_pass http://obstetric_care;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
    
    location / {
        proxy_pass http://obstetric_care;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📊 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ARQUITECTURA OB-CARE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌─────────┐     ┌─────────┐     ┌─────────┐                     │
│    │ Browser │     │ Mobile  │     │ Push    │                     │
│    │  (Web)  │     │  App    │     │ Client  │                     │
│    └────┬────┘     └────┬────┘     └────┬────┘                     │
│         │               │               │                           │
│         └───────────────┴───────────────┘                           │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                               │
│              │      Nginx          │                               │
│              │  (Reverse Proxy)    │                               │
│              └──────────┬──────────┘                               │
│                         │                                           │
│         ┌───────────────┼───────────────┐                          │
│         │               │               │                          │
│         ▼               ▼               ▼                          │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐                     │
│   │  Daphne   │  │  Daphne   │  │  Daphne   │                     │
│   │  (ASGI)   │  │  (ASGI)   │  │  (ASGI)   │                     │
│   └─────┬─────┘  └─────┬─────┘  └─────┬─────┘                     │
│         │               │               │                          │
│         └───────────────┴───────────────┘                          │
│                         │                                           │
│         ┌───────────────┴───────────────┐                          │
│         │                               │                          │
│         ▼                               ▼                          │
│   ┌───────────┐                  ┌───────────┐                     │
│   │   MySQL   │                  │   Redis   │                     │
│   │  (Data)   │                  │  (Cache/  │                     │
│   │           │                  │  Channels)│                     │
│   └───────────┘                  └───────────┘                     │
│                                                                     │
│   ┌───────────┐                  ┌───────────┐                     │
│   │  Celery   │                  │  Firebase │                     │
│   │ (Workers) │                  │   (Push)  │                     │
│   └───────────┘                  └───────────┘                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

*Documentación obstetric_care (Proyecto Principal) - OB_CARE v1.0*
