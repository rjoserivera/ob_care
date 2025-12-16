from django.contrib.auth.models import User

def get_client_ip(request):
    """Obtiene la IP del cliente del request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_role(user):
    """Obtiene el rol principal del usuario"""
    if not user or not user.is_authenticated:
        return "Anónimo"
    
    try:
        if hasattr(user, 'perfil'):
            return user.perfil.rol_principal
        elif user.is_superuser:
            return "Superusuario"
        elif user.groups.exists():
            return user.groups.first().name
    except:
        pass
        
    return "Usuario"
