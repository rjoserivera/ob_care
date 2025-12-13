"""
Comando para verificar personal disponible
"""
from django.core.management.base import BaseCommand
from gestionProcesosApp.models import PersonalTurno
from django.utils import timezone

class Command(BaseCommand):
    help = 'Verifica personal disponible'

    def handle(self, *args, **options):
        now = timezone.now()
        
        self.stdout.write('\n📊 PERSONAL DISPONIBLE:\n')
        
        for rol in ['MEDICO', 'MATRONA', 'TENS']:
            personal = PersonalTurno.objects.filter(
                rol=rol,
                estado='DISPONIBLE',
                fecha_fin_turno__gte=now
            )
            
            self.stdout.write(f'\n{rol}:')
            self.stdout.write(f'  Total: {personal.count()}')
            
            for pt in personal[:5]:  # Mostrar solo los primeros 5
                self.stdout.write(f'  - {pt.usuario.get_full_name()} (ID: {pt.id})')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Verificación completada'))
