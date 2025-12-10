"""
recienNacidoApp/urls.py
URLs para recienNacidoApp - Registro de recién nacido
"""

from django.urls import path
from . import views

app_name = 'recien_nacido'

urlpatterns = [
    # Menu principal
    path('', views.menu_recien_nacido, name='menu_recien_nacido'),
    
    # Pasos del registro de RN
    path('crear/<int:registro_parto_pk>/paso1/', views.crear_registro_rn_paso1, name='crear_rn_paso1'),
    path('paso2/', views.crear_registro_rn_paso2, name='crear_rn_paso2'),
    path('paso3/', views.crear_registro_rn_paso3, name='crear_rn_paso3'),
    path('paso4/', views.crear_registro_rn_paso4, name='crear_rn_paso4'),
    path('paso5/', views.crear_registro_rn_paso5, name='crear_rn_paso5'),
    path('paso6/', views.crear_registro_rn_paso6, name='crear_rn_paso6'),
    path('paso7/', views.crear_registro_rn_paso7, name='crear_rn_paso7'),
    path('paso8/', views.crear_registro_rn_paso8, name='crear_rn_paso8'),
    path('paso9/', views.crear_registro_rn_paso9, name='crear_rn_paso9'),
    
    # Detalle y lista
    path('registro/<int:registro_rn_pk>/', views.detalle_registro_rn, name='detalle_registro_rn'),
    path('registros/', views.lista_registros_rn, name='lista_registros'),
]