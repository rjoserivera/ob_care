import os
import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from gestionProcesosApp.models import PersonalTurno

def check_counts():
    print(f"Total PersonalTurno: {PersonalTurno.objects.count()}")
    
    now = timezone.now()
    print(f"Current server time: {now}")
    
    available = PersonalTurno.objects.filter(estado='DISPONIBLE', fecha_fin_turno__gte=now)
    print(f"Available (future) shifts: {available.count()}")
    
    # Check max date
    if PersonalTurno.objects.exists():
        latest = PersonalTurno.objects.order_by('-fecha_fin_turno').first()
        print(f"Latest shift ends at: {latest.fecha_fin_turno}")
        
    # Check by role
    for rol in ['MEDICO', 'MATRONA', 'TENS']:
        c = PersonalTurno.objects.filter(rol=rol, estado='DISPONIBLE', fecha_fin_turno__gte=now).count()
        print(f"{rol}: {c}")

if __name__ == "__main__":
    check_counts()
