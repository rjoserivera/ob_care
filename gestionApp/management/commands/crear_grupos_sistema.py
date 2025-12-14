from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Crea los 5 grupos: Médico, Matrona, TENS, Paciente, Administrador'

    def handle(self, *args, **kwargs):
        grupos = ['Médico', 'Matrona', 'TENS', 'Paciente', 'Administrador']
        
        for nombre in grupos:
            grupo, created = Group.objects.get_or_create(name=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Grupo "{nombre}" creado'))
            else:
                self.stdout.write(self.style.WARNING(f'○ Grupo "{nombre}" ya existe'))
        
        self.stdout.write(self.style.SUCCESS('\\n✓ TODOS LOS GRUPOS CREADOS\\n'))