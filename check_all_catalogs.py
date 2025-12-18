import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from matronaApp.models import CatalogoViaAdministracion, CatalogoTipoPaciente, CatalogoARO
from partosApp.models import CatalogoPosicionParto, CatalogoEstadoPerine, CatalogoCausaCesarea
from recienNacidoApp.models import CatalogoComplicacionesRN
from ingresoPartoApp.models import (
    CatalogoEstadoCervical, CatalogoPosicionFetal, 
    CatalogoAlturaPresentacion, CatalogoEstadoFetal, CatalogoSalaAsignada
)

print("Checking Catalogs...")
print(f"Via Admin: {CatalogoViaAdministracion.objects.count()}")
print(f"Tipo Paciente: {CatalogoTipoPaciente.objects.count()}")
print(f"ARO: {CatalogoARO.objects.count()}")
print(f"Posicion Parto: {CatalogoPosicionParto.objects.count()}")
print(f"Estado Perine: {CatalogoEstadoPerine.objects.count()}")
print(f"Causa Cesarea: {CatalogoCausaCesarea.objects.count()}")
print(f"Complicaciones RN: {CatalogoComplicacionesRN.objects.count()}")
print(f"Estado Cervical: {CatalogoEstadoCervical.objects.count()}")
print(f"Posicion Fetal: {CatalogoPosicionFetal.objects.count()}")
print(f"Altura Presentacion: {CatalogoAlturaPresentacion.objects.count()}")
print(f"Estado Fetal: {CatalogoEstadoFetal.objects.count()}")
print(f"Sala Asignada: {CatalogoSalaAsignada.objects.count()}")
