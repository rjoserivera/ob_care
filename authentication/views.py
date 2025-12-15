"""
authentication/views.py - CORREGIDO para usar User + Groups
Sistema de autenticación y dashboards por rol
"""

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group

# Importar modelos para conteos
from gestionApp.models import Paciente, Persona
from .utils import user_has_role, get_dashboard_url_for_user


# ─────────────────────────────────────────────
# LOGIN / LOGOUT
# ─────────────────────────────────────────────

class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        destino = get_dashboard_url_for_user(self.request.user)
        return destino if destino else reverse_lazy("home")


def custom_logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("home")


# ─────────────────────────────────────────────
# DASHBOARDS POR ROL
# ─────────────────────────────────────────────

@method_decorator(login_required, name='dispatch')
class DashboardAdminView(TemplateView):
    template_name = "Gestion/Data/dashboard_admin.html"

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or user_has_role(request.user, "administradores")):
            messages.error(request, "No tienes permisos para acceder al panel de administración.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Panel de Administración'
        context['usuario'] = self.request.user
        
        # Conteos usando User + Groups
        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        context['total_medicos'] = User.objects.filter(groups__name='Medicos', is_active=True).count()
        context['total_matronas'] = User.objects.filter(groups__name='Matronas', is_active=True).count()
        context['total_tens'] = User.objects.filter(groups__name='TENS', is_active=True).count()
        context['total_usuarios'] = User.objects.filter(is_active=True).count()
        
        return context


@method_decorator(login_required, name='dispatch')
class DashboardMedicoView(TemplateView):
    template_name = "Medico/Data/dashboard_medico.html"

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or user_has_role(request.user, "medicos")):
            messages.error(request, "No tienes permisos para acceder al dashboard médico.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Dashboard Médico'
        context['usuario'] = self.request.user
        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        
        # Permisos
        context['puede_agregar_paciente'] = True
        context['puede_editar_ficha'] = True
        context['puede_iniciar_parto'] = True
        
        return context


@method_decorator(login_required, name='dispatch')
class DashboardMatronaView(TemplateView):
    template_name = "Matrona/Data/dashboard_matrona.html"

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or user_has_role(request.user, "matronas")):
            messages.error(request, "No tienes permisos para acceder al dashboard de matrona.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Dashboard Matrona'
        context['usuario'] = self.request.user
        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        
        # Importar aquí para evitar import circular
        from matronaApp.models import FichaObstetrica
        context['fichas_activas'] = FichaObstetrica.objects.filter(activa=True).count()
        
        return context


@method_decorator(login_required, name='dispatch')
class DashboardTensView(TemplateView):
    template_name = "Tens/Data/dashboard_tens.html"

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or user_has_role(request.user, "tens")):
            messages.error(request, "No tienes permisos para acceder al dashboard TENS.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Dashboard TENS'
        context['usuario'] = self.request.user
        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        
        return context