import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from gestionProcesosApp.models import Sala

def clear_rooms():
    """Libera todas las salas marcándolas como disponibles"""
    salas = Sala.objects.all()
    for sala in salas:
        sala.proceso_activo = None
        sala.estado = 'DISPONIBLE'
        sala.save()
        print(f"Liberada: {sala.nombre}")
    
    print(f"Total: {salas.count()} salas liberadas")

if __name__ == "__main__":
    clear_rooms()
