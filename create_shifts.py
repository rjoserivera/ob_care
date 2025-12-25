import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from django.contrib.auth.models import User
from gestionProcesosApp.models import PersonalTurno

def create_shifts():
    users = User.objects.filter(is_active=True).exclude(username='admin')
    print(f"Found {users.count()} users.")
    
    start = timezone.now()
    end = start + timedelta(hours=24)
    
    created = 0
    for u in users:
        # Determine role based on username or group?
        # Assuming demo users have roles in their profile or simple mapping
        # Let's check groups
        groups = u.groups.values_list('name', flat=True)
        role = 'MATRONA' # Default
        if 'Medico' in groups or 'médico' in u.username.lower():
            role = 'MEDICO'
        elif 'TENS' in groups or 'tens' in u.username.lower():
            role = 'TENS'
        elif 'Matrona' in groups or 'matrona' in u.username.lower():
            role = 'MATRONA'
            
        # Create shift
        PersonalTurno.objects.create(
            usuario=u,
            rol=role,
            fecha_inicio_turno=start,
            fecha_fin_turno=end,
            estado='DISPONIBLE'
        )
        created += 1
        print(f"Created shift for {u.username} as {role}")

    print(f"Created {created} shifts.")

if __name__ == "__main__":
    create_shifts()
