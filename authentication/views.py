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
    """
    DEPRECATED: Esta vista redirige al dashboard principal de médico
    Usar directamente /medico/ en lugar de /dashboard/medico/
    """
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or user_has_role(request.user, "medicos")):
            messages.error(request, "No tienes permisos para acceder al dashboard médico.")
            return redirect("home")
        # Redirigir a la vista correcta con todas las funcionalidades
        return redirect("medico:menu_medico")


@method_decorator(login_required, name='dispatch')
class DashboardMatronaView(TemplateView):
    """
    DEPRECATED: Esta vista redirige al dashboard principal de matrona
    Usar directamente /matrona/ en lugar de /dashboard/matrona/
    """
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or user_has_role(request.user, "matronas")):
            messages.error(request, "No tienes permisos para acceder al dashboard de matrona.")
            return redirect("home")
        # Redirigir a la vista correcta con todas las funcionalidades
        return redirect("matrona:menu_matrona")


@method_decorator(login_required, name='dispatch')
class DashboardTensView(TemplateView):
    """
    DEPRECATED: Esta vista redirige al dashboard principal de TENS
    Usar directamente /tens/ en lugar de /dashboard/tens/
    """
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or user_has_role(request.user, "tens")):
            messages.error(request, "No tienes permisos para acceder al dashboard TENS.")
            return redirect("home")
        # Redirigir a la vista correcta con todas las funcionalidades
        return redirect("tens:menu_tens")