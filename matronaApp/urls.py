"""
matronaApp/urls.py
URLs para matronaApp
ACTUALIZADO: Incluye rutas para dilatación, parto, APIs AJAX
"""

from django.urls import path
from . import views
from . import views_simple_invitations as views_simple
from . import views_limpiar

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
    path('ficha/<int:ficha_pk>/proceso-parto-iniciado/', views.proceso_parto_iniciado, name='proceso_parto_iniciado'),
    path('sala/<int:ficha_parto_id>/', views.sala_parto_view, name='sala_parto'),
    path('sala/<int:ficha_parto_id>/guardar/', views.guardar_registro_parto, name='guardar_parto'),
    path('sala/<int:ficha_parto_id>/guardar-rn/', views.guardar_registro_rn, name='guardar_rn'),
    
    # ==================== APIs AJAX ====================
    # Dilatación
    path('api/ficha/<int:ficha_pk>/dilatacion/agregar/', views.agregar_registro_dilatacion, name='api_agregar_dilatacion'),
    path('api/ficha/<int:ficha_pk>/dilatacion/estado/', views.verificar_estado_dilatacion, name='api_estado_dilatacion'),
    path('api/ficha/<int:ficha_id>/dilatacion/registrar/', views.registrar_dilatacion, name='registrar_dilatacion'),
    
    # Medicamentos AJAX
    path('api/ficha/<int:ficha_pk>/medicamento/agregar/', views.agregar_medicamento_ajax, name='api_agregar_medicamento'),
    path('api/medicamento/<int:medicamento_pk>/eliminar/', views.eliminar_medicamento_ajax, name='api_eliminar_medicamento'),
    
    # Personal
    path('api/ficha/<int:ficha_pk>/personal/', views.obtener_personal_requerido, name='api_personal_requerido'),
    path('api/asignar-personal/<int:ficha_parto_id>/', views.asignar_personal_parto, name='asignar_personal_parto'),
    path('api/invitar-rol/<int:ficha_parto_id>/', views_simple.invitar_personal_rol, name='invitar_personal_rol'),
    path('api/limpiar-invitaciones/<int:ficha_parto_id>/', views_limpiar.limpiar_invitaciones_ajax, name='limpiar_invitaciones_ajax'),
    path('api/finalizar-asignacion/<int:ficha_parto_id>/', views.finalizar_asignacion_parto, name='finalizar_asignacion_parto'),
    path('api/responder-asignacion/<int:asignacion_id>/', views.responder_asignacion, name='responder_asignacion'),
    path('api/verificar-pin/<int:ficha_parto_id>/', views.verificar_pin, name='verificar_pin'),
    
    # DEBUG
    path('api/debug/rellenar-equipo/<int:ficha_parto_id>/', views.debug_rellenar_equipo, name='debug_rellenar_equipo'),
]