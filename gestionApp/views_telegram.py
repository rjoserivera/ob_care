from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from gestionApp.models import PerfilUsuario

from gestionProcesosApp.telegram_utils import enviar_telegram

import subprocess
import sys
import os

# Decorador para asegurar que solo administrativos accedan
def admin_required(user):
    return user.is_superuser or user.groups.filter(name='Administrador').exists()

@method_decorator(login_required, name='dispatch')
class ConfigurarTelegramView(View):
    template_name = "Gestion/Data/configurar_telegram.html"

    def dispatch(self, request, *args, **kwargs):
        if not admin_required(request.user):
            messages.error(request, "Acceso denegado. Se requieren permisos de administrador.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        users = User.objects.select_related('perfil').order_by('username')
        return render(request, self.template_name, {'users': users})

    def post(self, request):
        user_id = request.POST.get('user_id')
        chat_id = request.POST.get('chat_id', '').strip()
        action = request.POST.get('action', 'save')
        
        try:
            user = User.objects.get(id=user_id)
            
            # Crear perfil si no existe
            perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
            
            if action == 'test':
                if chat_id:
                    # Enviar mensaje de prueba
                    mensaje = (
                        "🔔 *Prueba de Notificación*\n\n"
                        f"Hola {user.first_name}, esta es una prueba de conexión exitosa con el Sistema Obstétrico."
                    )
                    exito = enviar_telegram(chat_id, mensaje)
                    if exito:
                        messages.success(request, f"Mensaje de prueba enviado a {user.username}")
                    else:
                        messages.warning(request, f"No se pudo enviar el mensaje a {user.username}. Verifica el Chat ID.")
                else:
                    messages.warning(request, "Debes guardar un Chat ID antes de probar.")
            else:
                # Guardar configuración (Default)
                perfil.telegram_chat_id = chat_id
                perfil.save()
                messages.success(request, f"Telegram configurado correctamente para {user.username}")
            
        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
        except Exception as e:
            messages.error(request, f"Error: {e}")
            
        return redirect('gestion:configurar_telegram')


@method_decorator(login_required, name='dispatch')
class IniciarBotView(View):
    def dispatch(self, request, *args, **kwargs):
        if not admin_required(request.user):
            messages.error(request, "Acceso denegado.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            # Path to manage.py
            manage_py = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'manage.py')
            
            # Command to run
            # Use sys.executable to ensure we use the same python interpreter (venv)
            cmd = [sys.executable, manage_py, 'telegram_bot']
            
            # Spawn process (Windows specific flags for new console to stay alive)
            CREATE_NEW_CONSOLE = 0x00000010
            
            # Use Popen to run detached
            subprocess.Popen(cmd, creationflags=CREATE_NEW_CONSOLE, close_fds=True)
            
            messages.success(request, "✅ Servicio de Bot iniciado exitosamente en una nueva ventana.")
        except Exception as e:
            messages.error(request, f"❌ Error iniciando el bot: {str(e)}")
            
        return redirect('gestion:configurar_telegram')


@method_decorator(login_required, name='dispatch')
class AsignarRolesView(View):
    template_name = "Gestion/Data/asignar_roles.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not admin_required(request.user):
            messages.error(request, "Acceso denegado. Se requieren permisos de administrador.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        from django.contrib.auth.models import Group
        
        # Obtener parámetro de búsqueda
        search_query = request.GET.get('search', '').strip()
        
        # Obtener todos los grupos disponibles
        grupos = Group.objects.all().order_by('name')
        
        # Buscar usuarios
        users = None
        if search_query:
            users = User.objects.filter(
                username__icontains=search_query
            ) | User.objects.filter(
                first_name__icontains=search_query
            ) | User.objects.filter(
                last_name__icontains=search_query
            )
            users = users.select_related('perfil').distinct().order_by('username')
        
        context = {
            'users': users,
            'grupos': grupos,
            'search_query': search_query
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        from django.contrib.auth.models import Group
        
        user_id = request.POST.get('user_id')
        grupo_id = request.POST.get('grupo_id')
        
        try:
            user = User.objects.get(id=user_id)
            grupo = Group.objects.get(id=grupo_id)
            
            # Asignar grupo al usuario
            user.groups.add(grupo)
            
            messages.success(request, f"✅ Rol '{grupo.name}' asignado a {user.username}")
            
        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
        except Group.DoesNotExist:
            messages.error(request, "Grupo no encontrado.")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        
        # Redirigir con el parámetro de búsqueda si existe
        search_query = request.POST.get('search_query', '')
        if search_query:
            return redirect(f"{request.path}?search={search_query}")
        return redirect('gestion:asignar_roles')

