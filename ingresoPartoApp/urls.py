"""
ingresoPartoApp/urls.py
URLs para ingresoPartoApp - Con Sala de Espera
"""

from django.urls import path
from . import views

app_name = 'ingreso_parto'

urlpatterns = [
    # Menu principal
    path('', views.menu_ingreso_parto, name='menu'),
    
    # Sala de espera (NUEVO - antes de crear ficha)
    path('sala-espera/<int:ficha_obstetrica_pk>/', views.sala_espera_parto, name='sala_espera'),
    
    # Fichas de ingreso a parto
    path('ficha/crear/<int:ficha_obstetrica_pk>/', views.crear_ficha_parto, name='crear_ficha'),
    path('ficha/<int:ficha_parto_pk>/editar/', views.editar_ficha_parto, name='editar_ficha'),
    path('ficha/<int:ficha_parto_pk>/', views.detalle_ficha_parto, name='detalle_ficha'),
    path('fichas/', views.lista_fichas_parto, name='lista_fichas'),
]