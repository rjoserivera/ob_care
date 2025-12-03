# matronaApp/urls.py
"""
URLs para matronaApp - Gestión de Fichas Obstétricas
LIMPIO: Sin gestión de patología
"""

from django.urls import path
from . import views

app_name = 'matrona'

urlpatterns = [
    # ============================================
    # MENÚ PRINCIPAL
    # ============================================
    path('', views.menu_matrona, name='menu_matrona'),

    # ============================================
    # FICHAS OBSTÉTRICAS
    # ============================================
    
    # Seleccionar persona para crear ficha
    path('ficha/seleccionar-persona/', 
         views.seleccionar_persona_ficha, 
         name='seleccionar_persona_ficha'),
    
    # Crear ficha obstétrica (crea automáticamente Paciente + Ingreso)
    path('persona/<int:persona_pk>/ficha/crear/', 
         views.crear_ficha_obstetrica, 
         name='crear_ficha'),
    
    # Listar fichas de una persona
    path('persona/<int:persona_pk>/fichas/', 
         views.lista_fichas_persona, 
         name='lista_fichas_persona'),
    
    # Detalle de ficha
    path('ficha/<int:ficha_pk>/', 
         views.detalle_ficha, 
         name='detalle_ficha'),
    
    # Editar ficha
    path('ficha/<int:ficha_pk>/editar/', 
         views.editar_ficha, 
         name='editar_ficha'),
    
    # Listar todas las fichas
    path('fichas/', 
         views.lista_todas_fichas, 
         name='todas_fichas'),

    # ============================================
    # MEDICAMENTOS EN FICHA
    # ============================================
    
    path('ficha/<int:ficha_pk>/medicamento/agregar/', 
         views.agregar_medicamento_ficha, 
         name='agregar_medicamento'),
    
    path('medicamento/<int:medicamento_pk>/editar/', 
         views.editar_medicamento_ficha, 
         name='editar_medicamento'),
    
    path('medicamento/<int:medicamento_pk>/eliminar/', 
         views.eliminar_medicamento_ficha, 
         name='eliminar_medicamento'),

    # ============================================
    # BÚSQUEDA API
    # ============================================
    
    path('api/persona/buscar/', 
         views.buscar_persona_api, 
         name='api_buscar_persona'),
]