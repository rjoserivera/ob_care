from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from gestionApp.models import PerfilUsuario

from gestionProcesosApp.telegram_utils import enviar_telegram

# Decorador para asegurar que solo administrativos accedan
def admin_required(user):
    return user.is_superuser or user.groups.filter(name='Administradores').exists()

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
