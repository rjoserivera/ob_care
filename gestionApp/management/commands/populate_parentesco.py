from django.core.management.base import BaseCommand
from gestionApp.models import CatalogoParentesco

class Command(BaseCommand):
    help = 'Populate CatalogoParentesco'

    def handle(self, *args, **options):
        self.stdout.write("Populating CatalogoParentesco...")
        
        data = [
            ('PAREJA', 'Pareja/Esposo(a)', 1),
            ('MADRE', 'Madre', 2),
            ('PADRE', 'Padre', 3),
            ('HERMANO', 'Hermano(a)', 4),
            ('HIJO', 'Hijo(a)', 5),
            ('FAMILIAR', 'Otro Familiar', 6),
            ('AMIGO', 'Amigo(a)', 7),
            ('OTRO', 'Otro', 8),
        ]
        
        for codigo, nombre, orden in data:
            obj, created = CatalogoParentesco.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'orden': orden, 'activo': True}
            )
            if created:
                self.stdout.write(f"Created: {nombre}")
            else:
                self.stdout.write(f"Exists: {nombre}")
