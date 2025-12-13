# -*- coding: utf-8 -*-
"""
utilidad/catalogos/cargar_medicamentos.py
Script para cargar y corregir medicamentos obstétricos
Ejecución:
python utilidad/catalogos/cargar_medicamentos.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from matronaApp.models import CatalogoMedicamento, CatalogoViaAdministracion

print("🔧 Cargando y reparando catálogo de medicamentos obstétricos...")

# ============================
# VÍAS DE ADMINISTRACIÓN
# ============================
vias_data = [
    ('VO', 'Vía Oral', 1),
    ('IV', 'Intravenosa', 2),
    ('IM', 'Intramuscular', 3),
    ('SC', 'Subcutánea', 4),
    ('TOP', 'Tópica', 5),
    ('REC', 'Rectal', 6),
    ('VAG', 'Vaginal', 7),
    ('INH', 'Inhalatoria', 8),
    ('PERID', 'Peridural / Epidural', 9),
]

print("\n📋 Vías de administración")
for codigo, nombre, orden in vias_data:
    CatalogoViaAdministracion.objects.update_or_create(
        codigo=codigo,
        defaults={
            'nombre': nombre,
            'orden': orden,
            'activo': True
        }
    )
    print(f"  ♻️ {nombre}")

# ============================
# MEDICAMENTOS
# ============================
medicamentos_data = [
    ('OXI-5', 'Oxitocina', 'Oxitocina', 'Ampolla', '5 UI/ml', 'UI'),
    ('OXI-10', 'Oxitocina', 'Oxitocina', 'Ampolla', '10 UI/ml', 'UI'),

    ('NIF-10', 'Nifedipino', 'Nifedipino', 'Cápsula', '10 mg', 'mg'),
    ('BET-12', 'Betametasona', 'Betametasona', 'Ampolla', '12 mg/2 ml', 'mg'),
    ('TRA-100', 'Tramadol', 'Tramadol', 'Ampolla', '100 mg/2 ml', 'mg'),
    ('BUP-05', 'Bupivacaína', 'Bupivacaína', 'Ampolla', '0.5 %', '%'),
    ('MIS-200', 'Misoprostol', 'Misoprostol', 'Comprimido', '200 mcg', 'mcg'),
    ('OND-8', 'Ondansetrón', 'Ondansetrón', 'Ampolla', '8 mg/4 ml', 'mg'),
]

creados = 0
actualizados = 0

print("\n💊 Medicamentos")
for codigo, nombre, generico, presentacion, concentracion, unidad in medicamentos_data:
    _, created = CatalogoMedicamento.objects.update_or_create(
        codigo=codigo,
        defaults={
            'nombre': nombre,
            'nombre_generico': generico,
            'presentacion': presentacion,
            'concentracion': concentracion,
            'unidad': unidad,
            'activo': True
        }
    )
    if created:
        creados += 1
    else:
        actualizados += 1

print("\n✅ Proceso completado correctamente")
print(f"   • Medicamentos creados: {creados}")
print(f"   • Medicamentos actualizados: {actualizados}")
print(f"   • Total en catálogo: {CatalogoMedicamento.objects.count()}")
