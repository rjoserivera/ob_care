"""
Script para verificar y limpiar grupos duplicados
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Verifica y limpia grupos duplicados'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('VERIFICANDO GRUPOS EN LA BASE DE DATOS')
        self.stdout.write('=' * 60)
        
        # Listar todos los grupos
        grupos = Group.objects.all().order_by('name')
        
        self.stdout.write(f'\nTotal de grupos: {grupos.count()}\n')
        
        for grupo in grupos:
            usuarios_count = grupo.user_set.count()
            self.stdout.write(f'  - {grupo.name} ({usuarios_count} usuarios)')
        
        # Buscar duplicados por nombre (case-insensitive)
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('BUSCANDO DUPLICADOS')
        self.stdout.write('=' * 60 + '\n')
        
        nombres_vistos = {}
        duplicados = []
        
        for grupo in grupos:
            nombre_lower = grupo.name.lower()
            if nombre_lower in nombres_vistos:
                duplicados.append((grupo, nombres_vistos[nombre_lower]))
                self.stdout.write(self.style.WARNING(
                    f'  ⚠ DUPLICADO: "{grupo.name}" (ID: {grupo.id}) vs "{nombres_vistos[nombre_lower].name}" (ID: {nombres_vistos[nombre_lower].id})'
                ))
            else:
                nombres_vistos[nombre_lower] = grupo
        
        if not duplicados:
            self.stdout.write(self.style.SUCCESS('\n  ✓ No se encontraron duplicados'))
        else:
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write('ELIMINANDO DUPLICADOS')
            self.stdout.write('=' * 60 + '\n')
            
            for grupo_dup, grupo_original in duplicados:
                # Transferir usuarios
                usuarios = grupo_dup.user_set.all()
                if usuarios.exists():
                    self.stdout.write(f'  Transfiriendo {usuarios.count()} usuarios de "{grupo_dup.name}" a "{grupo_original.name}"')
                    for usuario in usuarios:
                        usuario.groups.add(grupo_original)
                
                # Eliminar duplicado
                self.stdout.write(self.style.SUCCESS(f'  ✓ Eliminando: "{grupo_dup.name}" (ID: {grupo_dup.id})'))
                grupo_dup.delete()
        
        # Verificar grupos finales
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('GRUPOS FINALES')
        self.stdout.write('=' * 60 + '\n')
        
        grupos_finales = Group.objects.all().order_by('name')
        for grupo in grupos_finales:
            usuarios_count = grupo.user_set.count()
            self.stdout.write(self.style.SUCCESS(f'  ✓ {grupo.name} ({usuarios_count} usuarios)'))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('PROCESO COMPLETADO'))
        self.stdout.write('=' * 60)
