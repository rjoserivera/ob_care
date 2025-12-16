
import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from matronaApp.models import CatalogoARO

def populate_aro():
    print("Populating CatalogoARO...")
    opciones = [
        'Sin Riesgo',
        'Riesgo Bajo',
        'Riesgo Alto',
        'Riesgo Inminente'
    ]
    
    for nombre in opciones:
        obj, created = CatalogoARO.objects.get_or_create(nombre=nombre)
        if created:
            print(f"- Created: {nombre}")
        else:
            print(f"- Exists: {nombre}")

if __name__ == '__main__':
    populate_aro()
