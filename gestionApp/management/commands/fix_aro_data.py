from django.core.management.base import BaseCommand
from matronaApp.models import FichaObstetrica, CatalogoARO
import random

class Command(BaseCommand):
    help = 'Backfill Clasificación ARO for existing records'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando backfill de Clasificación ARO...")

        # 1. Asegurar categorías
        nombres_aro = ['Sin Riesgo', 'Alto Riesgo I', 'Alto Riesgo II', 'Alto Riesgo III']
        aros = []
        for nombre in nombres_aro:
            aro, created = CatalogoARO.objects.get_or_create(nombre=nombre, defaults={'activo': True})
            if created:
                self.stdout.write(f"Creado nuevo ARO: {nombre}")
            aros.append(aro)

        # 2. Actualizar Fichas
        fichas = FichaObstetrica.objects.filter(clasificacion_aro__isnull=True)
        count = fichas.count()
        self.stdout.write(f"Procesando {count} fichas sin ARO...")

        updated = 0
        for ficha in fichas:
            ficha.clasificacion_aro = random.choice(aros)
            ficha.save(update_fields=['clasificacion_aro'])
            updated += 1
        
        self.stdout.write(self.style.SUCCESS(f"Listo. {updated} fichas actualizadas."))
