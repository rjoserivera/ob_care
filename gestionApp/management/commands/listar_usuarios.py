"""
Comando para listar usuarios
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Lista todos los usuarios del sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('   USUARIOS DEL SISTEMA'))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))

        usuarios = User.objects.all().order_by('username')

        if not usuarios.exists():
            self.stdout.write(self.style.WARNING('⚠️ No hay usuarios en el sistema.\n'))
            return

        self.stdout.write('┌─────────────────────┬───────────────────────────┬──────────────────────────┬────────────┐')
        self.stdout.write('│ Username            │ Nombre Completo           │ Roles                    │ Estado     │')
        self.stdout.write('├─────────────────────┼───────────────────────────┼──────────────────────────┼────────────┤')

        for user in usuarios:
            username = user.username[:19].ljust(19)
            full_name = f"{user.first_name} {user.last_name}"[:25].ljust(25)
            roles = ", ".join(user.groups.values_list('name', flat=True))[:24].ljust(24)
            estado = "✅ Activo" if user.is_active else "❌ Inactivo"
            
            self.stdout.write(f'│ {username} │ {full_name} │ {roles} │ {estado}  │')

        self.stdout.write('└─────────────────────┴───────────────────────────┴──────────────────────────┴────────────┘')
        self.stdout.write(f'\n📊 Total: {usuarios.count()} usuario(s)\n')
