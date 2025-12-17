
import os
import sys
import django
from django.utils import timezone

# Configure environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from django.contrib.auth.models import User
from gestionProcesosApp.models import PersonalTurno
from gestionApp.models import PerfilUsuario

def start_all_shifts():
    print("🚀 INICIANDO TURNOS PARA TODO EL PERSONAL...")
    
    users = User.objects.filter(is_active=True).select_related('perfil')
    count = 0
    
    now = timezone.now()
    end_time = now + timezone.timedelta(hours=24)
    
    for user in users:
        # Determine Role based on Group or Profile
        rol = None
        cargo_lower = ""
        
        # 1. Try Groups
        groups = list(user.groups.values_list('name', flat=True))
        
        if 'Medicos' in groups:
            rol = 'MEDICO'
        elif 'Matronas' in groups:
            rol = 'MATRONA'
        elif 'TENS' in groups:
            rol = 'TENS'
        elif 'Administrativos' in groups:
            rol = 'ADMIN'
            
        # 2. Try Profile Cargo if no group strict match but maybe in name
        if not rol and hasattr(user, 'perfil'):
            cargo_lower = user.perfil.cargo.lower()
            if 'medico' in cargo_lower or 'médico' in cargo_lower or 'obstetra' in cargo_lower:
                rol = 'MEDICO'
            elif 'matrona' in cargo_lower or 'matron' in cargo_lower:
                rol = 'MATRONA'
            elif 'tens' in cargo_lower or 'tecnico' in cargo_lower:
                rol = 'TENS'
            elif 'admin' in cargo_lower:
                rol = 'ADMIN'
                
        # 3. Fallback for known test users
        if not rol:
            if 'medico' in user.username.lower(): rol = 'MEDICO'
            elif 'matrona' in user.username.lower(): rol = 'MATRONA'
            elif 'tens' in user.username.lower(): rol = 'TENS'
            elif 'admin' in user.username.lower(): rol = 'ADMIN'
            
        if rol:
            # Create/Update Turn
            # Check if active turn exists
            turno = PersonalTurno.objects.filter(
                usuario=user,
                fecha_fin_turno__gte=now
            ).first()
            
            if turno:
                turno.estado = 'DISPONIBLE'
                turno.fecha_fin_turno = end_time # Extend it
                turno.rol = rol
                turno.save()
                print(f"  🔄 Turno actualizado: {user.username} ({rol})")
            else:
                PersonalTurno.objects.create(
                    usuario=user,
                    rol=rol,
                    estado='DISPONIBLE',
                    fecha_inicio_turno=now,
                    fecha_fin_turno=end_time
                )
                print(f"  ✅ Turno INICIADO: {user.username} ({rol})")
            count += 1
        else:
            print(f"  ⚠️  Usuario sin rol clínico detectado: {user.username}")

    print(f"\n✨ {count} TURNOS ACTIVOS GENERADOS ✨")

if __name__ == '__main__':
    start_all_shifts()
