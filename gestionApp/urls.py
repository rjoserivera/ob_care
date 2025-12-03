from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # PERSONAS
    path('registrar-persona/', views.registrar_persona, name='registrar_persona'),
    path('persona/<int:pk>/', views.detalle_persona, name='detalle_persona'),
    path('persona/<int:pk>/editar/', views.editar_persona, name='editar_persona'),
    path('persona/<int:pk>/desactivar/', views.desactivar_persona, name='desactivar_persona'),
    path('persona/<int:pk>/activar/', views.activar_persona, name='activar_persona'),
    path('personas/', views.persona_list, name='persona_list'),
    path('buscar-persona/', views.buscar_persona, name='buscar_persona'),
    
    # API
    path('api/buscar-persona/', views.api_buscar_persona, name='api_buscar_persona'),
]