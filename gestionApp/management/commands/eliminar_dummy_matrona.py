"""
Script para eliminar usuario dummy_matrona_d46bda12
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Elimina el usuario dummy_matrona_d46bda12'

    def handle(self, *args, **options):
        username = 'dummy_matrona_d46bda12'
        
        self.stdout.write('=' * 60)
        self.stdout.write(f'ELIMINANDO USUARIO: {username}')
        self.stdout.write('=' * 60 + '\n')
        
        try:
            user = User.objects.get(username=username)
            
            # Mostrar información del usuario
            self.stdout.write(f'  Usuario encontrado:')
            self.stdout.write(f'    - ID: {user.id}')
            self.stdout.write(f'    - Username: {user.username}')
            self.stdout.write(f'    - Nombre: {user.get_full_name()}')
            self.stdout.write(f'    - Email: {user.email}')
            self.stdout.write(f'    - Grupos: {", ".join([g.name for g in user.groups.all()])}')
            
            # Eliminar usuario
            user.delete()
            
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write(self.style.SUCCESS(f'✓ USUARIO ELIMINADO EXITOSAMENTE'))
            self.stdout.write('=' * 60)
            
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'⚠ Usuario "{username}" no encontrado'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error al eliminar usuario: {e}'))
