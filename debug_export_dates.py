import os
import django
from datetime import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from partosApp.models import RegistroParto

print("Checking RegistroParto dates...")
partos = RegistroParto.objects.all()
print(f"Total partos: {partos.count()}")

for p in partos[:10]:
    print(f"ID: {p.id}, Fecha Parto: {p.fecha_hora_parto}, Fecha Creacion: {p.fecha_creacion}")

# Simulate filter
fecha_test = datetime.now().strftime('%Y-%m-%d')
print(f"\nSimulating filter for date: {fecha_test}")

q_gte = RegistroParto.objects.filter(fecha_hora_parto__date__gte=fecha_test)
q_lte = RegistroParto.objects.filter(fecha_hora_parto__date__lte=fecha_test)
q_exact = RegistroParto.objects.filter(fecha_hora_parto__date=fecha_test)

print(f"GTE Count: {q_gte.count()}")
print(f"LTE Count: {q_lte.count()}")
print(f"Exact Count: {q_exact.count()}")

if partos.exists():
    first_date = partos.first().fecha_hora_parto.strftime('%Y-%m-%d')
    print(f"\nSimulating filter for known date: {first_date}")
    q_test = RegistroParto.objects.filter(fecha_hora_parto__date=first_date)
    print(f"Count for {first_date}: {q_test.count()}")
