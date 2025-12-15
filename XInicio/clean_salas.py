
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from gestionProcesosApp.models import Sala

def clean_salas():
    print("🧹 LIMPIANDO SALAS EXTRA...")
    
    # Keep IDs 1, 2, 3 (Sala Parto 1, 2, 3)
    # Delete everything else
    
    deleted_count, _ = Sala.objects.exclude(id__in=[1, 2, 3]).delete()
    
    print(f"✅ Se han eliminado {deleted_count} salas extra.")
    
    print("\nSalas actuales:")
    for s in Sala.objects.all().order_by('id'):
        print(f" - [{s.id}] {s.nombre} ({s.estado})")

if __name__ == '__main__':
    clean_salas()
