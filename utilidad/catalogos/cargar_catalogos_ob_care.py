# -*- coding: utf-8 -*-
"""
cargar_catalogos_ob_care.py
Script para cargar y CORREGIR catálogos del sistema OB_CARE
Región de Ñuble - Chile

EJECUCIÓN:
python manage.py shell < cargar_catalogos_ob_care.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from gestionApp.models import (
    CatalogoSexo, CatalogoNacionalidad, CatalogoPuebloOriginario,
    CatalogoEstadoCivil, CatalogoPrevision, CatalogoTurno,
)
from matronaApp.models import CatalogoConsultorioOrigen, CatalogoViaAdministracion
from django.contrib.auth.models import Group

print("=" * 80)
print("🏥 CARGANDO Y REPARANDO CATÁLOGOS - OB_CARE (UTF-8)")
print("=" * 80)

def cargar_catalogo(modelo, datos, nombre):
    print(f"\n📋 {nombre}")
    for item in datos:
        obj, creado = modelo.objects.update_or_create(
            codigo=item['codigo'],
            defaults={
                'nombre': item['nombre'],
                'orden': item['orden'],
                'activo': True
            }
        )
        print(f"  {'✅' if creado else '♻️'} {item['nombre']}")

# 0. GRUPOS
print("\n👥 GRUPOS")
for nombre in ['Medicos', 'Matronas', 'TENS', 'Administradores']:
    Group.objects.get_or_create(name=nombre)
    print(f"  ✅ {nombre}")

# 1. SEXO
cargar_catalogo(CatalogoSexo, [
    {'codigo': 'M', 'nombre': 'Masculino', 'orden': 1},
    {'codigo': 'F', 'nombre': 'Femenino', 'orden': 2},
    {'codigo': 'TM', 'nombre': 'Trans Masculino', 'orden': 3},
], "SEXO")

# 2. NACIONALIDAD
cargar_catalogo(CatalogoNacionalidad, [
    {'codigo': 'CL', 'nombre': 'Chilena', 'orden': 1},
    {'codigo': 'VE', 'nombre': 'Venezolana', 'orden': 2},
    {'codigo': 'PE', 'nombre': 'Peruana', 'orden': 3},
    {'codigo': 'BO', 'nombre': 'Boliviana', 'orden': 4},
    {'codigo': 'CO', 'nombre': 'Colombiana', 'orden': 5},
    {'codigo': 'HT', 'nombre': 'Haitiana', 'orden': 6},
    {'codigo': 'AR', 'nombre': 'Argentina', 'orden': 7},
    {'codigo': 'EC', 'nombre': 'Ecuatoriana', 'orden': 8},
    {'codigo': 'BR', 'nombre': 'Brasileña', 'orden': 9},
    {'codigo': 'DO', 'nombre': 'Dominicana', 'orden': 10},
    {'codigo': 'MX', 'nombre': 'Mexicana', 'orden': 11},
    {'codigo': 'ES', 'nombre': 'Española', 'orden': 12},
    {'codigo': 'US', 'nombre': 'Estadounidense', 'orden': 13},
    {'codigo': 'OT', 'nombre': 'Otra', 'orden': 99},
], "NACIONALIDAD")

# 3. PUEBLOS ORIGINARIOS
cargar_catalogo(CatalogoPuebloOriginario, [
    {'codigo': 'NINGUNO', 'nombre': 'No pertenece', 'orden': 0},
    {'codigo': 'MAPUCHE', 'nombre': 'Mapuche', 'orden': 1},
    {'codigo': 'AYMARA', 'nombre': 'Aymara', 'orden': 2},
    {'codigo': 'DIAGUITA', 'nombre': 'Diaguita', 'orden': 3},
    {'codigo': 'QUECHUA', 'nombre': 'Quechua', 'orden': 4},
    {'codigo': 'ATACAMENO', 'nombre': 'Atacameño / Lickan Antay', 'orden': 5},
    {'codigo': 'COLLA', 'nombre': 'Colla', 'orden': 6},
    {'codigo': 'CHANGO', 'nombre': 'Chango', 'orden': 7},
    {'codigo': 'RAPANUI', 'nombre': 'Rapa Nui', 'orden': 8},
    {'codigo': 'YAGAN', 'nombre': 'Yagán / Yámana', 'orden': 9},
    {'codigo': 'KAWESQAR', 'nombre': 'Kawésqar', 'orden': 10},
], "PUEBLOS ORIGINARIOS")

# 4. ESTADO CIVIL
cargar_catalogo(CatalogoEstadoCivil, [
    {'codigo': 'SOLTERO', 'nombre': 'Soltero/a', 'orden': 1},
    {'codigo': 'CASADO', 'nombre': 'Casado/a', 'orden': 2},
    {'codigo': 'SEPARADO', 'nombre': 'Separado/a', 'orden': 3},
    {'codigo': 'DIVORCIADO', 'nombre': 'Divorciado/a', 'orden': 4},
    {'codigo': 'VIUDO', 'nombre': 'Viudo/a', 'orden': 5},
], "ESTADO CIVIL")

# 5. PREVISIÓN
cargar_catalogo(CatalogoPrevision, [
    {'codigo': 'FONASA_A', 'nombre': 'FONASA A', 'orden': 1},
    {'codigo': 'FONASA_B', 'nombre': 'FONASA B', 'orden': 2},
    {'codigo': 'FONASA_C', 'nombre': 'FONASA C', 'orden': 3},
    {'codigo': 'FONASA_D', 'nombre': 'FONASA D', 'orden': 4},
    {'codigo': 'FONASA_LE', 'nombre': 'FONASA Tramo Libre Elección', 'orden': 5},
    {'codigo': 'ISAPRE', 'nombre': 'ISAPRE', 'orden': 6},
    {'codigo': 'PARTICULAR', 'nombre': 'Particular', 'orden': 7},
], "PREVISIÓN")

# 6. TURNOS
cargar_catalogo(CatalogoTurno, [
    {'codigo': 'MANANA', 'nombre': 'Turno Mañana (08:00 - 16:00)', 'orden': 1},
    {'codigo': 'TARDE', 'nombre': 'Turno Tarde (16:00 - 00:00)', 'orden': 2},
    {'codigo': 'NOCHE', 'nombre': 'Turno Noche (00:00 - 08:00)', 'orden': 3},
    {'codigo': 'LARGO', 'nombre': 'Turno Largo (08:00 - 20:00)', 'orden': 4},
    {'codigo': '24_HORAS', 'nombre': 'Turno 24 Horas (Guardia)', 'orden': 5},
], "TURNOS")

# 8. VÍAS DE ADMINISTRACIÓN
cargar_catalogo(CatalogoViaAdministracion, [
    {'codigo': 'VO', 'nombre': 'Oral (V.O.)', 'orden': 1},
    {'codigo': 'VAG', 'nombre': 'Vaginal', 'orden': 2},
    {'codigo': 'IV', 'nombre': 'Intravenosa (I.V.)', 'orden': 3},
    {'codigo': 'IM', 'nombre': 'Intramuscular (I.M.)', 'orden': 4},
    {'codigo': 'SC', 'nombre': 'Subcutánea (S.C.)', 'orden': 5},
    {'codigo': 'REC', 'nombre': 'Rectal', 'orden': 6},
], "VÍAS DE ADMINISTRACIÓN")

print("\n🎉 CARGA Y REPARACIÓN COMPLETA (UTF-8 OK)")
