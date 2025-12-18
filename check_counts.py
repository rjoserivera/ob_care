import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from matronaApp.models import FichaObstetrica
from partosApp.models import RegistroParto

print(f"Fichas Obstétricas: {FichaObstetrica.objects.count()}")
print(f"Registros de Parto: {RegistroParto.objects.count()}")
