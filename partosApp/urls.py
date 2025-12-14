"""
partosApp/urls.py
URLs para partosApp - Registro de partos
"""

from django.urls import path
from . import views

app_name = 'partos'

urlpatterns = [
    # Menu principal
    path('', views.menu_partos, name='menu_partos'),
    
    # Pasos del registro de parto
    path('registro/<int:ficha_parto_pk>/paso1/', views.crear_registro_parto_paso1, name='crear_registro_parto_paso1'),
    path('registro/paso2/', views.crear_registro_parto_paso2, name='crear_registro_parto_paso2'),
    path('registro/paso3/', views.crear_registro_parto_paso3, name='crear_registro_parto_paso3'),
    path('registro/paso4/', views.crear_registro_parto_paso4, name='crear_registro_parto_paso4'),
    path('registro/paso5/', views.crear_registro_parto_paso5, name='crear_registro_parto_paso5'),
    path('registro/paso6/', views.crear_registro_parto_paso6, name='crear_registro_parto_paso6'),
    path('registro/paso7/', views.crear_registro_parto_paso7, name='crear_registro_parto_paso7'),
    path('registro/paso8/', views.crear_registro_parto_paso8, name='crear_registro_parto_paso8'),
    path('registro/paso9/', views.crear_registro_parto_paso9, name='crear_registro_parto_paso9'),
    
    # Detalle y lista
    path('registro/<int:registro_pk>/', views.detalle_registro_parto, name='detalle_registro'),
    path('registros/', views.lista_registros_parto, name='lista_registros'),
]