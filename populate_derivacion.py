
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from ingresoPartoApp.models import CatalogoDerivacion

derivaciones = [
    {"codigo": "INFECTO", "nombre": "Infectología"},
    {"codigo": "ARO", "nombre": "Alto Riesgo Obstétrico (ARO)"},
    {"codigo": "GASTRO", "nombre": "Gastroenterología"},
    {"codigo": "NA", "nombre": "No requiere"},
    {"codigo": "OTRA", "nombre": "Otra Especialidad"},
]

print("Populating CatalogoDerivacion...")
for d in derivaciones:
    obj, created = CatalogoDerivacion.objects.get_or_create(
        codigo=d['codigo'],
        defaults={'nombre': d['nombre']}
    )
    if created:
        print(f"Created: {d['nombre']}")
    else:
        print(f"Already exists: {d['nombre']}")

print("Done.")
