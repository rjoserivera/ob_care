"""
cargar_catalogos_corregido.py
Script CORREGIDO con nombres de campos válidos
Ejecutar con: python manage.py shell < cargar_catalogos_corregido.py
"""

from gestionApp.models import (
    CatalogoSexo, CatalogoEstadoCivil, CatalogoPrevision, 
    CatalogoTurno, CatalogoEspecialidad, CatalogoNivelTens,
    CatalogoNacionalidad, CatalogoPuebloOriginario, CatalogoCertificacion
)

from matronaApp.models import (
    CatalogoConsultorioOrigen, CatalogoViaAdministracion
)

from ingresoPartoApp.models import (
    CatalogoEstadoCervical, CatalogoEstadoFetal
)

from partosApp.models import (
    CatalogoTipoParto, CatalogoClasificacionRobson, CatalogoPosicionParto,
    CatalogoEstadoPerine, CatalogoCausaCesarea, CatalogoMotivoPartoNoAcompanado,
    CatalogoPersonaAcompanante, CatalogoMetodoNoFarmacologico
)

from recienNacidoApp.models import CatalogoSexoRN

print("=" * 80)
print("CARGANDO CATÁLOGOS DEL SISTEMA (VERSIÓN CORREGIDA)")
print("=" * 80)

# ============================================
# partosApp - CATÁLOGOS (CORREGIDO)
# ============================================

print("\n📋 partosApp - Catálogos...")

# Tipo de Parto (usa 'descripcion' no 'nombre')
tipos_parto = [
    {'codigo': 'VAGINAL', 'descripcion': 'Vaginal'},
    {'codigo': 'CESAREA', 'descripcion': 'Cesárea'},
    {'codigo': 'FORCEPS', 'descripcion': 'Fórceps'},
    {'codigo': 'VENTOSA', 'descripcion': 'Ventosa'},
]
for tp in tipos_parto:
    obj, created = CatalogoTipoParto.objects.get_or_create(
        codigo=tp['codigo'],
        defaults={'descripcion': tp['descripcion'], 'activo': True}
    )
    if created:
        print(f"  ✅ Tipo de Parto: {tp['descripcion']}")

# Clasificación de Robson (usa 'numero_grupo' y 'descripcion')
clasificaciones = [
    {'codigo': 'ROBSON_1', 'numero_grupo': 1, 'descripcion': 'Nulíparas, parto espontáneo'},
    {'codigo': 'ROBSON_2', 'numero_grupo': 2, 'descripcion': 'Nulíparas, parto inducido'},
    {'codigo': 'ROBSON_3', 'numero_grupo': 3, 'descripcion': 'Multíparas, parto espontáneo'},
    {'codigo': 'ROBSON_4', 'numero_grupo': 4, 'descripcion': 'Multíparas, parto inducido'},
    {'codigo': 'ROBSON_5', 'numero_grupo': 5, 'descripcion': 'Todos con cesárea anterior'},
]
for cr in clasificaciones:
    obj, created = CatalogoClasificacionRobson.objects.get_or_create(
        codigo=cr['codigo'],
        defaults={
            'numero_grupo': cr['numero_grupo'],
            'descripcion': cr['descripcion'],
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Clasificación Robson: Grupo {cr['numero_grupo']} - {cr['descripcion']}")

# Posición de Parto (usa 'descripcion')
posiciones = [
    {'codigo': 'DORSAL', 'descripcion': 'Dorsal'},
    {'codigo': 'LATERAL', 'descripcion': 'Lateral'},
    {'codigo': 'CUCLILLAS', 'descripcion': 'Cuclillas'},
    {'codigo': 'GEMELO', 'descripcion': 'Posición de Gemelo'},
    {'codigo': 'ARRODILLADO', 'descripcion': 'Arrodillado'},
    {'codigo': 'DE_PIE', 'descripcion': 'De Pie'},
]
for pos in posiciones:
    obj, created = CatalogoPosicionParto.objects.get_or_create(
        codigo=pos['codigo'],
        defaults={'descripcion': pos['descripcion'], 'activo': True}
    )
    if created:
        print(f"  ✅ Posición Parto: {pos['descripcion']}")

# Estado Periné (usa 'descripcion')
estados_perine = [
    {'codigo': 'INTEGRO', 'descripcion': 'Íntegro'},
    {'codigo': 'DESGARRO_1', 'descripcion': 'Desgarro 1er grado'},
    {'codigo': 'DESGARRO_2', 'descripcion': 'Desgarro 2do grado'},
    {'codigo': 'DESGARRO_3', 'descripcion': 'Desgarro 3er grado'},
    {'codigo': 'DESGARRO_4', 'descripcion': 'Desgarro 4to grado'},
    {'codigo': 'EPISIOTOMIA', 'descripcion': 'Episiotomía'},
]
for ep in estados_perine:
    obj, created = CatalogoEstadoPerine.objects.get_or_create(
        codigo=ep['codigo'],
        defaults={'descripcion': ep['descripcion'], 'activo': True}
    )
    if created:
        print(f"  ✅ Estado Periné: {ep['descripcion']}")

# Causa de Cesárea (usa 'descripcion')
causas_cesarea = [
    {'codigo': 'TRABAJO_PARTO_PROLONGADO', 'descripcion': 'Trabajo de parto prolongado'},
    {'codigo': 'DETENCIÓN_DILATACIÓN', 'descripcion': 'Detención de dilatación'},
    {'codigo': 'DESPROPORCIÓN_CEFALOPÉLVICA', 'descripcion': 'Desproporción cefalopélvica'},
    {'codigo': 'SUFRIMIENTO_FETAL', 'descripcion': 'Sufrimiento fetal'},
    {'codigo': 'PREECLAMPSIA', 'descripcion': 'Preeclampsia'},
    {'codigo': 'PLACENTA_PREVIA', 'descripcion': 'Placenta previa'},
    {'codigo': 'DESPRENDIMIENTO_PLACENTA', 'descripcion': 'Desprendimiento de placenta'},
    {'codigo': 'CIRCULAR_CUELLO', 'descripcion': 'Circular de cuello'},
    {'codigo': 'POSICIÓN_TRANSVERSA', 'descripcion': 'Posición transversa'},
]
for cc in causas_cesarea:
    obj, created = CatalogoCausaCesarea.objects.get_or_create(
        codigo=cc['codigo'],
        defaults={'descripcion': cc['descripcion'], 'activo': True}
    )
    if created:
        print(f"  ✅ Causa Cesárea: {cc['descripcion']}")

# Motivo Parto No Acompañado (usa 'descripcion')
motivos_no_acompanado = [
    {'codigo': 'PREMATURO', 'descripcion': 'Parto prematuro'},
    {'codigo': 'ACOMPAÑANTE_AUSENTE', 'descripcion': 'Acompañante ausente'},
    {'codigo': 'EMERGENCIA', 'descripcion': 'Emergencia'},
    {'codigo': 'DESEO_MADRE', 'descripcion': 'Deseo de la madre'},
]
for mna in motivos_no_acompanado:
    obj, created = CatalogoMotivoPartoNoAcompanado.objects.get_or_create(
        codigo=mna['codigo'],
        defaults={'descripcion': mna['descripcion'], 'activo': True}
    )
    if created:
        print(f"  ✅ Motivo No Acompañado: {mna['descripcion']}")

# Persona Acompañante (usa 'descripcion')
personas_acompanantes = [
    {'codigo': 'PAREJA', 'descripcion': 'Pareja'},
    {'codigo': 'MADRE', 'descripcion': 'Madre'},
    {'codigo': 'HERMANA', 'descripcion': 'Hermana'},
    {'codigo': 'AMIGA', 'descripcion': 'Amiga'},
    {'codigo': 'DOULA', 'descripcion': 'Doula'},
    {'codigo': 'OTRA', 'descripcion': 'Otra persona'},
]
for pa in personas_acompanantes:
    obj, created = CatalogoPersonaAcompanante.objects.get_or_create(
        codigo=pa['codigo'],
        defaults={'descripcion': pa['descripcion'], 'activo': True}
    )
    if created:
        print(f"  ✅ Persona Acompañante: {pa['descripcion']}")

# Método No Farmacológico (usa 'nombre')
metodos_no_farm = [
    {'codigo': 'DEAMBULACION', 'nombre': 'Deambulación'},
    {'codigo': 'POSICION_CAMBIANTE', 'nombre': 'Posición cambiante'},
    {'codigo': 'MASAJE', 'nombre': 'Masaje'},
    {'codigo': 'RESPIRACION', 'nombre': 'Técnicas de respiración'},
    {'codigo': 'COMPRESA_CALIENTE', 'nombre': 'Compresa caliente'},
    {'codigo': 'PISCINA_INMERSION', 'nombre': 'Piscina/Inmersión'},
    {'codigo': 'MUSICOTERAPIA', 'nombre': 'Musicoterapia'},
]
for mnf in metodos_no_farm:
    obj, created = CatalogoMetodoNoFarmacologico.objects.get_or_create(
        codigo=mnf['codigo'],
        defaults={'nombre': mnf['nombre'], 'activo': True}
    )
    if created:
        print(f"  ✅ Método No Farmacológico: {mnf['nombre']}")

# ============================================
# RESUMEN
# ============================================

print("\n" + "=" * 80)
print("✅ CATÁLOGOS DE PARTOS CARGADOS EXITOSAMENTE")
print("=" * 80)
print("\nEl sistema está listo para usar.")
