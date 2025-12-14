"""
tensApp/urls.py
URLs del módulo TENS
"""

from django.urls import path
from . import views

app_name = 'tens'

urlpatterns = [
    # Menú principal
    path('', views.menu_tens, name='menu_tens'),
    
    # Buscar paciente
    path('buscar-paciente/', views.buscar_paciente_tens, name='buscar_paciente'),
    
    # Lista de fichas
    path('fichas/', views.lista_fichas_tens, name='lista_fichas'),
    path('ficha/<int:ficha_pk>/', views.detalle_ficha_tens, name='detalle_ficha'),
    
    # Signos vitales (parametros)
    path('parametros/', views.lista_fichas_tens, name='parametros_tens'),
    path('ficha/<int:ficha_pk>/signos/', views.registrar_signos_vitales, name='registrar_signos'),
    path('ficha/<int:ficha_pk>/historial/', views.historial_signos, name='historial_signos'),
    
    # Medicamentos
    path('medicamento/<int:medicamento_pk>/administrar/', views.administrar_medicamento, name='administrar_medicamento'),
    
    # Tratamientos
    path('ficha/<int:ficha_pk>/tratamiento/', views.registrar_tratamiento, name='registrar_tratamiento'),
]