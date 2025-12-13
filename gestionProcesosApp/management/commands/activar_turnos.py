"""
Comando para activar turnos del personal creado
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestionProcesosApp.models import PersonalTurno
from gestionApp.models import PerfilUsuario
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Activa turnos para todo el personal'

    def handle(self, *args, **options):
        # Obtener todos los usuarios con perfil
        usuarios = User.objects.filter(perfil__isnull=False).select_related('perfil')
        
        turnos_creados = 0
        
        for user in usuarios:
            # Determinar rol basado en grupos
            if user.groups.filter(name='Medicos').exists():
                rol = 'MEDICO'
            elif user.groups.filter(name='Matronas').exists():
                rol = 'MATRONA'
            elif user.groups.filter(name='TENS').exists():
                rol = 'TENS'
            else:
                continue  # Saltar si no tiene rol
            
            # Crear o actualizar turno
            turno, created = PersonalTurno.objects.update_or_create(
                usuario=user,
                defaults={
                    'rol': rol,
                    'estado': 'DISPONIBLE',
                    'fecha_inicio_turno': timezone.now(),
                    'fecha_fin_turno': timezone.now() + timedelta(hours=12)
                }
            )
            
            if created:
                turnos_creados += 1
                self.stdout.write(f'  ✅ Turno creado: {user.get_full_name()} ({rol})')
            else:
                self.stdout.write(f'  🔄 Turno actualizado: {user.get_full_name()} ({rol})')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 {turnos_creados} turnos nuevos creados'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total de personal en turno: {PersonalTurno.objects.filter(estado="DISPONIBLE").count()}'))
