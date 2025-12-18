import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from partosApp.models import CatalogoTipoParto, CatalogoClasificacionRobson
from recienNacidoApp.models import RegistroRecienNacido, CatalogoSexoRN
from matronaApp.models import CatalogoMedicamento

print("=== Checking Catalogs ===")
print(f"Tipos de Parto: {CatalogoTipoParto.objects.count()}")
print(f"Clasificaciones Robson: {CatalogoClasificacionRobson.objects.count()}")
print(f"Sexos RN: {CatalogoSexoRN.objects.count()}")
print(f"Medicamentos: {CatalogoMedicamento.objects.count()}")

print("\n=== Checking Model Fields ===")
print("RegistroRecienNacido fields:")
for field in RegistroRecienNacido._meta.get_fields():
    print(f"  - {field.name}")
