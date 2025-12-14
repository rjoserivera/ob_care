from django.urls import path
from . import views
from . import views_notificaciones

app_name = 'gestion_procesos'

urlpatterns = [
    path('mis-notificaciones/', views.mis_notificaciones, name='mis_notificaciones'),
    path('test-notificacion/', views.crear_notificacion_prueba, name='test_notificacion'),
    path('api/check-notificaciones/', views.check_nuevas_notificaciones, name='check_nuevas_notificaciones'),
    path('api/notificacion/<int:notificacion_id>/confirmar/', views.confirmar_asistencia, name='confirmar_asistencia'),
    
    # Nuevo sistema de notificaciones
    path('notificaciones/', views_notificaciones.pagina_notificaciones, name='notificaciones'),
    path('api/notificaciones/personal/', views_notificaciones.obtener_notificaciones_ajax, name='notificaciones_ajax'),
]
