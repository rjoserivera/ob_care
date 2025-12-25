import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from gestionProcesosApp.models import AsignacionPersonal
from ingresoPartoApp.models import FichaParto

def check_assignments():
    try:
        ficha = FichaParto.objects.get(pk=89) # P-FO-000107
        asignaciones = AsignacionPersonal.objects.filter(proceso=ficha)
        
        print(f"Assignments for Ficha {ficha.numero_ficha_parto}:")
        for a in asignaciones:
            u = a.personal.usuario
            cid = u.perfil.telegram_chat_id if hasattr(u, 'perfil') else "N/A"
            print(f"- {u.username} ({a.personal.rol}): Result={a.estado_respuesta}, ChatID={cid}")
            
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check_assignments()
