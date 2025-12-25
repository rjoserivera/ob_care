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
    path('select/', views.seleccionar_persona_ficha, name='seleccionar_persona_ficha'),
    
    # ==================== FICHAS OBSTÉTRICAS ====================
    path('case/new/<str:paciente_pk>/', views.crear_ficha_obstetrica, name='crear_ficha'),
    path('case/create/<str:persona_pk>/', views.crear_ficha_obstetrica_persona, name='crear_ficha_persona'),
    path('case/<str:ficha_pk>/edit/', views.editar_ficha_obstetrica, name='editar_ficha'),
    path('case/<str:ficha_pk>/', views.detalle_ficha_obstetrica, name='detalle_ficha'),
    path('cases/', views.lista_fichas_obstetrica, name='lista_fichas'),
    
    # API Polling Equipo
    path('api/process/<str:ficha_pk>/team-status/', views.equipo_confirmado_partial, name='equipo_confirmado_partial'),
    path('api/debug/fill-team/<str:ficha_parto_id>/', views.debug_rellenar_equipo, name='debug_rellenar_equipo'),
    
    # ==================== MEDICAMENTOS ====================
    path('case/<str:ficha_pk>/treatment/add/', views.agregar_medicamento, name='agregar_medicamento'),
    path('treatment/<str:medicamento_pk>/remove/', views.eliminar_medicamento, name='eliminar_medicamento'),
    
    # ==================== PARTO ====================
    path('case/<str:ficha_pk>/procedure/start/', views.iniciar_proceso_parto, name='iniciar_parto'),
    path('case/<str:ficha_pk>/procedure/active/', views.proceso_parto_iniciado, name='proceso_parto_iniciado'),
    path('case/<str:ficha_pk>/close/', views.cerrar_ficha_definitivamente, name='cerrar_ficha'),
    path('room/<str:ficha_parto_id>/', views.sala_parto_view, name='sala_parto'),
    path('room/<str:ficha_parto_id>/save/', views.guardar_registro_parto, name='guardar_registro_parto'),
    path('room/<str:ficha_parto_id>/save-newborn/', views.guardar_registro_rn, name='guardar_rn'),
    path('room/<str:ficha_parto_id>/close/', views.cierre_parto_view, name='cierre_parto'),
    path('room/<str:ficha_parto_id>/summary/', views.resumen_final_parto_view, name='resumen_final_parto'),
    path('room/<str:ficha_parto_id>/details/', views.detalle_registro_parto, name='detalle_registro_parto'),
    
    # ==================== RN ====================
    path('room/<str:ficha_parto_id>/link-patient/', views.crear_asociacion_rn, name='asociar_rn'),
    path('patient/<str:rn_id>/', views.ficha_rn_view, name='ficha_rn'),
    path('patient/<str:rn_id>/info/', views.detalle_rn_view, name='detalle_rn'),
    
    # ==================== HISTORIAL ====================
    path('history/', views.historial_partos_view, name='historial_partos'),
    
    # ==================== APIs AJAX ====================
    # Dilatación
    path('api/case/<str:ficha_pk>/progress/add/', views.agregar_registro_dilatacion, name='api_agregar_dilatacion'),
    path('api/case/<str:ficha_pk>/progress/status/', views.verificar_estado_dilatacion, name='api_estado_dilatacion'),
    path('api/case/<str:ficha_id>/progress/register/', views.registrar_dilatacion, name='registrar_dilatacion'),
    
    # Medicamentos AJAX
    path('api/case/<str:ficha_pk>/treatment/add/', views.agregar_medicamento_ajax, name='api_agregar_medicamento'),
    path('api/treatment/<str:medicamento_pk>/remove/', views.eliminar_medicamento_ajax, name='api_eliminar_medicamento'),
    
    # Administración Medicamentos
    path('api/treatment/<str:medicamento_id>/doses/', views.obtener_administraciones, name='api_obtener_administraciones'),
    path('api/treatment/<str:medicamento_id>/administer/', views.registrar_administracion, name='api_registrar_administracion'),
    
    # Personal
    path('api/case/<str:ficha_pk>/staff/', views.obtener_personal_requerido, name='api_personal_requerido'),
    path('api/assign-staff/<str:ficha_parto_id>/', views.asignar_personal_parto, name='asignar_personal_parto'),
    path('api/invite-role/<str:ficha_parto_id>/', views_simple.invitar_personal_rol, name='invitar_personal_rol'),
    path('api/clear-invites/<str:ficha_parto_id>/', views_limpiar.limpiar_invitaciones_ajax, name='limpiar_invitaciones_ajax'),
    path('api/finalize-assignment/<str:ficha_parto_id>/', views.finalizar_asignacion_parto, name='finalizar_asignacion_parto'),
    path('api/respond-assignment/<str:asignacion_id>/', views.responder_asignacion, name='responder_asignacion'),
    path('api/verify-pin/<str:ficha_parto_id>/', views.verificar_pin, name='verificar_pin'),
    path('api/resend-pin/<str:ficha_parto_id>/', views.reenviar_pin, name='reenviar_pin'),
    
    # DEBUG
    path('api/debug/fill-team/<str:ficha_parto_id>/', views.debug_rellenar_equipo, name='debug_rellenar_equipo'),
]