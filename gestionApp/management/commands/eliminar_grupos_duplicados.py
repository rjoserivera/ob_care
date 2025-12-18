"""
Script para eliminar grupos duplicados de Django
Mantiene solo: Administrador, Matrona, Medico, TENS
Elimina: Administradores, Matronas, Medicos
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Elimina grupos duplicados y mantiene solo los singulares'

    def handle(self, *args, **options):
        # Grupos a eliminar (plurales)
        grupos_eliminar = ['Administradores', 'Matronas', 'Medicos']
        
        # Grupos a mantener (singulares)
        grupos_mantener = ['Administrador', 'Matrona', 'Medico', 'TENS']
        
        self.stdout.write('=' * 50)
        self.stdout.write('ELIMINANDO GRUPOS DUPLICADOS')
        self.stdout.write('=' * 50)
        
        # Eliminar grupos duplicados
        for grupo_nombre in grupos_eliminar:
            try:
                grupo = Group.objects.get(name=grupo_nombre)
                
                # Mover usuarios al grupo singular si tienen el plural
                if grupo_nombre == 'Administradores':
                    grupo_correcto = Group.objects.get_or_create(name='Administrador')[0]
                elif grupo_nombre == 'Matronas':
                    grupo_correcto = Group.objects.get_or_create(name='Matrona')[0]
                elif grupo_nombre == 'Medicos':
                    grupo_correcto = Group.objects.get_or_create(name='Medico')[0]
                
                # Transferir usuarios
                usuarios = grupo.user_set.all()
                if usuarios.exists():
                    self.stdout.write(f'  Transfiriendo {usuarios.count()} usuarios de "{grupo_nombre}" a "{grupo_correcto.name}"')
                    for usuario in usuarios:
                        usuario.groups.add(grupo_correcto)
                        usuario.groups.remove(grupo)
                
                # Eliminar grupo duplicado
                grupo.delete()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Eliminado: {grupo_nombre}'))
                
            except Group.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  - No existe: {grupo_nombre}'))
        
        # Verificar que existan los grupos correctos
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('VERIFICANDO GRUPOS CORRECTOS')
        self.stdout.write('=' * 50)
        
        for grupo_nombre in grupos_mantener:
            grupo, created = Group.objects.get_or_create(name=grupo_nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Creado: {grupo_nombre}'))
            else:
                usuarios_count = grupo.user_set.count()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Existe: {grupo_nombre} ({usuarios_count} usuarios)'))
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('PROCESO COMPLETADO'))
        self.stdout.write('=' * 50)
