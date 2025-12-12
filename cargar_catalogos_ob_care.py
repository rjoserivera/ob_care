"""
cargar_catalogos_ob_care.py
Script para cargar TODOS los catálogos del sistema OB_CARE
Región de Ñuble - Chile

INSTRUCCIONES:
    python manage.py shell < cargar_catalogos_ob_care.py
"""

import os
import django

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
    django.setup()

from gestionApp.models import (
    CatalogoSexo, CatalogoNacionalidad, CatalogoPuebloOriginario,
    CatalogoEstadoCivil, CatalogoPrevision, CatalogoTurno,
)
from matronaApp.models import CatalogoConsultorioOrigen, CatalogoViaAdministracion
from django.contrib.auth.models import Group

print("=" * 80)
print("  🏥 CARGANDO CATÁLOGOS - OB_CARE - Región de Ñuble")
print("=" * 80)

# 0. GRUPOS (ROLES)
print("\n👥 GRUPOS DE DJANGO (ROLES)")
for nombre in ['Medicos', 'Matronas', 'TENS', 'Administradores']:
    g, c = Group.objects.get_or_create(name=nombre)
    print(f"  {'✅' if c else '⏭️ '} {nombre}")

# 1. SEXO
print("\n📋 1. SEXO")
for item in [
    {'codigo': 'M', 'nombre': 'Masculino', 'orden': 1},
    {'codigo': 'F', 'nombre': 'Femenino', 'orden': 2},
    {'codigo': 'TM', 'nombre': 'Trans Masculino', 'orden': 3},
]:
    o, c = CatalogoSexo.objects.get_or_create(codigo=item['codigo'], defaults={'nombre': item['nombre'], 'orden': item['orden'], 'activo': True})
    print(f"  {'✅' if c else '⏭️ '} {item['nombre']}")

# 2. NACIONALIDAD
print("\n📋 2. NACIONALIDAD")
for item in [
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
]:
    o, c = CatalogoNacionalidad.objects.get_or_create(codigo=item['codigo'], defaults={'nombre': item['nombre'], 'orden': item['orden'], 'activo': True})
    print(f"  {'✅' if c else '⏭️ '} {item['nombre']}")

# 3. PUEBLOS ORIGINARIOS
print("\n📋 3. PUEBLOS ORIGINARIOS")
for item in [
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
]:
    o, c = CatalogoPuebloOriginario.objects.get_or_create(codigo=item['codigo'], defaults={'nombre': item['nombre'], 'orden': item['orden'], 'activo': True})
    print(f"  {'✅' if c else '⏭️ '} {item['nombre']}")

# 4. ESTADO CIVIL
print("\n📋 4. ESTADO CIVIL")
for item in [
    {'codigo': 'SOLTERO', 'nombre': 'Soltero/a', 'orden': 1},
    {'codigo': 'CASADO', 'nombre': 'Casado/a', 'orden': 2},
    {'codigo': 'SEPARADO', 'nombre': 'Separado/a', 'orden': 3},
    {'codigo': 'DIVORCIADO', 'nombre': 'Divorciado/a', 'orden': 4},
    {'codigo': 'VIUDO', 'nombre': 'Viudo/a', 'orden': 5},
]:
    o, c = CatalogoEstadoCivil.objects.get_or_create(codigo=item['codigo'], defaults={'nombre': item['nombre'], 'orden': item['orden'], 'activo': True})
    print(f"  {'✅' if c else '⏭️ '} {item['nombre']}")

# 5. PREVISIÓN
print("\n📋 5. PREVISIÓN DE SALUD")
for item in [
    {'codigo': 'FONASA_A', 'nombre': 'FONASA A', 'orden': 1},
    {'codigo': 'FONASA_B', 'nombre': 'FONASA B', 'orden': 2},
    {'codigo': 'FONASA_C', 'nombre': 'FONASA C', 'orden': 3},
    {'codigo': 'FONASA_D', 'nombre': 'FONASA D', 'orden': 4},
    {'codigo': 'FONASA_LE', 'nombre': 'FONASA Tramo Libre Elección', 'orden': 5},
    {'codigo': 'ISAPRE', 'nombre': 'ISAPRE', 'orden': 6},
    {'codigo': 'PARTICULAR', 'nombre': 'Particular', 'orden': 7},
]:
    o, c = CatalogoPrevision.objects.get_or_create(codigo=item['codigo'], defaults={'nombre': item['nombre'], 'orden': item['orden'], 'activo': True})
    print(f"  {'✅' if c else '⏭️ '} {item['nombre']}")

# 6. TURNOS
print("\n📋 6. TURNOS HOSPITALARIOS")
for item in [
    {'codigo': 'MANANA', 'nombre': 'Turno Mañana (08:00 - 16:00)', 'orden': 1},
    {'codigo': 'TARDE', 'nombre': 'Turno Tarde (16:00 - 00:00)', 'orden': 2},
    {'codigo': 'NOCHE', 'nombre': 'Turno Noche (00:00 - 08:00)', 'orden': 3},
    {'codigo': 'LARGO', 'nombre': 'Turno Largo (08:00 - 20:00)', 'orden': 4},
    {'codigo': '24_HORAS', 'nombre': 'Turno 24 Horas (Guardia)', 'orden': 5},
]:
    o, c = CatalogoTurno.objects.get_or_create(codigo=item['codigo'], defaults={'nombre': item['nombre'], 'orden': item['orden'], 'activo': True})
    print(f"  {'✅' if c else '⏭️ '} {item['nombre']}")

# 7. CONSULTORIOS ÑUBLE
print("\n📋 7. CONSULTORIOS - REGIÓN DE ÑUBLE")
for item in [
    # CHILLÁN
    {'codigo': 'CESFAM_ISABEL_RIQUELME', 'nombre': 'CESFAM Isabel Riquelme (Chillán)', 'orden': 1},
    {'codigo': 'CESFAM_LOS_VOLCANES', 'nombre': 'CESFAM Los Volcanes (Chillán)', 'orden': 2},
    {'codigo': 'CESFAM_SAN_RAMON', 'nombre': 'CESFAM San Ramón Nonato (Chillán)', 'orden': 3},
    {'codigo': 'CESFAM_SOL_ORIENTE', 'nombre': 'CESFAM Sol de Oriente (Chillán)', 'orden': 4},
    {'codigo': 'CESFAM_ULTRAESTACION', 'nombre': 'CESFAM Ultraestación Dr. Raúl San Martín (Chillán)', 'orden': 5},
    {'codigo': 'CESFAM_VIOLETA_PARRA', 'nombre': 'CESFAM Violeta Parra (Chillán)', 'orden': 6},
    {'codigo': 'CESFAM_QUINCHAMALI', 'nombre': 'CESFAM Quinchamalí (Chillán Rural)', 'orden': 7},
    # PRIVADOS
    {'codigo': 'CONS_ACHS', 'nombre': 'Consultorio AChS Chillán', 'orden': 10},
    {'codigo': 'CONS_MUTUAL', 'nombre': 'Consultorio Mutual Seguridad Chillán', 'orden': 11},
    # CHILLÁN VIEJO
    {'codigo': 'CESFAM_BACHELET', 'nombre': 'CESFAM Dra. Michelle Bachelet (Chillán Viejo)', 'orden': 15},
    # SAN CARLOS
    {'codigo': 'CESFAM_BALDECCHI', 'nombre': 'CESFAM Teresa Baldecchi (San Carlos)', 'orden': 20},
    {'codigo': 'CESFAM_DURAN', 'nombre': 'CESFAM Dr. José Durán Trujillo (San Carlos)', 'orden': 21},
    # COIHUECO
    {'codigo': 'CESFAM_COIHUECO', 'nombre': 'CESFAM Michelle Chandía (Coihueco)', 'orden': 25},
    {'codigo': 'CESFAM_TRES_ESQUINAS', 'nombre': 'CESFAM Luis Montecinos (Tres Esquinas)', 'orden': 26},
    # RÁNQUIL
    {'codigo': 'CESFAM_NIPAS', 'nombre': 'CESFAM Ñipas (Ránquil)', 'orden': 30},
    # YUNGAY
    {'codigo': 'CESFAM_CAMPANARIO', 'nombre': 'CESFAM Campanario (Yungay)', 'orden': 35},
    {'codigo': 'HOSP_YUNGAY', 'nombre': 'Hospital Pedro Morales (Yungay)', 'orden': 36},
    # SAN FABIÁN
    {'codigo': 'CESFAM_SAN_FABIAN', 'nombre': 'CESFAM San Fabián', 'orden': 40},
    # PINTO
    {'codigo': 'CESFAM_PINTO', 'nombre': 'CESFAM de Pinto', 'orden': 45},
    # ÑIQUÉN
    {'codigo': 'CESFAM_SAN_GREGORIO', 'nombre': 'CESFAM San Gregorio (Ñiquén)', 'orden': 50},
    # HOSPITAL
    {'codigo': 'HOSP_HERMINDA', 'nombre': 'Hospital Herminda Martín (Chillán)', 'orden': 60},
    # OTROS
    {'codigo': 'PARTICULAR', 'nombre': 'Atención Particular', 'orden': 90},
    {'codigo': 'OTRO', 'nombre': 'Otro', 'orden': 99},
]:
    o, c = CatalogoConsultorioOrigen.objects.get_or_create(codigo=item['codigo'], defaults={'nombre': item['nombre'], 'orden': item['orden'], 'activo': True})
    print(f"  {'✅' if c else '⏭️ '} {item['nombre']}")

# 8. VÍAS DE ADMINISTRACIÓN
print("\n📋 8. VÍAS DE ADMINISTRACIÓN")
for item in [
    {'codigo': 'VO', 'nombre': 'Oral (V.O.)', 'orden': 1},
    {'codigo': 'VAG', 'nombre': 'Vaginal', 'orden': 2},
    {'codigo': 'IV', 'nombre': 'Intravenosa (I.V.)', 'orden': 3},
    {'codigo': 'IM', 'nombre': 'Intramuscular (I.M.)', 'orden': 4},
    {'codigo': 'SC', 'nombre': 'Subcutánea (S.C.)', 'orden': 5},
    {'codigo': 'REC', 'nombre': 'Rectal', 'orden': 6},
]:
    o, c = CatalogoViaAdministracion.objects.get_or_create(codigo=item['codigo'], defaults={'nombre': item['nombre'], 'orden': item['orden'], 'activo': True})
    print(f"  {'✅' if c else '⏭️ '} {item['nombre']}")

# RESUMEN
print("\n" + "=" * 80)
print("  ✅ CARGA COMPLETADA")
print("=" * 80)
print(f"\n📊 RESUMEN:")
print(f"   Grupos:        {Group.objects.count()}")
print(f"   Sexos:         {CatalogoSexo.objects.count()}")
print(f"   Nacionalidades:{CatalogoNacionalidad.objects.count()}")
print(f"   Pueblos Orig.: {CatalogoPuebloOriginario.objects.count()}")
print(f"   Estados Civ.:  {CatalogoEstadoCivil.objects.count()}")
print(f"   Previsiones:   {CatalogoPrevision.objects.count()}")
print(f"   Turnos:        {CatalogoTurno.objects.count()}")
print(f"   Consultorios:  {CatalogoConsultorioOrigen.objects.count()}")
print(f"   Vías Admin.:   {CatalogoViaAdministracion.objects.count()}")
print("\n🎉 Listo!")