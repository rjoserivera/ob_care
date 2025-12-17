from django.utils import timezone
from .models import LogSistema
from .utils import get_client_ip, get_user_role


class NoCacheMiddleware:
    """
    Middleware para prevenir el cacheo de páginas en el navegador.
    Esto evita que usuarios accedan a páginas sensibles al usar el botón de retroceder.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Solo aplicar a páginas HTML autenticadas (no a archivos estáticos)
        if request.user.is_authenticated and response.get('Content-Type', '').startswith('text/html'):
            # Headers para prevenir cacheo
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response


class SystemAuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            # Registrar métodos que modifican estado (POST, PUT, DELETE, PATCH)
            if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                self.log_action(request, response)
        
        return response

    def log_action(self, request, response):
        try:
            ip = get_client_ip(request)
            rol = get_user_role(request.user)
            
            # Determinar módulo
            modulo = "Sistema"
            if request.resolver_match:
                if request.resolver_match.app_name:
                    modulo = request.resolver_match.app_name
                elif request.resolver_match.view_name:
                    modulo = request.resolver_match.view_name.split('.')[0]

            # Capturar datos del POST (lo que cambió)
            detalle = ""
            if request.method in ['POST', 'PUT', 'PATCH']:
                datos = request.POST.copy()
                
                # Eliminar datos sensibles y técnicos
                sensitive_keys = ['csrfmiddlewaretoken', 'password', 'password_confirm', 'token']
                for key in sensitive_keys:
                    if key in datos:
                        del datos[key]
                
                # Formatear datos legibles
                cambios = []
                for key, value in datos.items():
                    if value: # Solo mostrar campos con valor
                        cambios.append(f"{key}: {value}")
                
                if cambios:
                    detalle = " | ".join(cambios)
                else:
                    detalle = "Sin datos registrados o solo archivos."
            else:
                detalle = f"Status Code: {response.status_code}"

            LogSistema.objects.create(
                usuario=request.user,
                accion=f"{request.method} {request.path}",
                detalle=detalle[:500], # Truncar si es muy largo
                modulo=modulo,
                rol_usuario=rol,
                ip_address=ip
            )
        except Exception as e:
            print(f"Error logging action: {e}")
            pass
