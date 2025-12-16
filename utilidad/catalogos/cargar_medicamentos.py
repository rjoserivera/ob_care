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
    # --- UTEROTÓNICOS ---
    ('OXI-5', 'Oxitocina', 'Oxitocina', 'Ampolla', '5 UI/ml', 'UI'),
    ('OXI-10', 'Oxitocina', 'Oxitocina', 'Ampolla', '10 UI/ml', 'UI'),
    ('CAR-100', 'Carbetocina', 'Carbetocina', 'Ampolla', '100 mcg/ml', 'mcg'),
    ('MIS-200', 'Misoprostol', 'Misoprostol', 'Comprimido', '200 mcg', 'mcg'),
    ('MET-02', 'Metilergometrina', 'Metilergometrina', 'Ampolla', '0.2 mg/ml', 'mg'),

    # --- ANALGÉSICOS / ANESTÉSICOS ---
    ('PAR-500', 'Paracetamol', 'Paracetamol', 'Comprimido', '500 mg', 'mg'),
    ('PAR-1G', 'Paracetamol', 'Paracetamol', 'Frasco', '1 g', 'g'),
    ('IBU-400', 'Ibuprofeno', 'Ibuprofeno', 'Gragea', '400 mg', 'mg'),
    ('IBU-600', 'Ibuprofeno', 'Ibuprofeno', 'Comprimido', '600 mg', 'mg'),
    ('KET-30', 'Ketorolaco', 'Ketorolaco', 'Ampolla', '30 mg/ml', 'mg'),
    ('TRA-100', 'Tramadol', 'Tramadol', 'Ampolla', '100 mg/2 ml', 'mg'),
    ('LID-2', 'Lidocaína', 'Lidocaína', 'Frasco', '2%', '%'),
    ('BUP-05', 'Bupivacaína', 'Bupivacaína', 'Ampolla', '0.5%', '%'),

    # --- ANTIBIÓTICOS ---
    ('CEF-1G', 'Cefazolina', 'Cefazolina', 'Frasco', '1 g', 'g'),
    ('AMP-500', 'Ampicilina', 'Ampicilina', 'Frasco', '500 mg', 'mg'),
    ('PEN-5M', 'Penicilina Sódica', 'Penicilina G Sódica', 'Frasco', '5.000.000 UI', 'UI'),
    ('CLI-600', 'Clindamicina', 'Clindamicina', 'Ampolla', '600 mg/4 ml', 'mg'),
    ('GEN-80', 'Gentamicina', 'Gentamicina', 'Ampolla', '80 mg/2 ml', 'mg'),

    # --- ANTIHIPERTENSIVOS ---
    ('NIF-10', 'Nifedipino', 'Nifedipino', 'Cápsula', '10 mg', 'mg'),
    ('NIF-20', 'Nifedipino', 'Nifedipino', 'Comprimido', '20 mg', 'mg'),
    ('MET-250', 'Metildopa', 'Metildopa', 'Comprimido', '250 mg', 'mg'),
    ('MET-500', 'Metildopa', 'Metildopa', 'Comprimido', '500 mg', 'mg'),
    ('LAB-100', 'Labetalol', 'Labetalol', 'Ampolla', '100 mg/20 ml', 'mg'), # IV
    ('LAB-200', 'Labetalol', 'Labetalol', 'Comprimido', '200 mg', 'mg'), # Oral

    # --- OTROS ---
    ('SULF-M', 'Sulfato de Magnesio', 'Sulfato de Magnesio', 'Ampolla', '25%', '%'),
    ('GLU-10', 'Gluconato de Calcio', 'Gluconato de Calcio', 'Ampolla', '10%', '%'),
    ('OND-4', 'Ondansetrón', 'Ondansetrón', 'Ampolla', '4 mg/2 ml', 'mg'),
    ('OND-8', 'Ondansetrón', 'Ondansetrón', 'Ampolla', '8 mg/4 ml', 'mg'),
    ('FER-200', 'Sulfato Ferroso', 'Sulfato Ferroso', 'Gragea', '200 mg', 'mg'),
    ('ACI-5', 'Ácido Tranexámico', 'Ácido Tranexámico', 'Ampolla', '500 mg/5 ml', 'mg'),
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
