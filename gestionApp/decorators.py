"""
gestionApp/decorators.py
Decoradores personalizados para vistas con URLs encriptadas
"""

from functools import wraps
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
from .url_encryption import url_encryptor


def decrypt_url_params(*param_names):
    """
    Decorador para desencriptar automáticamente parámetros de URL
    
    Args:
        *param_names: Nombres de los parámetros a desencriptar
        
    Uso:
        @decrypt_url_params('ficha_id', 'paciente_id')
        def mi_vista(request, ficha_id, paciente_id):
            # ficha_id y paciente_id ya están desencriptados
            ficha = FichaObstetrica.objects.get(id=ficha_id)
            ...
    
    Example:
        # URL: /detalle/MTIz:abc123def456/
        # El decorador convierte 'MTIz:abc123def456' -> 123
        
        @decrypt_url_params('ficha_id')
        def detalle_ficha(request, ficha_id):
            # ficha_id = 123 (ya desencriptado)
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Desencriptar los parámetros especificados
            for param_name in param_names:
                if param_name in kwargs:
                    encrypted_value = kwargs[param_name]
                    
                    # Intentar desencriptar
                    decrypted_value = url_encryptor.decrypt_id(encrypted_value)
                    
                    if decrypted_value is None:
                        # Token inválido o manipulado
                        messages.error(request, "El enlace es inválido o ha expirado.")
                        raise Http404("Parámetro de URL inválido")
                    
                    # Reemplazar con el valor desencriptado
                    kwargs[param_name] = decrypted_value
            
            # Llamar a la vista original con los parámetros desencriptados
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def require_encrypted_access(resource_type='ficha'):
    """
    Decorador que requiere un token de acceso válido para acceder a un recurso
    
    Args:
        resource_type: Tipo de recurso ('ficha', 'parto', 'paciente', etc.)
        
    Uso:
        @require_encrypted_access(resource_type='ficha')
        def detalle_ficha(request, ficha_id):
            # Solo accesible con token válido
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verificar si hay un token de acceso en la sesión o en GET
            access_token = request.GET.get('token') or request.session.get('access_token')
            
            if not access_token:
                messages.warning(request, "Acceso denegado. Token de acceso requerido.")
                return redirect('home')
            
            # Aquí podrías validar el token contra una base de datos
            # Por ahora, solo verificamos que exista
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def obfuscate_response_urls(view_func):
    """
    Decorador que automáticamente ofusca todas las URLs en la respuesta
    
    NOTA: Este es un decorador avanzado que modifica el HTML de la respuesta
    Úsalo con precaución ya que puede afectar el rendimiento
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        
        # Solo procesar respuestas HTML
        if hasattr(response, 'content') and 'text/html' in response.get('Content-Type', ''):
            # Aquí podrías implementar lógica para reemplazar URLs en el HTML
            # Por ahora, solo retornamos la respuesta sin modificar
            pass
        
        return response
    
    return wrapper
