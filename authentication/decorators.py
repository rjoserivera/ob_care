from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .utils import user_has_role


def role_required(role):
    """
    Decorador que requiere un rol específico
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse_lazy('authentication:login'))
            
            if not (user_has_role(request.user, role) or request.user.is_superuser):
                messages.error(request, f"Necesitas el rol '{role}' para acceder aquí.")
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def roles_required(*roles):
    """
    Decorador que permite múltiples roles
    Ejemplo: @roles_required('medico', 'administrador')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse_lazy('authentication:login'))
            
            has_role = any(user_has_role(request.user, role) for role in roles) or request.user.is_superuser
            
            if not has_role:
                messages.error(request, "No tienes permisos para acceder aquí.")
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_only(view_func):
    """
    Decorador que solo permite administradores
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('authentication:login'))
        
        if not (request.user.is_superuser or user_has_role(request.user, 'administrador')):
            messages.error(request, "Solo administradores pueden acceder aquí.")
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper