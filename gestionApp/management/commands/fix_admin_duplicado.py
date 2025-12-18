"""
Script para eliminar grupo Administrador vacío
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Elimina grupos Administrador vacíos, mantiene solo uno con usuarios'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('GRUPOS ADMINISTRADOR EN LA BASE DE DATOS')
        self.stdout.write('=' * 60 + '\n')
        
        # Buscar todos los grupos llamados "Administrador"
        grupos_admin = Group.objects.filter(name='Administrador').order_by('id')
        
        if not grupos_admin.exists():
            self.stdout.write(self.style.WARNING('  No se encontraron grupos "Administrador"'))
            return
        
        self.stdout.write(f'Total de grupos "Administrador": {grupos_admin.count()}\n')
        
        # Listar todos
        for grupo in grupos_admin:
            usuarios_count = grupo.user_set.count()
            self.stdout.write(f'  ID: {grupo.id:3d} | Usuarios: {usuarios_count}')
        
        if grupos_admin.count() == 1:
            self.stdout.write(self.style.SUCCESS('\n  ✓ Solo hay un grupo Administrador, no hay duplicados'))
            return
        
        # Encontrar el grupo con usuarios
        grupo_con_usuarios = None
        grupos_vacios = []
        
        for grupo in grupos_admin:
            if grupo.user_set.exists():
                if grupo_con_usuarios is None:
                    grupo_con_usuarios = grupo
                else:
                    # Si hay múltiples con usuarios, transferir al primero
                    self.stdout.write(f'\n  Transfiriendo usuarios de ID {grupo.id} a ID {grupo_con_usuarios.id}')
                    for usuario in grupo.user_set.all():
                        usuario.groups.add(grupo_con_usuarios)
                        usuario.groups.remove(grupo)
                    grupos_vacios.append(grupo)
            else:
                grupos_vacios.append(grupo)
        
        # Si no hay ninguno con usuarios, mantener el de menor ID
        if grupo_con_usuarios is None:
            grupo_con_usuarios = grupos_admin.first()
            grupos_vacios = list(grupos_admin.exclude(id=grupo_con_usuarios.id))
            self.stdout.write(f'\n  Manteniendo grupo ID {grupo_con_usuarios.id} (ninguno tenía usuarios)')
        
        # Eliminar grupos vacíos/duplicados
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('ELIMINANDO DUPLICADOS')
        self.stdout.write('=' * 60 + '\n')
        
        for grupo in grupos_vacios:
            self.stdout.write(self.style.WARNING(f'  ✗ Eliminando: ID {grupo.id}'))
            grupo.delete()
        
        # Verificar resultado
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('RESULTADO FINAL')
        self.stdout.write('=' * 60 + '\n')
        
        grupos_finales = Group.objects.filter(name='Administrador')
        for grupo in grupos_finales:
            usuarios_count = grupo.user_set.count()
            self.stdout.write(self.style.SUCCESS(
                f'  ✓ ID: {grupo.id} | "{grupo.name}" | {usuarios_count} usuarios'
            ))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'COMPLETADO - {len(grupos_vacios)} grupos eliminados'))
        self.stdout.write('=' * 60)
