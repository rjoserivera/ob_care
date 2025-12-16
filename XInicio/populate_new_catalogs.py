
import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from matronaApp.models import CatalogoTipoPaciente, CatalogoDiscapacidad

def populate():
    print("Populating CatalogoTipoPaciente...")
    tipos_paciente = [
        'Fonasa A', 'Fonasa B', 'Fonasa C', 'Fonasa D',
        'Isapre',
        'Particular',
        'Convenio',
        'Otro'
    ]
    
    for nombre in tipos_paciente:
        obj, created = CatalogoTipoPaciente.objects.get_or_create(nombre=nombre)
        if created:
            print(f"- Created: {nombre}")
        else:
            print(f"- Exists: {nombre}")

    print("\nPopulating CatalogoDiscapacidad...")
    discapacidades = [
        'Física',
        'Auditiva',
        'Visual',
        'Intelectual',
        'Psíquica',
        'Visceral',
        'Otra'
    ]
    
    for nombre in discapacidades:
        obj, created = CatalogoDiscapacidad.objects.get_or_create(nombre=nombre)
        if created:
            print(f"- Created: {nombre}")
        else:
            print(f"- Exists: {nombre}")

if __name__ == '__main__':
    populate()
    print("\nDone!")
