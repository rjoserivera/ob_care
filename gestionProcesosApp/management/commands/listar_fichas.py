"""
Comando para listar fichas de parto
"""
from django.core.management.base import BaseCommand
from ingresoPartoApp.models import FichaParto
from gestionProcesosApp.models import AsignacionPersonal

class Command(BaseCommand):
    help = 'Lista todas las fichas de parto'

    def handle(self, *args, **options):
        fichas = FichaParto.objects.all()
        
        self.stdout.write('\n📋 FICHAS DE PARTO:\n')
        
        for ficha in fichas:
            asignaciones = AsignacionPersonal.objects.filter(proceso=ficha).count()
            self.stdout.write(
                f'ID: {ficha.id} | Número: {ficha.numero_ficha_parto} | '
                f'Paciente: {ficha.ficha_obstetrica.paciente.persona.nombre_completo} | '
                f'Invitaciones: {asignaciones}'
            )
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Total: {fichas.count()} fichas'))
