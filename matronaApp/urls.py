"""
matronaApp/urls.py
URLs para matronaApp
Actualizado: Solo incluye vistas que existen
"""

from django.urls import path
from . import views

app_name = 'matrona'

urlpatterns = [
    # Menu principal
    path('', views.menu_matrona, name='menu_matrona'),
    
    # Fichas obstétricas
    path('ficha/crear/<int:paciente_pk>/', views.crear_ficha_obstetrica, name='crear_ficha'),
    path('ficha/<int:ficha_pk>/editar/', views.editar_ficha_obstetrica, name='editar_ficha'),
    path('ficha/<int:ficha_pk>/', views.detalle_ficha_obstetrica, name='detalle_ficha'),
    path('fichas/', views.lista_fichas_obstetrica, name='lista_fichas'),
    
    # Medicamentos
    path('ficha/<int:ficha_pk>/medicamento/agregar/', views.agregar_medicamento, name='agregar_medicamento'),
    path('medicamento/<int:medicamento_pk>/eliminar/', views.eliminar_medicamento, name='eliminar_medicamento'),
]