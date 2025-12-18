"""
Script para actualizar fichas antiguas con el nuevo sistema de cierre
Marca como 'parto_completado' las fichas que tienen proceso_parto_iniciado
pero no tienen el campo actualizado
"""

from django.core.management.base import BaseCommand
from matronaApp.models import FichaObstetrica
from django.utils import timezone


class Command(BaseCommand):
    help = 'Actualiza fichas antiguas con el sistema de cierre'

    def handle(self, *args, **options):
        # Buscar fichas con parto iniciado pero no marcadas como completadas
        fichas_antiguas = FichaObstetrica.objects.filter(
            proceso_parto_iniciado=True,
            parto_completado=False
        )
        
        count = fichas_antiguas.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No hay fichas para actualizar'))
            return
        
        self.stdout.write(f'Encontradas {count} fichas con parto iniciado pero no completado')
        
        # Preguntar confirmación
        confirm = input(f'¿Marcar estas {count} fichas como "parto completado"? (s/n): ')
        
        if confirm.lower() != 's':
            self.stdout.write(self.style.WARNING('Operación cancelada'))
            return
        
        # Actualizar fichas
        updated = 0
        for ficha in fichas_antiguas:
            ficha.parto_completado = True
            ficha.save(update_fields=['parto_completado'])
            updated += 1
            self.stdout.write(f'  ✓ {ficha.numero_ficha} - {ficha.paciente}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ {updated} fichas actualizadas correctamente'))
        self.stdout.write(self.style.WARNING('Ahora puedes cerrar estas fichas manualmente desde el detalle'))
