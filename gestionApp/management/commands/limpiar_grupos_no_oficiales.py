"""
Script para limpiar grupos no estándar y mantener solo los 4 roles oficiales
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Limpia grupos no estándar y mantiene solo Administrador, Matrona, Medico, TENS'

    def handle(self, *args, **options):
        # Grupos oficiales permitidos
        GRUPOS_OFICIALES = ['Administrador', 'Matrona', 'Medico', 'TENS']
        
        # Mapeo de grupos no oficiales a oficiales
        MAPEO_GRUPOS = {
            'Administrador de Sistemas': 'Administrador',
            'Matrona Supervisora': 'Matrona',
            'Matrona Clínica': 'Matrona',
            'Matrona Clinica': 'Matrona',
            'Medico Obstetra': 'Medico',
            'TENS de Turno': 'TENS',
        }
        
        self.stdout.write('=' * 60)
        self.stdout.write('LIMPIEZA DE GRUPOS NO ESTÁNDAR')
        self.stdout.write('=' * 60 + '\n')
        
        # Listar todos los grupos actuales
        todos_grupos = Group.objects.all().order_by('name')
        self.stdout.write(f'Total de grupos encontrados: {todos_grupos.count()}\n')
        
        for grupo in todos_grupos:
            usuarios_count = grupo.user_set.count()
            self.stdout.write(f'  - {grupo.name} ({usuarios_count} usuarios)')
        
        # Asegurar que existan los grupos oficiales
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('CREANDO/VERIFICANDO GRUPOS OFICIALES')
        self.stdout.write('=' * 60 + '\n')
        
        grupos_oficiales_obj = {}
        for nombre_grupo in GRUPOS_OFICIALES:
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)
            grupos_oficiales_obj[nombre_grupo] = grupo
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Creado: {nombre_grupo}'))
            else:
                self.stdout.write(f'  ✓ Existe: {nombre_grupo}')
        
        # Migrar usuarios de grupos no oficiales
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('MIGRANDO USUARIOS')
        self.stdout.write('=' * 60 + '\n')
        
        grupos_a_eliminar = []
        
        for grupo in todos_grupos:
            if grupo.name not in GRUPOS_OFICIALES:
                # Determinar a qué grupo oficial migrar
                grupo_destino_nombre = MAPEO_GRUPOS.get(grupo.name)
                
                if grupo_destino_nombre:
                    grupo_destino = grupos_oficiales_obj[grupo_destino_nombre]
                    usuarios = grupo.user_set.all()
                    
                    if usuarios.exists():
                        self.stdout.write(f'\n  Migrando de "{grupo.name}" a "{grupo_destino_nombre}":')
                        for usuario in usuarios:
                            usuario.groups.add(grupo_destino)
                            usuario.groups.remove(grupo)
                            self.stdout.write(f'    - {usuario.username}')
                    
                    grupos_a_eliminar.append(grupo)
                else:
                    # Grupo no mapeado, preguntar qué hacer
                    self.stdout.write(self.style.WARNING(
                        f'\n  ⚠ Grupo no mapeado: "{grupo.name}" ({grupo.user_set.count()} usuarios)'
                    ))
                    grupos_a_eliminar.append(grupo)
        
        # Eliminar grupos no oficiales
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('ELIMINANDO GRUPOS NO OFICIALES')
        self.stdout.write('=' * 60 + '\n')
        
        for grupo in grupos_a_eliminar:
            self.stdout.write(f'  ✗ Eliminando: {grupo.name}')
            grupo.delete()
        
        # Resumen final
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('GRUPOS FINALES')
        self.stdout.write('=' * 60 + '\n')
        
        grupos_finales = Group.objects.all().order_by('name')
        for grupo in grupos_finales:
            usuarios_count = grupo.user_set.count()
            self.stdout.write(self.style.SUCCESS(
                f'  ✓ {grupo.name} ({usuarios_count} usuarios)'
            ))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'COMPLETADO - {len(grupos_a_eliminar)} grupos eliminados'))
        self.stdout.write('=' * 60)
