"""
Script directo para eliminar grupos duplicados por ID
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db.models import Count


class Command(BaseCommand):
    help = 'Elimina grupos duplicados manteniendo el de menor ID'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('LISTANDO TODOS LOS GRUPOS')
        self.stdout.write('=' * 60 + '\n')
        
        # Listar TODOS los grupos con sus IDs
        grupos = Group.objects.all().order_by('id')
        for grupo in grupos:
            self.stdout.write(f'  ID: {grupo.id:3d} | Nombre: "{grupo.name}" | Usuarios: {grupo.user_set.count()}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('ELIMINANDO DUPLICADOS (manteniendo menor ID)')
        self.stdout.write('=' * 60 + '\n')
        
        # Grupos correctos que queremos mantener
        grupos_correctos = {
            'Administrador': None,
            'Matrona': None,
            'Medico': None,
            'TENS': None
        }
        
        # Encontrar el grupo con menor ID para cada nombre
        for nombre in grupos_correctos.keys():
            grupo_principal = Group.objects.filter(name=nombre).order_by('id').first()
            if grupo_principal:
                grupos_correctos[nombre] = grupo_principal
                self.stdout.write(f'  ✓ Manteniendo: "{nombre}" (ID: {grupo_principal.id})')
        
        # Eliminar duplicados
        eliminados = 0
        for nombre, grupo_principal in grupos_correctos.items():
            if grupo_principal:
                # Buscar duplicados (mismo nombre, diferente ID)
                duplicados = Group.objects.filter(name=nombre).exclude(id=grupo_principal.id)
                
                for dup in duplicados:
                    # Transferir usuarios
                    usuarios = dup.user_set.all()
                    if usuarios.exists():
                        self.stdout.write(f'    Transfiriendo {usuarios.count()} usuarios de ID {dup.id} a ID {grupo_principal.id}')
                        for usuario in usuarios:
                            usuario.groups.add(grupo_principal)
                            usuario.groups.remove(dup)
                    
                    self.stdout.write(self.style.WARNING(f'    ✗ Eliminando duplicado: "{dup.name}" (ID: {dup.id})'))
                    dup.delete()
                    eliminados += 1
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('GRUPOS FINALES')
        self.stdout.write('=' * 60 + '\n')
        
        grupos_finales = Group.objects.all().order_by('id')
        for grupo in grupos_finales:
            self.stdout.write(self.style.SUCCESS(
                f'  ID: {grupo.id:3d} | "{grupo.name}" | {grupo.user_set.count()} usuarios'
            ))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'COMPLETADO - {eliminados} grupos eliminados'))
        self.stdout.write('=' * 60)
