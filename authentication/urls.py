from django.urls import path
from . import views
from medicoApp import views as medico_views
from matronaApp import views as matrona_views

app_name = 'authentication'

urlpatterns = [
    # Autenticación (ofuscado como acceso genérico)
    path('access/', views.CustomLoginView.as_view(), name='login'),
    path('exit/', views.custom_logout_view, name='logout'),
    
    # Dashboards por rol (ofuscados con hash - parecen URLs aleatorias)
    path('w3x9k7m2/', views.DashboardAdminView.as_view(), name='dashboard_admin'),
    path('p5n8j4q1/', medico_views.DashboardMedicoView.as_view(), name='dashboard_medico'),
    path('r2t6v9h3/', matrona_views.DashboardMatronaView.as_view(), name='dashboard_matrona'),
    path('l1w5d0y8/', views.DashboardTensView.as_view(), name='dashboard_tens'),
    
    # Registro de usuarios (ofuscado como "join")
    path('join/', views.registro_usuario, name='registro_usuario'),
]
