from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomLoginForm
from .utils import get_dashboard_url_for_user, user_has_role
import logging

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user

        dashboard_url = get_dashboard_url_for_user(user)
        if dashboard_url:
            logger.info(f"Login redirige → {dashboard_url}")
            return dashboard_url

        messages.warning(self.request, "No tienes un rol asignado.")
        return reverse_lazy("home")

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me", False)
        self.request.session.set_expiry(2592000 if remember_me else 0)

        user = form.get_user()
        login(self.request, user)

        logger.info(f'✅ Login exitoso - Usuario: {user.username} - IP: {self.get_client_ip()}')

        rol = self.get_user_role_display(user)
        messages.success(self.request, f"Bienvenido {user.username} ({rol})")

        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        username = form.cleaned_data.get('username', 'desconocido')
        logger.warning(f'❌ Login fallido - Usuario: {username} - IP: {self.get_client_ip()}')
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)

    def get_client_ip(self):
        x = self.request.META.get("HTTP_X_FORWARDED_FOR")
        return x.split(",")[0] if x else self.request.META.get("REMOTE_ADDR")

    def get_user_role_display(self, user):
        if user_has_role(user, "administrador"):
            return "Administrador"
        if user_has_role(user, "medico"):
            return "Médico"
        if user_has_role(user, "matrona"):
            return "Matrona"
        if user_has_role(user, "tens"):
            return "TENS"
        return "Usuario"

def custom_logout_view(request):
    if request.user.is_authenticated:
        logger.info(f"Logout: {request.user.username}")
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("home")


# -----------------------------
# DASHBOARDS POR ROL
# -----------------------------

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
