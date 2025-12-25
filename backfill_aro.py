import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from matronaApp.models import FichaObstetrica, CatalogoARO

def backfill_aro():
    print("Iniciando backfill de Clasificación ARO...")

    # 1. Asegurar que existan categorías ARO
    nombres_aro = ['Sin Riesgo', 'Alto Riesgo I', 'Alto Riesgo II', 'Alto Riesgo III']
    aros = []
    
    for nombre in nombres_aro:
        aro, created = CatalogoARO.objects.get_or_create(nombre=nombre, defaults={'activo': True})
        if created:
            print(f"Creado nuevo ARO: {nombre}")
        aros.append(aro)
    
    # 2. Actualizar Fichas que no tengan ARO
    fichas = FichaObstetrica.objects.all()
    count = 0
    
    print(f"Procesando {fichas.count()} fichas...")
    
    for ficha in fichas:
        if not ficha.clasificacion_aro:
            ficha.clasificacion_aro = random.choice(aros)
            ficha.save(update_fields=['clasificacion_aro'])
            count += 1
            
    print(f"Backfill completado. {count} fichas actualizadas con Clasificación ARO.")

if __name__ == '__main__':
    backfill_aro()
