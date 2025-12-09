# ═══════════════════════════════════════════════════════════════
# authentication/views.py - ARCHIVO COMPLETO PARA REEMPLAZAR
# ═══════════════════════════════════════════════════════════════

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Importar modelos para conteos
from gestionApp.models import Paciente, Medico, Matrona, Tens, Persona
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
        if not (request.user.is_superuser or user_has_role(request.user, "administrador")):
            messages.error(request, "No tienes permisos.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Dashboard Administrador'
        context['usuario'] = self.request.user
        
        # ═══════════════════════════════════════════════════════════════
        # CONTEOS DE PERSONAL Y PACIENTES ACTIVOS
        # ═══════════════════════════════════════════════════════════════
        
        # Contar médicos activos (campo Activo con A mayúscula)
        context['total_medicos'] = Medico.objects.filter(Activo=True).count()
        
        # Contar matronas activas (campo Activo con A mayúscula)
        context['total_matronas'] = Matrona.objects.filter(Activo=True).count()
        
        # Contar TENS activos (campo Activo con A mayúscula)
        context['total_tens'] = Tens.objects.filter(Activo=True).count()
        
        # Contar pacientes activos (campo activo con a minúscula)
        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        
        # Contar administradores (superusuarios activos)
        context['total_admins'] = User.objects.filter(is_superuser=True, is_active=True).count()
        
        # Total de personas registradas
        context['total_personas'] = Persona.objects.filter(Activo=True).count()
        
        # Total general (suma de todo)
        context['total_general'] = (
            context['total_medicos'] + 
            context['total_matronas'] + 
            context['total_tens'] + 
            context['total_pacientes'] + 
            context['total_admins']
        )
        
        return context


@method_decorator(login_required, name='dispatch')
class DashboardMedicoView(TemplateView):
    template_name = "Medico/Data/dashboard_medico.html"

    def dispatch(self, request, *args, **kwargs):
        if not user_has_role(request.user, "medico"):
            messages.error(request, "No tienes permisos.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Dashboard Médico'
        context['usuario'] = self.request.user
        return context


@method_decorator(login_required, name='dispatch')
class DashboardMatronaView(TemplateView):
    template_name = "Matrona/Data/dashboard_matrona.html"

    def dispatch(self, request, *args, **kwargs):
        if not user_has_role(request.user, "matrona"):
            messages.error(request, "No tienes permisos.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Dashboard Matrona'
        context['usuario'] = self.request.user
        return context


@method_decorator(login_required, name='dispatch')
class DashboardTensView(TemplateView):
    template_name = "Tens/Data/dashboard_tens.html"

    def dispatch(self, request, *args, **kwargs):
        if not user_has_role(request.user, "tens"):
            messages.error(request, "No tienes permisos.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Dashboard TENS'
        context['usuario'] = self.request.user
        return context