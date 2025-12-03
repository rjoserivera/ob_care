from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from inicioApp import views as inicio_views

urlpatterns = [
    path('admin/', admin.site.urls),  # ← Admin de Django (para crear usuarios)
    
    # Página principal - SCREENSAVER
    path('', inicio_views.screensaver, name='home'),  # ✅ SCREENSAVER
    
    # Autenticación
    path('login/', views.CustomLoginView.as_view(), name='login'),  # ✅ LOGIN
    path('logout/', views.custom_logout_view, name='logout'),
    
    # Apps del sistema
    path('gestion/', include('gestionApp.urls')),
    path('matrona/', include('matronaApp.urls')),
    path('medico/', include('medicoApp.urls')),
    path('tens/', include('tensApp.urls')),
    path('partos/', include('partosApp.urls')), 
]