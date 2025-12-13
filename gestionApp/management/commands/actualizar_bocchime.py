"""
Comando para actualizar el usuario medico_1 a BocchiMe
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Actualiza el usuario medico_1 a BocchiMe'

    def handle(self, *args, **options):
        try:
            # Buscar el usuario medico_1
            user = User.objects.get(username='medico_1')
            
            # Guardar el Telegram Chat ID actual
            telegram_id = None
            if hasattr(user, 'perfil') and user.perfil.telegram_chat_id:
                telegram_id = user.perfil.telegram_chat_id
                self.stdout.write(f'📱 Telegram ID guardado: {telegram_id}')
            
            # Actualizar datos
            user.username = 'BocchiMe'
            user.first_name = 'Joseph'
            user.last_name = 'Rivera'
            user.email = 'BocchiMe@hospital.cl'
            user.set_password('Tomas216')
            user.save()
            
            # Restaurar Telegram si existía
            if telegram_id and hasattr(user, 'perfil'):
                user.perfil.telegram_chat_id = telegram_id
                user.perfil.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Telegram restaurado: {telegram_id}'))
            
            self.stdout.write(self.style.SUCCESS('\n✅ Usuario actualizado exitosamente!'))
            self.stdout.write(f'   Username: BocchiMe')
            self.stdout.write(f'   Nombre: Joseph Rivera')
            self.stdout.write(f'   Contraseña: Tomas216')
            if telegram_id:
                self.stdout.write(f'   Telegram: Configurado ({telegram_id})')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Usuario medico_1 no encontrado'))
            self.stdout.write('   Verifica que el usuario existe en la base de datos')
