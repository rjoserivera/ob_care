from django.urls import path
from . import views
from . import views_notificaciones

app_name = 'gestion_procesos'

urlpatterns = [
    path('mis-notificaciones/', views.mis_notificaciones, name='mis_notificaciones'),
    path('test-notificacion/', views.crear_notificacion_prueba, name='test_notificacion'),
    path('api/check-notificaciones/', views.check_nuevas_notificaciones, name='check_nuevas_notificaciones'),
    path('api/notificacion/<int:notificacion_id>/confirmar/', views.confirmar_asistencia, name='confirmar_asistencia'),
    path('api/notificacion/<int:notificacion_id>/marcar-leida/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    
    # api endpoints
    path('api/responder-asignacion/<int:asignacion_id>/', views_notificaciones.responder_asignacion, name='responder_asignacion'),
    path('api/check-notificaciones/', views.check_nuevas_notificaciones, name='check_nuevas_notificaciones'),
    path('api/notificacion/<int:notificacion_id>/marcar-leida/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),

    
    # Admin Panel
    path('admin/panel-notificaciones/', views.panel_notificaciones_admin, name='panel_notificaciones_admin'),
]
