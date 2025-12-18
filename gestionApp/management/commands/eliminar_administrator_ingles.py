"""
Script para eliminar grupo Administrator (inglés) y mantener Administrador (español)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Elimina grupo Administrator (inglés) y mantiene solo Administrador (español)'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('LISTANDO TODOS LOS GRUPOS')
        self.stdout.write('=' * 60 + '\n')
        
        # Listar TODOS los grupos
        grupos = Group.objects.all().order_by('name')
        for grupo in grupos:
            usuarios_count = grupo.user_set.count()
            self.stdout.write(f'  ID: {grupo.id:3d} | "{grupo.name}" | {usuarios_count} usuarios')
        
        # Buscar grupo "Administrator" (inglés)
        try:
            grupo_ingles = Group.objects.get(name='Administrator')
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write('ENCONTRADO GRUPO EN INGLÉS')
            self.stdout.write('=' * 60 + '\n')
            self.stdout.write(f'  ID: {grupo_ingles.id} | "{grupo_ingles.name}" | {grupo_ingles.user_set.count()} usuarios')
            
            # Buscar o crear grupo "Administrador" (español)
            grupo_espanol, created = Group.objects.get_or_create(name='Administrador')
            if created:
                self.stdout.write(f'\n  ✓ Creado grupo "Administrador" (ID: {grupo_espanol.id})')
            else:
                self.stdout.write(f'\n  ✓ Grupo "Administrador" ya existe (ID: {grupo_espanol.id})')
            
            # Transferir usuarios del inglés al español
            usuarios = grupo_ingles.user_set.all()
            if usuarios.exists():
                self.stdout.write(f'\n  Transfiriendo {usuarios.count()} usuarios de "Administrator" a "Administrador"')
                for usuario in usuarios:
                    usuario.groups.add(grupo_espanol)
                    usuario.groups.remove(grupo_ingles)
            
            # Eliminar grupo en inglés
            self.stdout.write(f'\n  ✗ Eliminando grupo "Administrator" (ID: {grupo_ingles.id})')
            grupo_ingles.delete()
            
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write(self.style.SUCCESS('GRUPO EN INGLÉS ELIMINADO'))
            self.stdout.write('=' * 60)
            
        except Group.DoesNotExist:
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write(self.style.WARNING('NO SE ENCONTRÓ GRUPO "Administrator" (inglés)'))
            self.stdout.write('=' * 60)
        
        # Listar grupos finales
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('GRUPOS FINALES')
        self.stdout.write('=' * 60 + '\n')
        
        grupos_finales = Group.objects.all().order_by('name')
        for grupo in grupos_finales:
            usuarios_count = grupo.user_set.count()
            self.stdout.write(self.style.SUCCESS(
                f'  ✓ ID: {grupo.id:3d} | "{grupo.name}" | {usuarios_count} usuarios'
            ))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('COMPLETADO'))
        self.stdout.write('=' * 60)
