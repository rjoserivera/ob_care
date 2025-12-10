"""
URLs para medicoApp
Incluye gestión de patologías, fichas obstétricas y medicamentos
"""
from django.urls import path
from . import views

app_name = 'medico'

urlpatterns = [
    # ============================================
    # MENÚ PRINCIPAL
    # ============================================
    path('', views.menu_medico, name='menu_medico'),
    
    # ============================================
    # FICHAS OBSTÉTRICAS
    # ============================================
    path('ficha/crear/<int:paciente_pk>/', views.crear_ficha_obstetrica, name='crear_ficha'),
    path('ficha/crear-persona/<int:persona_pk>/', views.crear_ficha_obstetrica_persona, name='crear_ficha_persona'),
    path('ficha/<int:ficha_pk>/editar/', views.editar_ficha_obstetrica, name='editar_ficha'),
    path('ficha/<int:ficha_pk>/', views.detalle_ficha_obstetrica, name='detalle_ficha'),
    path('fichas/', views.lista_fichas_obstetrica, name='lista_fichas'),
    
    # ============================================
    # MEDICAMENTOS
    # ============================================
    path('ficha/<int:ficha_pk>/medicamento/agregar/', views.agregar_medicamento, name='agregar_medicamento'),
    path('medicamento/<int:medicamento_pk>/eliminar/', views.eliminar_medicamento, name='eliminar_medicamento'),
    path('seleccionar-persona/', views.seleccionar_persona_ficha, name='seleccionar_persona_ficha'),
    
    # ============================================
    # GESTIÓN DE PATOLOGÍAS
    # ============================================
    path('patologias/', views.listar_patologias, name='listar_patologias'),
    path('patologia/registrar/', views.registrar_patologia, name='registrar_patologia'),
    path('patologia/<int:pk>/', views.detalle_patologia, name='detalle_patologia'),
    path('patologia/<int:pk>/editar/', views.editar_patologia, name='editar_patologia'),
    path('patologia/<int:pk>/toggle/', views.toggle_patologia, name='toggle_patologia'),
    
    # ============================================
    # CONSULTA DE HISTORIAL CLÍNICO
    # ============================================
    path('paciente/buscar/', views.buscar_paciente_medico, name='buscar_paciente'),
    path('paciente/<int:paciente_pk>/historial/', views.ver_historial_clinico, name='historial_clinico'),
]