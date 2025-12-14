"""
Comando para configurar Telegram Chat ID de un usuario
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Configura el Telegram Chat ID de un usuario'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username del usuario')
        parser.add_argument('chat_id', type=str, help='Chat ID de Telegram')

    def handle(self, *args, **options):
        username = options['username']
        chat_id = options['chat_id']
        
        try:
            user = User.objects.get(username=username)
            
            # Crear perfil si no existe
            if not hasattr(user, 'perfil'):
                from gestionApp.models import PerfilUsuario
                perfil = PerfilUsuario.objects.create(usuario=user)
                self.stdout.write(self.style.WARNING(f'Perfil creado para {username}'))
            
            user.perfil.telegram_chat_id = chat_id
            user.perfil.save()
            
            self.stdout.write(self.style.SUCCESS(
                f'✅ Telegram configurado para {user.get_full_name() or username}'
            ))
            self.stdout.write(f'   Chat ID: {chat_id}')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Usuario "{username}" no encontrado'))
            self.stdout.write('\nUsuarios disponibles:')
            for u in User.objects.all()[:10]:
                self.stdout.write(f'  - {u.username} ({u.get_full_name()})')
