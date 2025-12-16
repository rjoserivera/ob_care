from django.urls import path
from . import views
from medicoApp import views as medico_views
from matronaApp import views as matrona_views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    
    # Dashboards por rol
    path('dashboard/admin/', views.DashboardAdminView.as_view(), name='dashboard_admin'),
    path('dashboard/medico/', medico_views.DashboardMedicoView.as_view(), name='dashboard_medico'),
    path('dashboard/matrona/', matrona_views.DashboardMatronaView.as_view(), name='dashboard_matrona'),
    path('dashboard/tens/', views.DashboardTensView.as_view(), name='dashboard_tens'),
    
    # Registro de usuarios
    path('registro/', views.registro_usuario, name='registro_usuario'),
]
