"""
Script de prueba para verificar que la vista de exportación funciona
"""

from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Prueba la vista de exportación'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('PROBANDO VISTA DE EXPORTACIÓN')
        self.stdout.write('=' * 60 + '\n')
        
        # Crear cliente de prueba
        client = Client()
        
        # Obtener un usuario admin
        try:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                self.stdout.write(self.style.ERROR('No se encontró un usuario administrador'))
                return
            
            # Login
            client.force_login(user)
            
            # Hacer request a la vista
            self.stdout.write(f'Haciendo request a /partos/exportar-libro/')
            response = client.get('/partos/exportar-libro/')
            
            self.stdout.write(f'\nStatus Code: {response.status_code}')
            
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✓ Vista responde correctamente'))
                self.stdout.write(f'Content-Type: {response.get("Content-Type", "N/A")}')
                self.stdout.write(f'Template usado: {response.templates[0].name if response.templates else "N/A"}')
            else:
                self.stdout.write(self.style.ERROR(f'✗ Error: Status {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            import traceback
            traceback.print_exc()
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('PRUEBA COMPLETADA')
        self.stdout.write('=' * 60)
