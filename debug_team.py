import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from ingresoPartoApp.models import FichaParto
from gestionProcesosApp.models import AsignacionPersonal
from gestionProcesosApp.pin_utils import equipo_completo

def check_ficha_status():
    ficha = FichaParto.objects.order_by('-fecha_creacion').first()
    if not ficha:
        print("No ficha found")
        return

    print(f"Checking Ficha: {ficha.numero_ficha_parto} (ID: {ficha.pk})")
    print(f"PIN: {ficha.pin_inicio_parto}")
    
    # Requirements
    cantidad_bebes = ficha.ficha_obstetrica.cantidad_bebes
    if cantidad_bebes < 1: cantidad_bebes = 1
    
    print(f"Bebes: {cantidad_bebes}")
    print(f"Target: M:{cantidad_bebes}, Mat:{cantidad_bebes*2}, T:{cantidad_bebes*3}")
    
    # Actual
    asignaciones = AsignacionPersonal.objects.filter(proceso=ficha, estado_respuesta='ACEPTADA')
    m = asignaciones.filter(personal__rol='MEDICO').count()
    mat = asignaciones.filter(personal__rol='MATRONA').count()
    t = asignaciones.filter(personal__rol='TENS').count()
    
    print(f"Actual: M:{m}, Mat:{mat}, T:{t}")
    
    completo = equipo_completo(ficha)
    print(f"Equipo Completo? {completo}")
    
    if completo and not ficha.pin_inicio_parto:
        print("Strange: Equipo Completo but no PIN.")

if __name__ == "__main__":
    check_ficha_status()
