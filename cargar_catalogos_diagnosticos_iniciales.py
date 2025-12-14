"""
script_cargar_catalogos.py
Script para cargar todos los catálogos iniciales en la base de datos
Ejecutar con: python manage.py shell < script_cargar_catalogos.py
O dentro de Django shell: exec(open('script_cargar_catalogos.py').read())
"""

from matronaApp.models import (
    CatalogoViaAdministracion,
    CatalogoConsultorioOrigen,
)
from ingresoPartoApp.models import (
    CatalogoTipoPaciente,
    CatalogoOrigenIngreso,
    CatalogoOrdenVIH,
    CatalogoResultadoSGB,
    CatalogoResultadoVDRL,
    CatalogoTipoRoturaMembranas,
    CatalogoRegimentoTrabajoParto,
)
from partosApp.models import (
    CatalogoTipoParto,
    CatalogoClasificacionRobson,
    CatalogoPosicionParto,
    CatalogoEstadoPerine,
    CatalogoCausaCesarea,
    CatalogoMotivoPartoNoAcompanado,
    CatalogoPersonaAcompanante,
    CatalogoMetodoNoFarmacologico,
)
from recienNacidoApp.models import CatalogoSexoRN

print("=" * 80)
print("INICIANDO CARGA DE CATÁLOGOS")
print("=" * 80)

# ============================================
# MATRONAAPP
# ============================================

print("\n📋 matronaApp Catálogos...")

# Vías de Administración
vias_admin = [
    {'codigo': 'ORAL', 'nombre': 'Oral', 'orden': 1},
    {'codigo': 'IV', 'nombre': 'Intravenosa', 'orden': 2},
    {'codigo': 'IM', 'nombre': 'Intramuscular', 'orden': 3},
    {'codigo': 'SC', 'nombre': 'Subcutánea', 'orden': 4},
    {'codigo': 'IR', 'nombre': 'Intrarraquídea', 'orden': 5},
    {'codigo': 'TOPICA', 'nombre': 'Tópica', 'orden': 6},
]

for via in vias_admin:
    obj, created = CatalogoViaAdministracion.objects.get_or_create(
        codigo=via['codigo'],
        defaults={
            'nombre': via['nombre'],
            'orden': via['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Vía de Administración: {via['nombre']}")

# Consultorios de Origen
consultorios = [
    {'codigo': 'CONS_001', 'nombre': 'Consultorio Centro de Salud', 'orden': 1},
    {'codigo': 'CONS_002', 'nombre': 'Consultorio Privado', 'orden': 2},
    {'codigo': 'CONS_003', 'nombre': 'Hospital Público', 'orden': 3},
    {'codigo': 'CONS_004', 'nombre': 'Clínica Privada', 'orden': 4},
    {'codigo': 'CONS_005', 'nombre': 'Matrona Independiente', 'orden': 5},
]

for cons in consultorios:
    obj, created = CatalogoConsultorioOrigen.objects.get_or_create(
        codigo=cons['codigo'],
        defaults={
            'nombre': cons['nombre'],
            'orden': cons['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Consultorio: {cons['nombre']}")

# ============================================
# INGRESOPARTOAPP
# ============================================

print("\n📋 ingresoPartoApp Catálogos...")

# Tipo de Paciente
tipos_paciente = [
    {'codigo': 'PRIM', 'descripcion': 'Primigesta', 'orden': 1},
    {'codigo': 'MULT', 'descripcion': 'Multípara', 'orden': 2},
    {'codigo': 'GRAN_MULT', 'descripcion': 'Gran Multípara', 'orden': 3},
]

for tp in tipos_paciente:
    obj, created = CatalogoTipoPaciente.objects.get_or_create(
        codigo=tp['codigo'],
        defaults={
            'descripcion': tp['descripcion'],
            'orden': tp['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Tipo Paciente: {tp['descripcion']}")

# Origen Ingreso
origenes = [
    {'codigo': 'SALA', 'descripcion': 'Sala de Parto', 'orden': 1},
    {'codigo': 'UEGO', 'descripcion': 'UEGO', 'orden': 2},
    {'codigo': 'PREPARTOS', 'descripcion': 'Prepartos', 'orden': 3},
    {'codigo': 'UCI', 'descripcion': 'UCI', 'orden': 4},
]

for ori in origenes:
    obj, created = CatalogoOrigenIngreso.objects.get_or_create(
        codigo=ori['codigo'],
        defaults={
            'descripcion': ori['descripcion'],
            'orden': ori['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Origen Ingreso: {ori['descripcion']}")

# Orden VIH
ordenes_vih = [
    {'codigo': '1', 'descripcion': 'Primer orden', 'orden': 1},
    {'codigo': '2', 'descripcion': 'Segundo orden', 'orden': 2},
    {'codigo': '3', 'descripcion': 'Tercer orden', 'orden': 3},
]

for vh in ordenes_vih:
    obj, created = CatalogoOrdenVIH.objects.get_or_create(
        codigo=vh['codigo'],
        defaults={
            'descripcion': vh['descripcion'],
            'orden': vh['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Orden VIH: {vh['descripcion']}")

# Resultado SGB
resultados_sgb = [
    {'codigo': 'POS', 'descripcion': 'Positivo', 'orden': 1},
    {'codigo': 'NEG', 'descripcion': 'Negativo', 'orden': 2},
    {'codigo': 'NO_REALIZADO', 'descripcion': 'No Realizado', 'orden': 3},
]

for sgb in resultados_sgb:
    obj, created = CatalogoResultadoSGB.objects.get_or_create(
        codigo=sgb['codigo'],
        defaults={
            'descripcion': sgb['descripcion'],
            'orden': sgb['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Resultado SGB: {sgb['descripcion']}")

# Resultado VDRL
resultados_vdrl = [
    {'codigo': 'REACTIVO', 'descripcion': 'Reactivo', 'orden': 1},
    {'codigo': 'NO_REACTIVO', 'descripcion': 'No Reactivo', 'orden': 2},
    {'codigo': 'NO_REALIZADO', 'descripcion': 'No Realizado', 'orden': 3},
]

for vdrl in resultados_vdrl:
    obj, created = CatalogoResultadoVDRL.objects.get_or_create(
        codigo=vdrl['codigo'],
        defaults={
            'descripcion': vdrl['descripcion'],
            'orden': vdrl['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Resultado VDRL: {vdrl['descripcion']}")

# Tipo Rotura Membranas
roturas = [
    {'codigo': 'IOP', 'descripcion': 'Integras (Sin Rotura)', 'abreviatura': 'IOP', 'orden': 1},
    {'codigo': 'RAM', 'descripcion': 'Rotura Antes de Admisión a Maternidad', 'abreviatura': 'RAM', 'orden': 2},
    {'codigo': 'REM', 'descripcion': 'Rotura En Maternidad', 'abreviatura': 'REM', 'orden': 3},
    {'codigo': 'RPM', 'descripcion': 'Ruptura Prematura de Membranas', 'abreviatura': 'RPM', 'orden': 4},
]

for rot in roturas:
    obj, created = CatalogoTipoRoturaMembranas.objects.get_or_create(
        codigo=rot['codigo'],
        defaults={
            'descripcion': rot['descripcion'],
            'abreviatura': rot['abreviatura'],
            'orden': rot['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Tipo Rotura: {rot['abreviatura']} - {rot['descripcion']}")

# Régimen Trabajo Parto
regimenes = [
    {'codigo': 'CERO', 'descripcion': 'Cero (Ayuno)', 'orden': 1},
    {'codigo': 'LIQUIDO', 'descripcion': 'Líquido', 'orden': 2},
    {'codigo': 'COMUN', 'descripcion': 'Común/Dieta Regular', 'orden': 3},
    {'codigo': 'OTRO', 'descripcion': 'Otro', 'orden': 4},
]

for reg in regimenes:
    obj, created = CatalogoRegimentoTrabajoParto.objects.get_or_create(
        codigo=reg['codigo'],
        defaults={
            'descripcion': reg['descripcion'],
            'orden': reg['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Régimen: {reg['descripcion']}")

# ============================================
# PARTOSAPP
# ============================================

print("\n📋 partosApp Catálogos...")

# Tipo Parto
tipos_parto = [
    {'codigo': 'EUTOCICO', 'descripcion': 'Eutócico (Vaginal)', 'orden': 1},
    {'codigo': 'DISTOCICO', 'descripcion': 'Distócico (Complicado)', 'orden': 2},
    {'codigo': 'CES_URGENCIA', 'descripcion': 'Cesárea de Urgencia', 'orden': 3},
    {'codigo': 'CES_ELECTIVA', 'descripcion': 'Cesárea Electiva', 'orden': 4},
]

for tp in tipos_parto:
    obj, created = CatalogoTipoParto.objects.get_or_create(
        codigo=tp['codigo'],
        defaults={
            'descripcion': tp['descripcion'],
            'orden': tp['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Tipo Parto: {tp['descripcion']}")

# Clasificación de Robson (grupos 1-10)
robsons = [
    {'numero_grupo': 1, 'descripcion': 'Grupo 1 - Multíparas sin cicatriz, eutócicas, espontáneo', 'orden': 1},
    {'numero_grupo': 2, 'descripcion': 'Grupo 2 - Multíparas sin cicatriz, inducidas o aceleradas', 'orden': 2},
    {'numero_grupo': 3, 'descripcion': 'Grupo 3 - Multíparas con cicatriz, eutócicas', 'orden': 3},
    {'numero_grupo': 4, 'descripcion': 'Grupo 4 - Multíparas con cicatriz, inducidas o aceleradas', 'orden': 4},
    {'numero_grupo': 5, 'descripcion': 'Grupo 5 - Primíparas, eutócicas, espontáneo', 'orden': 5},
    {'numero_grupo': 6, 'descripcion': 'Grupo 6 - Primíparas, inducidas o aceleradas', 'orden': 6},
    {'numero_grupo': 7, 'descripcion': 'Grupo 7 - Multíparas con cicatriz, presentación no cefálica', 'orden': 7},
    {'numero_grupo': 8, 'descripcion': 'Grupo 8 - Presentación no cefálica (multíparas y primíparas)', 'orden': 8},
    {'numero_grupo': 9, 'descripcion': 'Grupo 9 - Parto único en transverso', 'orden': 9},
    {'numero_grupo': 10, 'descripcion': 'Grupo 10 - Cesáreas previas', 'orden': 10},
]

for rob in robsons:
    obj, created = CatalogoClasificacionRobson.objects.get_or_create(
        numero_grupo=rob['numero_grupo'],
        defaults={
            'codigo': f"ROBSON_{rob['numero_grupo']}",
            'descripcion': rob['descripcion'],
            'orden': rob['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Robson Grupo {rob['numero_grupo']}")

# Posición Parto
posiciones = [
    {'codigo': 'SEMISENTADA', 'descripcion': 'Semisentada', 'orden': 1},
    {'codigo': 'SENTADA', 'descripcion': 'Sentada', 'orden': 2},
    {'codigo': 'LITOTOMIA', 'descripcion': 'Litotomía', 'orden': 3},
    {'codigo': 'D_DORSAL', 'descripcion': 'Decúbito Dorsal', 'orden': 4},
    {'codigo': 'CUADRUPEDA', 'descripcion': 'Cuadrúpeda', 'orden': 5},
    {'codigo': 'D_LATERAL', 'descripcion': 'Decúbito Lateral', 'orden': 6},
    {'codigo': 'DE_PIE', 'descripcion': 'De Pie', 'orden': 7},
    {'codigo': 'CUCLILLAS', 'descripcion': 'En Cuclillas', 'orden': 8},
    {'codigo': 'OTRO', 'descripcion': 'Otra Posición', 'orden': 9},
]

for pos in posiciones:
    obj, created = CatalogoPosicionParto.objects.get_or_create(
        codigo=pos['codigo'],
        defaults={
            'descripcion': pos['descripcion'],
            'orden': pos['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Posición: {pos['descripcion']}")

# Estado Periné
periné_estados = [
    {'codigo': 'INTEGRO', 'descripcion': 'Íntegro', 'orden': 1},
    {'codigo': 'DESGARRO_G1', 'descripcion': 'Desgarro Grado 1', 'orden': 2},
    {'codigo': 'DESGARRO_G2', 'descripcion': 'Desgarro Grado 2', 'orden': 3},
    {'codigo': 'DESGARRO_G3A', 'descripcion': 'Desgarro Grado 3A', 'orden': 4},
    {'codigo': 'DESGARRO_G3B', 'descripcion': 'Desgarro Grado 3B', 'orden': 5},
    {'codigo': 'DESGARRO_G3C', 'descripcion': 'Desgarro Grado 3C', 'orden': 6},
    {'codigo': 'DESGARRO_G4', 'descripcion': 'Desgarro Grado 4', 'orden': 7},
    {'codigo': 'FISURA', 'descripcion': 'Fisura', 'orden': 8},
    {'codigo': 'EPISIOTOMIA', 'descripcion': 'Episiotomía', 'orden': 9},
]

for per in periné_estados:
    obj, created = CatalogoEstadoPerine.objects.get_or_create(
        codigo=per['codigo'],
        defaults={
            'descripcion': per['descripcion'],
            'orden': per['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Estado Periné: {per['descripcion']}")

# Causa Cesárea
causas_cesarea = [
    {'codigo': 'DCP', 'descripcion': 'Desproporción Céfalo-Pélvica', 'orden': 1},
    {'codigo': 'SFA', 'descripcion': 'Sufrimiento Fetal Agudo', 'orden': 2},
    {'codigo': 'PRES_NO_CEFALICA', 'descripcion': 'Presentación No Cefálica', 'orden': 3},
    {'codigo': 'RUPTURA_UTERINA', 'descripcion': 'Ruptura Uterina', 'orden': 4},
    {'codigo': 'DESPRENDIMIENTO', 'descripcion': 'Desprendimiento Prematuro de Placenta', 'orden': 5},
    {'codigo': 'PREECLAMPSIA', 'descripcion': 'Preeclampsia/Eclampsia', 'orden': 6},
    {'codigo': 'PLACENTA_PREVIA', 'descripcion': 'Placenta Previa', 'orden': 7},
    {'codigo': 'PROCORDIALISMO', 'descripcion': 'Procordialismo', 'orden': 8},
    {'codigo': 'TRABAJO_PARTO_PROLONGADO', 'descripcion': 'Trabajo de Parto Prolongado', 'orden': 9},
    {'codigo': 'ITERATIVIDAD', 'descripcion': 'Iteratividad (Cesárea Previa)', 'orden': 10},
    {'codigo': 'MATERNIDAD_SEGURA', 'descripcion': 'Maternidad Segura', 'orden': 11},
    {'codigo': 'OTRA', 'descripcion': 'Otra Causa', 'orden': 12},
]

for causa in causas_cesarea:
    obj, created = CatalogoCausaCesarea.objects.get_or_create(
        codigo=causa['codigo'],
        defaults={
            'descripcion': causa['descripcion'],
            'orden': causa['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Causa Cesárea: {causa['descripcion']}")

# Motivo Parto No Acompañado
motivos_no_acompanado = [
    {'codigo': 'NO_DESEA', 'descripcion': 'Paciente No Desea', 'orden': 1},
    {'codigo': 'NO_LLEGA', 'descripcion': 'Acompañante No Llega a Tiempo', 'orden': 2},
    {'codigo': 'URGENCIA', 'descripcion': 'Urgencia Obstétrica', 'orden': 3},
    {'codigo': 'SIN_ACOMPANANTE', 'descripcion': 'No Tiene Acompañante', 'orden': 4},
    {'codigo': 'RURALIDAD', 'descripcion': 'Dificultad de Ruralidad', 'orden': 5},
    {'codigo': 'SIN_PASE_MOVILIDAD', 'descripcion': 'Sin Pase de Movilidad', 'orden': 6},
]

for mot in motivos_no_acompanado:
    obj, created = CatalogoMotivoPartoNoAcompanado.objects.get_or_create(
        codigo=mot['codigo'],
        defaults={
            'descripcion': mot['descripcion'],
            'orden': mot['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Motivo No Acompañado: {mot['descripcion']}")

# Persona Acompañante
personas_acompanante = [
    {'codigo': 'PAREJA', 'descripcion': 'Pareja', 'orden': 1},
    {'codigo': 'MADRE', 'descripcion': 'Madre', 'orden': 2},
    {'codigo': 'PADRE', 'descripcion': 'Padre', 'orden': 3},
    {'codigo': 'HERMANA', 'descripcion': 'Hermana', 'orden': 4},
    {'codigo': 'AMIGA', 'descripcion': 'Amiga', 'orden': 5},
    {'codigo': 'OTRO', 'descripcion': 'Otro', 'orden': 6},
    {'codigo': 'NADIE', 'descripcion': 'Ninguno', 'orden': 7},
]

for per in personas_acompanante:
    obj, created = CatalogoPersonaAcompanante.objects.get_or_create(
        codigo=per['codigo'],
        defaults={
            'descripcion': per['descripcion'],
            'orden': per['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Persona Acompañante: {per['descripcion']}")

# Métodos No Farmacológicos
metodos_nofarm = [
    {'codigo': 'BALON', 'descripcion': 'Balón Kinésico', 'orden': 1},
    {'codigo': 'LENTEJA', 'descripcion': 'Lenteja de Parto', 'orden': 2},
    {'codigo': 'REBOZO', 'descripcion': 'Rebozo', 'orden': 3},
    {'codigo': 'AROMATERAPIA', 'descripcion': 'Aromaterapia', 'orden': 4},
    {'codigo': 'MASAJE', 'descripcion': 'Masaje Terapéutico', 'orden': 5},
    {'codigo': 'DUCHA', 'descripcion': 'Ducha/Baño de Agua Caliente', 'orden': 6},
    {'codigo': 'RESPIRACION', 'descripcion': 'Técnicas de Respiración', 'orden': 7},
    {'codigo': 'DEAMBULACION', 'descripcion': 'Deambulación', 'orden': 8},
    {'codigo': 'POSICIONES', 'descripcion': 'Cambio de Posiciones', 'orden': 9},
]

for met in metodos_nofarm:
    obj, created = CatalogoMetodoNoFarmacologico.objects.get_or_create(
        codigo=met['codigo'],
        defaults={
            'descripcion': met['descripcion'],
            'orden': met['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Método No Farmacológico: {met['descripcion']}")

# ============================================
# RECIENNACIDOAPP
# ============================================

print("\n📋 recienNacidoApp Catálogos...")

# Sexo RN
sexos_rn = [
    {'codigo': 'M', 'descripcion': 'Masculino', 'orden': 1},
    {'codigo': 'F', 'descripcion': 'Femenino', 'orden': 2},
]

for sex in sexos_rn:
    obj, created = CatalogoSexoRN.objects.get_or_create(
        codigo=sex['codigo'],
        defaults={
            'descripcion': sex['descripcion'],
            'orden': sex['orden'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Sexo RN: {sex['descripcion']}")

print("\n" + "=" * 80)
print("✅ CARGA DE CATÁLOGOS COMPLETADA")
print("=" * 80)
print("\nTotal de catálogos cargados:")
print("  • Vías de Administración: 6")
print("  • Consultorios: 5")
print("  • Tipos de Paciente: 3")
print("  • Orígenes de Ingreso: 4")
print("  • Órdenes VIH: 3")
print("  • Resultados SGB: 3")
print("  • Resultados VDRL: 3")
print("  • Tipos Rotura Membranas: 4")
print("  • Regímenes Trabajo Parto: 4")
print("  • Tipos de Parto: 4")
print("  • Clasificación Robson: 10")
print("  • Posiciones Parto: 9")
print("  • Estados Periné: 9")
print("  • Causas Cesárea: 12")
print("  • Motivos No Acompañado: 6")
print("  • Personas Acompañante: 7")
print("  • Métodos No Farmacológicos: 9")
print("  • Sexos RN: 2")
print("\n  TOTAL: ~107 catálogos")
print("\n🚀 Sistema listo para usar")
print("=" * 80)
