import os
import sys

# Configurar entorno Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")

import django
django.setup()

from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User
from gestionProcesosApp.models import PersonalTurno

def populate_turnos():
    print("🚀 GENERANDO TURNOS PARA PERSONAL...")
    
    # 1. Limpiar turnos antiguos (opcional, para limpieza)
    deleted, _ = PersonalTurno.objects.all().delete()
    print(f"🗑️  Turnos anteriores eliminados: {deleted}")
    
    # 2. Buscar personal por grupos
    grupos_roles = {
        'Medicos': 'MEDICO',
        'Matronas': 'MATRONA',
        'TENS': 'TENS'
    }
    
    count = 0
    now = timezone.now()
    fin = now + timedelta(hours=12) # Turno de 12hrs desde ahora
    
    for nombre_grupo, rol_code in grupos_roles.items():
        users = User.objects.filter(groups__name=nombre_grupo, is_active=True)
        print(f"\n🔍 Procesando Grupo {nombre_grupo} ({users.count()} usuarios)...")
        
        for u in users:
            # Crear turno activo
            PersonalTurno.objects.create(
                usuario=u,
                rol=rol_code,
                estado='DISPONIBLE',
                fecha_inicio_turno=now,
                fecha_fin_turno=fin,
                dispositivo_activo=True
            )
            count += 1
            print(f"  ✅ Turno creado: {u.get_full_name()} ({rol_code})")

    print(f"\n✨ FINALIZADO: {count} turnos creados.")

if __name__ == '__main__':
    populate_turnos()
