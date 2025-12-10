from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Paciente, Persona
from gestionApp.models import Medico, Matrona, Tens
from authentication.utils import user_has_role
from authentication.decorators import role_required, roles_required


# ═══════════════════════════════════════════════════════════════
# DASHBOARD MÉDICO
# ═══════════════════════════════════════════════════════════════

@method_decorator(login_required, name='dispatch')
class DashboardMedicoView(TemplateView):
    template_name = "Medico/Data/dashboard_medico.html"
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar que sea médico o administrador
        if not (user_has_role(request.user, "medico") or request.user.is_superuser):
            messages.error(request, "No tienes permisos para acceder al dashboard médico.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos para el dashboard médico
        context['titulo'] = 'Dashboard Médico'
        context['usuario'] = self.request.user
        context['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        context['total_fichas'] = 0  # Se obtendría de fichas activas
        context['partos_pendientes'] = 0  # Se obtendría de registros de parto pendientes
        
        # Permisos específicos del médico
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
        # Verificar que sea matrona o administrador
        if not (user_has_role(request.user, "matrona") or request.user.is_superuser):
            messages.error(request, "No tienes permisos para acceder al dashboard de matrona.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos para el dashboard matrona
        context['titulo'] = 'Dashboard Matrona'
        context['usuario'] = self.request.user
        context['total_ingresos'] = 0  # Se obtendría de ingresos de paciente
        context['total_medicamentos_asignados'] = 0  # Se obtendría de medicamentos
        
        # Permisos específicos de matrona
        context['puede_ingresar_paciente'] = True
        context['puede_asignar_medicamentos'] = True
        context['puede_buscar_paciente'] = True
        context['puede_editar_ficha'] = False  # Matrona NO puede editar todo
        context['puede_iniciar_parto'] = False  # Solo médico
        
        return context


# ═══════════════════════════════════════════════════════════════
# DASHBOARD TENS
# ═══════════════════════════════════════════════════════════════

@method_decorator(login_required, name='dispatch')
class DashboardTensView(TemplateView):
    template_name = "Tens/Data/dashboard_tens.html"
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar que sea TENS o administrador
        if not (user_has_role(request.user, "tens") or request.user.is_superuser):
            messages.error(request, "No tienes permisos para acceder al dashboard TENS.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos para el dashboard TENS
        context['titulo'] = 'Dashboard TENS'
        context['usuario'] = self.request.user
        context['total_tratamientos'] = 0  # Se obtendría de tratamientos aplicados
        context['total_registros_tens'] = 0  # Se obtendría de registros TENS
        
        # Permisos específicos de TENS
        context['puede_aplicar_tratamiento'] = True
        context['puede_registrar_tratamiento'] = True
        context['puede_buscar_paciente'] = True
        context['puede_asignar_medicamentos'] = False  # Solo médico y matrona
        context['puede_ver_historial'] = False  # Solo médico
        
        return context


# ═══════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES DE PERMISO
# ═══════════════════════════════════════════════════════════════

def tiene_permiso_ver_paciente(user, paciente):
    """
    Verifica si el usuario puede ver los datos de un paciente específico
    """
    if user.is_superuser or user_has_role(user, "administrador"):
        return True
    
    if user_has_role(user, "medico"):
        return True
    
    if user_has_role(user, "matrona"):
        return True
    
    if user_has_role(user, "tens"):
        return True
    
    return False


def tiene_permiso_editar_ficha(user):
    """
    Verifica si el usuario puede editar fichas
    """
    if user.is_superuser or user_has_role(user, "administrador"):
        return True
    
    if user_has_role(user, "medico"):
        return True
    
    # Matrona puede editar fichas pero no todo
    if user_has_role(user, "matrona"):
        return True
    
    return False


def tiene_permiso_asignar_medicamentos(user):
    """
    Verifica si el usuario puede asignar medicamentos
    """
    if user.is_superuser or user_has_role(user, "administrador"):
        return True
    
    if user_has_role(user, "medico"):
        return True
    
    if user_has_role(user, "matrona"):
        return True
    
    return False


def tiene_permiso_iniciar_parto(user):
    """
    Verifica si el usuario puede iniciar un parto
    Solo médico puede hacerlo
    """
    if user.is_superuser or user_has_role(user, "administrador"):
        return True
    
    if user_has_role(user, "medico"):
        return True
    
    return False