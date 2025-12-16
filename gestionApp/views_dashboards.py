"""
gestionApp/views_dashboards.py - CORREGIDO para usar User + Groups
Vistas de dashboards por rol
"""

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User, Group

from .models import Paciente, Persona
from authentication.utils import user_has_role


# ═══════════════════════════════════════════════════════════════
# DASHBOARD MÉDICO
# ═══════════════════════════════════════════════════════════════

@method_decorator(login_required, name='dispatch')
class DashboardMedicoView(TemplateView):
    template_name = "Medico/Data/dashboard_medico.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not (user_has_role(request.user, "medico") or request.user.is_superuser):
            messages.error(request, "No tienes permisos para acceder al dashboard médico.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Dashboard Médico'
        context['usuario'] = self.request.user
        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        context['total_fichas'] = 0
        context['partos_pendientes'] = 0
        
        context['puede_agregar_paciente'] = True
        context['puede_editar_ficha'] = True
        context['puede_iniciar_parto'] = True
        context['puede_asignar_medicamentos'] = True
        context['puede_ver_historial'] = True
        
        return context


# ═══════════════════════════════════════════════════════════════
# DASHBOARD MATRONA
# ═══════════════════════════════════════════════════════════════

@method_decorator(login_required, name='dispatch')
class DashboardMatronaView(TemplateView):
    template_name = "Matrona/Data/dashboard_matrona.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not (user_has_role(request.user, "matrona") or request.user.is_superuser):
            messages.error(request, "No tienes permisos para acceder al dashboard de matrona.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Dashboard Matrona'
        context['usuario'] = self.request.user
        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        
        from matronaApp.models import FichaObstetrica
        context['fichas_activas'] = FichaObstetrica.objects.filter(activa=True).count()
        
        context['puede_crear_ficha'] = True
        context['puede_registrar_ingreso'] = True
        context['puede_iniciar_parto'] = True
        
        return context


# ═══════════════════════════════════════════════════════════════
# DASHBOARD TENS
# ═══════════════════════════════════════════════════════════════

@method_decorator(login_required, name='dispatch')
class DashboardTensView(TemplateView):
    template_name = "Tens/Data/dashboard_tens.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not (user_has_role(request.user, "tens") or request.user.is_superuser):
            messages.error(request, "No tienes permisos para acceder al dashboard TENS.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Dashboard TENS'
        context['usuario'] = self.request.user
        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        
        from matronaApp.models import FichaObstetrica, AdministracionMedicamento
        from django.utils import timezone
        
        hoy = timezone.now().date()
        context['fichas_activas'] = FichaObstetrica.objects.filter(activa=True).count()
        context['administraciones_hoy'] = AdministracionMedicamento.objects.filter(
            fecha_hora_administracion__date=hoy
        ).count()
        
        context['puede_registrar_signos'] = True
        context['puede_administrar_medicamentos'] = True
        
        return context


# ═══════════════════════════════════════════════════════════════
# DASHBOARD ADMINISTRADOR
# ═══════════════════════════════════════════════════════════════

@method_decorator(login_required, name='dispatch')
class DashboardAdminView(TemplateView):
    template_name = "Gestion/Data/dashboard_admin.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not (user_has_role(request.user, "administrador") or request.user.is_superuser):
            messages.error(request, "No tienes permisos para acceder al panel de administración.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['titulo'] = 'Panel de Administración'
        context['usuario'] = self.request.user
        
        # Conteos usando User + Groups
        from django.db.models import Q
        from matronaApp.models import FichaObstetrica

        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        context['total_personas'] = Persona.objects.filter(Activo=True).count()
        context['total_medicos'] = User.objects.filter(groups__name='Medicos', is_active=True).count()
        context['total_matronas'] = User.objects.filter(groups__name='Matronas', is_active=True).count()
        context['total_tens'] = User.objects.filter(groups__name='TENS', is_active=True).count()
        context['total_administradores'] = User.objects.filter(Q(groups__name='Administradores') | Q(is_superuser=True), is_active=True).distinct().count()
        
        context['total_fichas'] = FichaObstetrica.objects.filter(activa=True).count()
        context['total_usuarios'] = User.objects.filter(is_active=True).count()
        
        return context