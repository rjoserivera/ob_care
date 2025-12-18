from django.urls import path
from . import views, views_logs
from .views_telegram import ConfigurarTelegramView, IniciarBotView, AsignarRolesView

app_name = 'gestion'

urlpatterns = [
    # PERSONAS
    path('profiles/new/', views.registrar_persona, name='registrar_persona'),
    path('profiles/<int:pk>/', views.detalle_persona, name='detalle_persona'),
    path('profiles/<int:pk>/edit/', views.editar_persona, name='editar_persona'),
    path('profiles/<int:pk>/disable/', views.desactivar_persona, name='desactivar_persona'),
    path('profiles/<int:pk>/enable/', views.activar_persona, name='activar_persona'),
    path('profiles/', views.persona_list, name='persona_list'),
    path('search/', views.buscar_persona, name='buscar_persona'),
    
    # API
    path('api/search/', views.api_buscar_persona, name='api_buscar_persona'),
    
    # TELEGRAM
    path('settings/notifications/', ConfigurarTelegramView.as_view(), name='configurar_telegram'),
    path('settings/notifications/start/', IniciarBotView.as_view(), name='iniciar_bot_telegram'),
    
    # ROLES
    path('settings/roles/', AsignarRolesView.as_view(), name='asignar_roles'),
    
    # LOGS
    path('activity/', views_logs.LogListView.as_view(), name='listar_logs'),
]