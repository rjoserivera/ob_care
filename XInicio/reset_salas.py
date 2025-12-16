
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from gestionProcesosApp.models import Sala

def reset_salas():
    print("🧹 RESETEANDO ESTADO DE SALAS...")
    
    total = Sala.objects.count()
    updated = Sala.objects.update(estado='DISPONIBLE', proceso_activo=None)
    
    print(f"✅ Se han liberado {updated} de {total} salas.")
    print("Todas las salas ahora están 'DISPONIBLE'.")

if __name__ == '__main__':
    reset_salas()
