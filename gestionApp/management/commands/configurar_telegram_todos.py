"""
Comando para configurar Telegram para todos los usuarios
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestionApp.models import PerfilUsuario

class Command(BaseCommand):
    help = 'Configura Telegram para todos los usuarios'

    def add_arguments(self, parser):
        parser.add_argument('chat_id', type=str, help='Telegram Chat ID a configurar')

    def handle(self, *args, **options):
        chat_id = options['chat_id']
        
        usuarios_actualizados = 0
        usuarios_sin_perfil = 0
        
        for user in User.objects.all():
            if hasattr(user, 'perfil'):
                user.perfil.telegram_chat_id = chat_id
                user.perfil.save()
                usuarios_actualizados += 1
                self.stdout.write(f'  ✅ {user.get_full_name() or user.username}')
            else:
                # Crear perfil si no existe
                perfil = PerfilUsuario.objects.create(
                    usuario=user,
                    telegram_chat_id=chat_id
                )
                usuarios_sin_perfil += 1
                self.stdout.write(f'  🆕 {user.get_full_name() or user.username} (perfil creado)')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ {usuarios_actualizados} usuarios actualizados'))
        if usuarios_sin_perfil > 0:
            self.stdout.write(self.style.SUCCESS(f'🆕 {usuarios_sin_perfil} perfiles creados'))
        self.stdout.write(self.style.SUCCESS(f'\n📱 Todos configurados con Chat ID: {chat_id}'))
