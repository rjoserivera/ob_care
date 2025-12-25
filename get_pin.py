import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from ingresoPartoApp.models import FichaParto

def get_latest_pin():
    # Get recent
    fichas = FichaParto.objects.order_by('-fecha_creacion')[:5]
    for ficha in fichas:
        print(f"--- Ficha {ficha.numero_ficha_parto} (ID: {ficha.pk}) ---")
        print(f"PIN: {ficha.pin_inicio_parto}")
        print(f"Pin generado en: {ficha.pin_generado_en}")
        try:
           print(f"Estado (etapa): {ficha.etapa_actual}") # Guessing field name
        except:
           pass

if __name__ == "__main__":
    get_latest_pin()
