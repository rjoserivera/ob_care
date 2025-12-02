from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from inicioApp import views as inicio_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Página principal
    path('', inicio_views.home, name='home'),
    
    # Apps del sistema
    path('gestion/', include('gestionApp.urls')),
    path('matrona/', include('matronaApp.urls')),
    path('medico/', include('medicoApp.urls')),
    path('tens/', include('tensApp.urls')),
    path('partos/', include('partosApp.urls')), 
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]