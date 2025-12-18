from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from inicioApp import views as inicio_views

urlpatterns = [
    # Panel de administración Django (ofuscado)
    path('n5p8r3t7/', admin.site.urls),
    
    # Página principal
    path('', inicio_views.home, name='home'),
    
    # Apps del sistema (semi-legibles para compatibilidad)
    path('portal/', include('gestionApp.urls')),
    path('services/', include('matronaApp.urls')),
    path('resources/', include('medicoApp.urls')),
    path('support/', include('tensApp.urls')),
    path('records/', include('partosApp.urls')),
    path('workflow/', include('ingresoPartoApp.urls')),
    path('management/', include('gestionProcesosApp.urls')),
    
    # Autenticación
    path('', include('authentication.urls')),
]

# ✅ DEBUG TOOLBAR (Solo en desarrollo) - DESACTIVADO
# if settings.DEBUG:
#     urlpatterns += [
#         path('__debug__/', include('debug_toolbar.urls')),
#     ]

