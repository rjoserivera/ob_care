"""
matronaApp/urls.py
URLs para matronaApp
ACTUALIZADO: Incluye rutas para dilatación, parto, APIs AJAX
"""

from django.urls import path
from . import views

app_name = 'matrona'

urlpatterns = [
    # ==================== MENÚ PRINCIPAL ====================
    path('', views.menu_matrona, name='menu_matrona'),
    
    # ==================== SELECCIONAR PERSONA ====================
    path('seleccionar-persona/', views.seleccionar_persona_ficha, name='seleccionar_persona_ficha'),
    
    # ==================== FICHAS OBSTÉTRICAS ====================
    # Crear ficha desde paciente existente
    path('ficha/crear/<int:paciente_pk>/', views.crear_ficha_obstetrica, name='crear_ficha'),
    
    # Crear ficha desde persona (crea paciente automáticamente)
    path('ficha/crear-persona/<int:persona_pk>/', views.crear_ficha_obstetrica_persona, name='crear_ficha_persona'),
    
    # Editar ficha
    path('ficha/<int:ficha_pk>/editar/', views.editar_ficha_obstetrica, name='editar_ficha'),
    
    # Detalle de ficha
    path('ficha/<int:ficha_pk>/', views.detalle_ficha_obstetrica, name='detalle_ficha'),
    
    # Lista de fichas
    path('fichas/', views.lista_fichas_obstetrica, name='lista_fichas'),
    
    # ==================== MEDICAMENTOS ====================
    path('ficha/<int:ficha_pk>/medicamento/agregar/', views.agregar_medicamento, name='agregar_medicamento'),
    path('medicamento/<int:medicamento_pk>/eliminar/', views.eliminar_medicamento, name='eliminar_medicamento'),
    
    # ==================== PARTO ====================
    path('ficha/<int:ficha_pk>/iniciar-parto/', views.iniciar_proceso_parto, name='iniciar_parto'),
    
    # ==================== APIs AJAX ====================
    # Dilatación
    path('api/ficha/<int:ficha_pk>/dilatacion/agregar/', views.agregar_registro_dilatacion, name='api_agregar_dilatacion'),
    path('api/ficha/<int:ficha_pk>/dilatacion/estado/', views.verificar_estado_dilatacion, name='api_estado_dilatacion'),
    
    # Medicamentos AJAX
    path('api/ficha/<int:ficha_pk>/medicamento/agregar/', views.agregar_medicamento_ajax, name='api_agregar_medicamento'),
    path('api/medicamento/<int:medicamento_pk>/eliminar/', views.eliminar_medicamento_ajax, name='api_eliminar_medicamento'),
    
    # Personal
    path('api/ficha/<int:ficha_pk>/personal/', views.obtener_personal_requerido, name='api_personal_requerido'),
]