from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import LogSistema
from .utils import get_client_ip, get_user_role

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    try:
        ip = get_client_ip(request)
        rol = get_user_role(user)
        
        LogSistema.objects.create(
            usuario=user,
            accion="INICIO DE SESIÓN",
            detalle="Usuario ingresó al sistema",
            modulo="Autenticación",
            rol_usuario=rol,
            ip_address=ip
        )
    except Exception as e:
        print(f"Error logging login: {e}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    try:
        if user:
            ip = get_client_ip(request)
            rol = get_user_role(user)
            
            LogSistema.objects.create(
                usuario=user,
                accion="CIERRE DE SESIÓN",
                detalle="Usuario salió del sistema",
                modulo="Autenticación",
                rol_usuario=rol,
                ip_address=ip
            )
    except Exception as e:
        print(f"Error logging logout: {e}")
