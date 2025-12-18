import os
import sys
import django
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error executing django.setup(): {e}")
    sys.exit(1)

from partosApp.models import RegistroParto
from django.utils import timezone

try:
    print("Checking RegistroParto dates...")
    partos = RegistroParto.objects.all().order_by('-id')
    print(f"Total partos: {partos.count()}")

    if partos.exists():
        for p in partos[:5]:
            print(f"ID: {p.id}, Fecha Parto: {p.fecha_hora_parto}")
            
            # Check if date corresponds to today
            if p.fecha_hora_parto:
                p_date = p.fecha_hora_parto.date()
                print(f"  -> Date object: {p_date}")

        # Test filtering with string
        latest = partos.first()
        if latest.fecha_hora_parto:
            test_date_str = latest.fecha_hora_parto.strftime('%Y-%m-%d')
            print(f"\nTesting filter for date string: '{test_date_str}'")
            
            # Perform query
            matches = RegistroParto.objects.filter(fecha_hora_parto__date=test_date_str)
            print(f"Matches found: {matches.count()}")
            
            if matches.count() == 0:
                print("WARNING: No matches found for the exact date string!")
                
            # Check range
            matches_gte = RegistroParto.objects.filter(fecha_hora_parto__date__gte=test_date_str)
            print(f"Matches >= {test_date_str}: {matches_gte.count()}")

    else:
        print("No records found in database.")

except Exception as e:
    print(f"Runtime error: {e}")
