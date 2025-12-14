"""
Comando para limpiar invitaciones de una ficha de parto
"""
from django.core.management.base import BaseCommand
from gestionProcesosApp.models import AsignacionPersonal
from ingresoPartoApp.models import FichaParto

class Command(BaseCommand):
    help = 'Limpia las invitaciones de una ficha de parto'

    def add_arguments(self, parser):
        parser.add_argument('ficha_obstetrica_id', type=int, help='ID de la ficha obstétrica')

    def handle(self, *args, **options):
        ficha_obs_id = options['ficha_obstetrica_id']
        
        try:
            # Buscar FichaParto por FichaObstetrica
            ficha = FichaParto.objects.get(ficha_obstetrica_id=ficha_obs_id)
            
            # Eliminar asignaciones
            asignaciones = AsignacionPersonal.objects.filter(proceso=ficha)
            count = asignaciones.count()
            asignaciones.delete()
            
            self.stdout.write(self.style.SUCCESS(
                f'✅ Se eliminaron {count} invitaciones de la ficha {ficha.numero_ficha_parto}'
            ))
            
        except FichaParto.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'❌ No existe ficha de parto para la ficha obstétrica ID {ficha_obs_id}'
            ))
