import os
import sys
import django
import random
from datetime import timedelta
from django.utils import timezone

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error executing django.setup(): {e}")
    sys.exit(1)

from gestionApp.models import Persona, Paciente, CatalogoPrevision, CatalogoPuebloOriginario
from matronaApp.models import FichaObstetrica, CatalogoConsultorioOrigen, CatalogoDiscapacidad
from ingresoPartoApp.models import FichaParto
from partosApp.models import RegistroParto

def backfill_data():
    print("Iniciando relleno de datos faltantes (VIH y otros)...")
    
    # 1. Cargar catálogos
    pueblos = list(CatalogoPuebloOriginario.objects.filter(activo=True))
    consultorios = list(CatalogoConsultorioOrigen.objects.filter(activo=True))
    discapacidades = list(CatalogoDiscapacidad.objects.filter(activo=True))
    prevision_fonasa = CatalogoPrevision.objects.filter(nombre__icontains='FONASA').first()

    # 2. Fichas Obstétricas (VIH 1 y 2, y otros)
    fichas = FichaObstetrica.objects.all()
    count_vih = 0
    count_extra = 0
    
    for f in fichas:
        updated = False
        
        # --- VIH 1 ---
        # Si tiene resultado pero no fecha (caso común del demo anterior)
        if f.vih_1_resultado and not f.vih_1_fecha:
            # Asignar fecha ~5-6 meses antes de la fecha de creación/parto
            base_date = f.fecha_creacion.date()
            f.vih_1_fecha = base_date - timedelta(days=random.randint(120, 160))
            f.vih_1_realizado = True
            updated = True
            
        # --- VIH 2 (Agregar a algunos) ---
        if not f.vih_2_fecha and random.random() < 0.4: # 40% tiene VIH 2
            base_date = f.fecha_creacion.date()
            f.vih_2_fecha = base_date - timedelta(days=random.randint(30, 60))
            f.vih_2_resultado = 'NEGATIVO'
            f.vih_2_realizado = True
            updated = True
            
        # --- Relleno previo (por si acaso) ---
        if not f.consultorio_origen and consultorios:
            f.consultorio_origen = random.choice(consultorios)
            updated = True
            
        if not f.peso_actual:
            f.peso_actual = random.uniform(55, 95)
            f.talla_actual = random.randint(155, 175)
            updated = True

        if not f.tiene_discapacidad and discapacidades and random.random() < 0.2:
             f.tiene_discapacidad = True
             f.discapacidad = random.choice(discapacidades)
             updated = True

        if updated:
            f.save()
            count_vih += 1

    print(f"Fichas Obstétricas actualizadas (incluye VIH): {count_vih}")
    
    # 3. Ficha de Ingreso a Parto (VIH 3 Intraparto)
    ingresos = FichaParto.objects.all()
    count_ingreso_vih = 0
    
    for mh in ingresos:
        updated = False
        # Si está Pendiente, ponerlo Negativo/No Reagente
        if mh.vih_resultado == 'PENDIENTE':
            mh.vih_resultado = 'NEGATIVO'
            mh.vih_tomado_sala = True
            updated = True
            
        if updated:
            mh.save()
            count_ingreso_vih += 1
            
    print(f"Fichas de Parto (Ingreso) actualizadas (VIH Intraparto): {count_ingreso_vih}")
    print("Corrección finalizada.")

if __name__ == '__main__':
    backfill_data()
