# gestionApp/urls.py
"""
URLs para gestionApp - Gestión de Personas
"""

from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # ============================================
    # PERSONAS
    # ============================================
    
    # Listar personas
    path('personas/', 
         views.persona_list, 
         name='persona_list'),
    
    # Registrar nueva persona
    path('persona/registrar/', 
         views.registrar_persona, 
         name='registrar_persona'),
    
    # Detalle de persona
    path('persona/<int:pk>/', 
         views.detalle_persona, 
         name='detalle_persona'),
    
    # Editar persona
    path('persona/<int:pk>/editar/', 
         views.editar_persona, 
         name='editar_persona'),
    
    # Desactivar persona
    path('persona/<int:pk>/desactivar/', 
         views.desactivar_persona, 
         name='desactivar_persona'),
    
    # Activar persona
    path('persona/<int:pk>/activar/', 
         views.activar_persona, 
         name='activar_persona'),
    
    # Buscar persona
    path('persona/buscar/', 
         views.buscar_persona, 
         name='buscar_persona'),
    
    # ============================================
    # API - BÚSQUEDA AJAX
    # ============================================
    
    path('api/persona/buscar/', 
         views.api_buscar_persona, 
         name='api_buscar_persona'),
]