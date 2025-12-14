
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from partosApp.models import (
    CatalogoTipoParto, CatalogoClasificacionRobson, CatalogoPosicionParto,
    CatalogoEstadoPerine, CatalogoCausaCesarea, CatalogoMotivoPartoNoAcompanado,
    CatalogoPersonaAcompanante, CatalogoMetodoNoFarmacologico, CatalogoTipoEsterilizacion
)
from recienNacidoApp.models import CatalogoSexoRN, CatalogoComplicacionesRN, CatalogoMotivoHospitalizacionRN

def populate():
    print("Iniciando población de catálogos...")

    # 1. Tipo Esterilización
    tipos_est = [
        ('LIGADURA', 'Ligadura Tubaria'),
        ('VASECTOMIA', 'Vasectomía'),
        ('SALPINGECTOMIA', 'Salpingectomía'),
        ('OTRO', 'Otro')
    ]
    for cod, desc in tipos_est:
        CatalogoTipoEsterilizacion.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Tipos de Esterilización OK")

    # 2. Complicaciones RN
    comps_rn = [
        ('TRAUMA', 'Traumatismo Obstétrico'),
        ('DIFF_RESP', 'Dificultad Respiratoria'),
        ('HIPOGLUCEMIA', 'Hipoglucemia'),
        ('HIPOTERMIA', 'Hipotermia'),
        ('ICTERICIA', 'Ictericia'),
        ('SEPSIS', 'Sepsis Neonatal'),
        ('MECONIO', 'Aspiración Meconio'),
        ('OTRO', 'Otra')
    ]
    for cod, desc in comps_rn:
        CatalogoComplicacionesRN.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Complicaciones RN OK")

    # 3. Sexo RN
    sexos = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('I', 'Indeterminado')
    ]
    for cod, desc in sexos:
        CatalogoSexoRN.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Sexo RN OK")
    
    # 4. Estado Periné
    perines = [
        ('INTACTO', 'Intacto'),
        ('DESGARRO_I', 'Desgarro Grado I'),
        ('DESGARRO_II', 'Desgarro Grado II'),
        ('DESGARRO_III', 'Desgarro Grado III'),
        ('DESGARRO_IV', 'Desgarro Grado IV'),
        ('EPISIOTOMIA', 'Episiotomía')
    ]
    for cod, desc in perines:
        CatalogoEstadoPerine.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Estado Periné OK")

    # 5. Robson
    robsons = [
        ('GRUPO_1', 1, 'Nulípara, feto único, cefálico, >=37 sem, espontáneo'),
        ('GRUPO_2', 2, 'Nulípara, feto único, cefálico, >=37 sem, inducido o cesárea antes de TP'),
        ('GRUPO_3', 3, 'Multípara, sin cicatriz, feto único, cefálico, >=37 sem, espontáneo'),
        ('GRUPO_4', 4, 'Multípara, sin cicatriz, feto único, cefálico, >=37 sem, inducido o cesárea'),
        ('GRUPO_5', 5, 'Multípara, cicatriz uterina previa, feto único, cefálico, >=37 sem'),
        ('GRUPO_6', 6, 'Nulípara, podálica, único'),
        ('GRUPO_7', 7, 'Multípara, podálica, único'),
        ('GRUPO_8', 8, 'Embarazo múltiple'),
        ('GRUPO_9', 9, 'Situación transversa u oblicua'),
        ('GRUPO_10', 10, 'Feto único, cefálico, <37 semanas (Pretérmino)')
    ]
    for cod, num, desc in robsons:
        CatalogoClasificacionRobson.objects.get_or_create(
            codigo=cod, 
            defaults={'numero_grupo': num, 'descripcion': desc}
        )
    print("Robson OK")

    # 6. Motivo No Acompañado
    motivos = [
        ('ELECCION', 'Elección Materna'),
        ('NO_TIENE', 'No tiene acompañante'),
        ('AFORO', 'Restricción de aforo'),
        ('URGENCIA', 'Urgencia Médica'),
        ('OTRO', 'Otro')
    ]
    for cod, desc in motivos:
        CatalogoMotivoPartoNoAcompanado.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Motivos No Acompañado OK")

    # 7. Tipo Parto
    tipos_parto = [
        ('EUTOCICO', 'Vaginal Eutócico'),
        ('DISTOCICO', 'Vaginal Distócico'),
        ('CESAREA', 'Cesárea')
    ]
    for cod, desc in tipos_parto:
        CatalogoTipoParto.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Tipo Parto OK")

    # 8. Posición Parto
    posiciones = [
        ('LITOTOMIA', 'Litotomía'),
        ('SENTADA', 'Sentada'),
        ('DE_PIE', 'De pie'),
        ('CUCLILLAS', 'Cuclillas'),
        ('LATERAL', 'Decúbito Lateral'),
        ('CUATRO_APOYOS', 'Cuatro Apoyos')
    ]
    for cod, desc in posiciones:
        CatalogoPosicionParto.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Posición Parto OK")

    # 9. Causa Cesárea
    causas_cesarea = [
        ('SFA', 'Sufrimiento Fetal Agudo'),
        ('DCP', 'Desproporción Cefalo-Pélvica'),
        ('PODALICA', 'Presentación Podálica'),
        ('ANTERIOR', 'Cesárea Anterior'),
        ('ESTACIONARIA', 'Dilatación Estacionaria'),
        ('OTRA', 'Otra')
    ]
    for cod, desc in causas_cesarea:
        CatalogoCausaCesarea.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Causa Cesárea OK")

    # 10. Persona Acompañante
    personas = [
        ('PAREJA', 'Pareja'),
        ('MADRE', 'Madre'),
        ('HERMANA', 'Hermana'),
        ('DOULA', 'Doula'),
        ('OTRO', 'Otro Familiar/Amigo')
    ]
    for cod, desc in personas:
        CatalogoPersonaAcompanante.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Persona Acompañante OK")

    # 11. Métodos No Farmacológicos
    metodos = [
        ('BALON', 'Balón Kinésico'),
        ('MASAJE', 'Masaje'),
        ('DUCHA', 'Ducha/Agua Caliente'),
        ('GUATERO', 'Guatero Semillas'),
        ('AROMA', 'Aromaterapia'),
        ('MOVIMIENTO', 'Movimiento Libre')
    ]
    for cod, desc in metodos:
        CatalogoMetodoNoFarmacologico.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Métodos No Farmacológicos OK")

    # 12. Motivos Hospitalización RN
    motivos_hosp = [
        ('PREMATUREZ', 'Prematurez'),
        ('SDR', 'Síndrome de Dificultad Respiratoria'),
        ('ASFIXIA', 'Asfixia Perinatal'),
        ('MALFORMACION', 'Malformación Congénita'),
        ('ICTERICIA', 'Ictericia Patológica'),
        ('OBSERVACION', 'Observación'),
        ('SEPSIS', 'Sepsis / Infección'),
        ('OTRO', 'Otro')
    ]
    for cod, desc in motivos_hosp:
        CatalogoMotivoHospitalizacionRN.objects.get_or_create(codigo=cod, defaults={'descripcion': desc})
    print("Motivos Hospitalización RN OK")

    print("--- POBLACION COMPLETADA ---")

if __name__ == '__main__':
    populate()
