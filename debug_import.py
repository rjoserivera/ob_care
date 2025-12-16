
import os
import django
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")

try:
    django.setup()
    print("Django setup success")
    from gestionApp.models import Persona
    print("Import Persona success")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
