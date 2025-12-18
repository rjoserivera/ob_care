import os
import sys
import django
from datetime import datetime, timedelta

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
    print("Checking RegistroParto dates with NEW LOGIC...")
    partos = RegistroParto.objects.all().order_by('-id')
    
    if partos.exists():
        latest = partos.first()
        if latest.fecha_hora_parto:
            test_date_str = latest.fecha_hora_parto.strftime('%Y-%m-%d') # Local string if default TZ
            # Actually strftime uses the object's info. If it is UTC, it prints UTC date.
            # We want to simulate the input "YYYY-MM-DD"
            
            # Use timezone.localtime to see what the user "sees"
            local_dt = timezone.localtime(latest.fecha_hora_parto)
            local_date_str = local_dt.strftime('%Y-%m-%d')
            
            print(f"Latest record local date: {local_date_str} (UTC: {latest.fecha_hora_parto})")
            
            # MANUAL LOGIC (Same as view)
            fi = datetime.strptime(local_date_str, "%Y-%m-%d")
            fi_aware = timezone.make_aware(fi)
            
            ff = datetime.strptime(local_date_str, "%Y-%m-%d")
            ff = ff.replace(hour=23, minute=59, second=59, microsecond=999999)
            ff_aware = timezone.make_aware(ff)
            
            print(f"Filtering range: {fi_aware} to {ff_aware}")
            
            matches = RegistroParto.objects.filter(fecha_hora_parto__gte=fi_aware, fecha_hora_parto__lte=ff_aware)
            print(f"Matches found with new logic: {matches.count()}")
            
            if matches.count() > 0:
                print("SUCCESS: New logic found the record!")
            else:
                print("FAILURE: Matches is still 0.")

    else:
        print("No records found in database.")

except Exception as e:
    print(f"Runtime error: {e}")
