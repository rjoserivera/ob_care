"""
populate_full_system.py
Script COMPLETO para poblar TODOS los catálogos del sistema
Versión: 3.0 - Diciembre 2025
Región de Ñuble, Chile

# 1. Guardar el artifact como populate_full_system.py
# 2. Ejecutar:
python populate_full_system.py

# O desde manage.py:
python manage.py shell < populate_full_system.py

"""

import os
import django
import sys
from datetime import datetime

# Configurar entorno Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "obstetric_care.settings")
django.setup()

from django.db import transaction
from django.contrib.auth.models import Group

# ============================================
# IMPORTACIONES DE MODELOS
# ============================================

# PARTOS APP
from partosApp.models import (
    CatalogoTipoParto, 
    CatalogoClasificacionRobson, 
    CatalogoPosicionParto,
    CatalogoEstadoPerine, 
    CatalogoCausaCesarea, 
    CatalogoMotivoPartoNoAcompanado,
    CatalogoPersonaAcompanante, 
    CatalogoMetodoNoFarmacologico, 
    CatalogoTipoEsterilizacion
)

# CATÁLOGOS NUEVOS PARTOS
from partosApp.catalogos_nuevos import (
    CatalogoRegimenParto,
    CatalogoTipoRoturaMembrana
)

# RECIÉN NACIDO APP
from recienNacidoApp.models import (
    CatalogoSexoRN, 
    CatalogoComplicacionesRN, 
    CatalogoMotivoHospitalizacionRN
)

# MATRONA APP
from matronaApp.models import (
    CatalogoViaAdministracion, 
    CatalogoConsultorioOrigen, 
    CatalogoMedicamento,
    CatalogoTipoPaciente,
    CatalogoDiscapacidad,
    CatalogoARO
)

# GESTIÓN APP
from gestionApp.models import (
    CatalogoSexo, 
    CatalogoNacionalidad, 
    CatalogoPuebloOriginario, 
    CatalogoEstadoCivil, 
    CatalogoPrevision, 
    CatalogoTurno
)

# INGRESO PARTO APP
from ingresoPartoApp.models import (
    CatalogoEstadoCervical, 
    CatalogoEstadoFetal, 
    CatalogoPosicionFetal,
    CatalogoAlturaPresentacion, 
    CatalogoCaracteristicasLiquido, 
    CatalogoResultadoCTG, 
    CatalogoSalaAsignada,
    CatalogoResultadoExamen,
    CatalogoDerivacion
)

# GESTIÓN PROCESOS APP
from gestionProcesosApp.models import GeneradorCodigo, Sala

# MÉDICO APP (Si existe el modelo)
try:
    from medicoApp.models import Patologias
    MEDICO_APP_AVAILABLE = True
except ImportError:
    MEDICO_APP_AVAILABLE = False
    print("⚠️ medicoApp.models.Patologias no disponible")


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def print_header(title):
    """Imprime un encabezado formateado"""
    print(f"\n{'='*70}")
    print(f" {title}")
    print(f"{'='*70}")


def print_success(msg):
    """Imprime mensaje de éxito"""
    print(f"  ✅ {msg}")


def print_info(msg):
    """Imprime mensaje informativo"""
    print(f"  ℹ️  {msg}")


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def populate_all():
    """Puebla TODOS los catálogos del sistema"""
    
    print("🚀 INICIANDO POBLACIÓN COMPLETA DEL SISTEMA...")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📍 Región de Ñuble, Chile")

    with transaction.atomic():
        
        # ══════════════════════════════════════════════════════════════
        # 1. GESTIÓN APP (DEMOGRÁFICOS Y ADMINISTRATIVOS)
        # ══════════════════════════════════════════════════════════════
        print_header("1. DATOS DEMOGRÁFICOS Y GESTIÓN")

        # 1.1 Sexo (Adultos)
        sexos = [
            ('F', 'Femenino', 1),
            ('M', 'Masculino', 2),
            ('T', 'Trans Masculino', 3)
        ]
        for cod, nom, orden in sexos:
            CatalogoSexo.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Sexos (Adultos)")

        # 1.2 Nacionalidades (Chile y principales migrantes)
        nacionalidades = [
            ('CL', 'Chilena', 1),
            ('VE', 'Venezolana', 2),
            ('HT', 'Haitiana', 3),
            ('PE', 'Peruana', 4),
            ('CO', 'Colombiana', 5),
            ('BO', 'Boliviana', 6),
            ('AR', 'Argentina', 7),
            ('EC', 'Ecuatoriana', 8),
            ('BR', 'Brasileña', 9),
            ('DO', 'Dominicana', 10),
            ('CU', 'Cubana', 11),
            ('OTRA', 'Otra', 99)
        ]
        for cod, nom, orden in nacionalidades:
            CatalogoNacionalidad.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Nacionalidades")

        # 1.3 Pueblos Originarios (Chile)
        pueblos = [
            ('NINGUNO', 'Ninguno', 1),
            ('MAPUCHE', 'Mapuche', 2),
            ('AYMARA', 'Aymara', 3),
            ('RAPANUI', 'Rapa Nui', 4),
            ('DIAGUITA', 'Diaguita', 5),
            ('QUECHUA', 'Quechua', 6),
            ('COLLA', 'Colla', 7),
            ('OTRO', 'Otro', 99)
        ]
        for cod, nom, orden in pueblos:
            CatalogoPuebloOriginario.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Pueblos Originarios")

        # 1.4 Estado Civil
        estados_civil = [
            ('SOLTERA', 'Soltera', 1),
            ('CASADA', 'Casada', 2),
            ('VIUDA', 'Viuda', 3),
            ('DIVORCIADA', 'Divorciada', 4),
            ('UNION', 'Unión Civil', 5),
            ('SEPARADA', 'Separada', 6)
        ]
        for cod, nom, orden in estados_civil:
            CatalogoEstadoCivil.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Estados Civiles")

        # 1.5 Previsión
        previsiones = [
            ('FONASA_A', 'FONASA A', 1),
            ('FONASA_B', 'FONASA B', 2),
            ('FONASA_C', 'FONASA C', 3),
            ('FONASA_D', 'FONASA D', 4),
            ('ISAPRE', 'ISAPRE', 5),
            ('PARTICULAR', 'PARTICULAR', 6),
            ('OTRA', 'OTRA', 99)
        ]
        for cod, nom, orden in previsiones:
            CatalogoPrevision.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Previsiones de Salud")

        # 1.6 Turnos
        turnos = [
            ('24HRS', 'Turno 24 Horas', '08:00', '08:00', 1),
            ('DIURNO', 'Diurno', '08:00', '17:00', 2),
            ('NOCHE', 'Noche', '20:00', '08:00', 3),
            ('LARGO', 'Largo', '08:00', '20:00', 4)
        ]
        for cod, nom, ini, fin, orden in turnos:
            CatalogoTurno.objects.get_or_create(
                codigo=cod, 
                defaults={
                    'nombre': nom, 
                    'hora_inicio': ini, 
                    'hora_fin': fin, 
                    'orden': orden,
                    'activo': True
                }
            )
        print_success("Turnos")

        # ══════════════════════════════════════════════════════════════
        # 2. INGRESO PARTO APP (CLÍNICOS)
        # ══════════════════════════════════════════════════════════════
        print_header("2. DATOS CLÍNICOS DE INGRESO")

        # 2.1 Estado Cervical
        estados_cerv = [
            ('CERRADO', 'Cerrado', 1),
            ('PERMEABLE', 'Permeable', 2),
            ('BORRADO_25', 'Borrado 25%', 3),
            ('BORRADO_50', 'Borrado 50%', 4),
            ('BORRADO_75', 'Borrado 75%', 5),
            ('BORRADO_100', 'Completamente borrado', 6),
            ('EDEMATOSO', 'Edematoso', 7),
            ('RIGIDO', 'Rígido', 8)
        ]
        for cod, nom, orden in estados_cerv:
            CatalogoEstadoCervical.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Estados Cervicales")

        # 2.2 Estado Fetal
        estados_fetal = [
            ('TRANQUILO', 'Tranquilo', 1),
            ('ACTIVO', 'Activo / Movimientos normales', 2),
            ('HIPERACTIVO', 'Hiperactivo', 3),
            ('DISMINUIDO', 'Movimientos disminuidos', 4),
            ('AUSENTE', 'Sin movimientos percibidos', 5)
        ]
        for cod, nom, orden in estados_fetal:
            CatalogoEstadoFetal.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Estados Fetales")

        # 2.3 Posición Fetal
        posiciones_fetal = [
            ('CEFALICA', 'Cefálica', 1),
            ('PODALICA', 'Podálica', 2),
            ('TRANSVERSA', 'Transversa', 3),
            ('OBLICUA', 'Oblicua', 4)
        ]
        for cod, nom, orden in posiciones_fetal:
            CatalogoPosicionFetal.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Posiciones Fetales")

        # 2.4 Altura Presentación
        alturas = [
            ('LIBRE', 'Libre / Flotante', '', 1),
            ('ABOCADA', 'Abocada', '', 2),
            ('ENCAJADA', 'Encajada', '0', 3),
            ('HODGE_I', 'I Plano Hodge', '-4', 4),
            ('HODGE_II', 'II Plano Hodge', '-2', 5),
            ('HODGE_III', 'III Plano Hodge', '0', 6),
            ('HODGE_IV', 'IV Plano Hodge', '+4', 7)
        ]
        for cod, nom, val, orden in alturas:
            CatalogoAlturaPresentacion.objects.get_or_create(
                codigo=cod, 
                defaults={
                    'nombre': nom, 
                    'valor_numerico': val, 
                    'orden': orden,
                    'activo': True
                }
            )
        print_success("Alturas de Presentación")

        # 2.5 Características Líquido
        liquidos = [
            ('CLARO', 'Claro / Transparente', False, 1),
            ('GRUMO', 'Con Grumos', False, 2),
            ('MECONIO_FLUIDO', 'Meconio Fluido', True, 3),
            ('MECONIO_ESPESO', 'Meconio Espeso ("Puré de arvejas")', True, 4),
            ('SANGUINOLENTO', 'Sanguinolento', True, 5),
            ('FETIDO', 'Fétido / Mal olor', True, 6)
        ]
        for cod, nom, pat, orden in liquidos:
            CatalogoCaracteristicasLiquido.objects.get_or_create(
                codigo=cod, 
                defaults={
                    'nombre': nom, 
                    'es_patologico': pat, 
                    'orden': orden,
                    'activo': True
                }
            )
        print_success("Características Líquido Amniótico")

        # 2.6 Resultado CTG
        ctgs = [
            ('CAT_I', 'Categoría I (Normal)', False, 1),
            ('CAT_II', 'Categoría II (Indeterminado)', True, 2),
            ('CAT_III', 'Categoría III (Anormal)', True, 3),
            ('SIN_REGISTRO', 'Sin Registro', False, 4)
        ]
        for cod, nom, acc, orden in ctgs:
            CatalogoResultadoCTG.objects.get_or_create(
                codigo=cod, 
                defaults={
                    'nombre': nom, 
                    'requiere_accion': acc, 
                    'orden': orden,
                    'activo': True
                }
            )
        print_success("Resultados CTG")

        # 2.7 Resultado Exámenes (VIH, SGB, VDRL, Hepatitis B) ✅ NUEVO
        resultados_exam = [
            ('POSITIVO', 'Positivo', 1),
            ('NEGATIVO', 'Negativo', 2),
            ('PENDIENTE', 'Pendiente', 3),
            ('INDETERMINADO', 'Indeterminado', 4),
            ('NO_REALIZADO', 'No Realizado', 5)
        ]
        for cod, nom, orden in resultados_exam:
            CatalogoResultadoExamen.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Resultados de Exámenes")

        # 2.8 Derivación (Ingreso Parto)
        derivaciones = [
            ('HOSP_BASE', 'Hospital Base'),
            ('DOMICILIO', 'Domicilio'),
            ('APS', 'Atención Primaria (APS)'),
            ('EXTRA', 'Extra Sistema'),
            ('OTRO', 'Otro')
        ]
        for cod, nom in derivaciones:
            # Check if model has codigo (it does in ingresoPartoApp)
            CatalogoDerivacion.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'activo': True}
            )
        print_success("Lugares de Derivación")

        # ══════════════════════════════════════════════════════════════
        # 3. INFRAESTRUCTURA
        # ══════════════════════════════════════════════════════════════
        print_header("3. INFRAESTRUCTURA Y SALAS")

        # 3.1 Salas Asignadas (Catálogo para Ingreso Parto)
        salas_catalogo = [
            ('UTPR_1', 'Sala UTPR 1', 'Parto', 1),
            ('UTPR_2', 'Sala UTPR 2', 'Parto', 1),
            ('UTPR_3', 'Sala UTPR 3', 'Parto', 1),
            ('PREPARTO', 'Sala Preparto', 'Preparto', 2),
            ('PABELLON', 'Pabellón Obstétrico', 'Quirófano', 1),
            ('RECUPERACION', 'Recuperación', 'Recuperación', 1)
        ]
        for cod, nom, tipo, cap in salas_catalogo:
            CatalogoSalaAsignada.objects.get_or_create(
                codigo=cod,
                defaults={
                    'nombre': nom, 
                    'tipo': tipo, 
                    'capacidad': cap,
                    'activo': True
                }
            )
        print_success("Salas Asignadas (Catálogo)")

        # 3.2 Salas Físicas (Gestión Procesos - Camas Reales)
        salas_fisicas = [
            ('SALA_PARTO_1', 'Sala de Parto 1', 1),
            ('SALA_PARTO_2', 'Sala de Parto 2', 1),
            ('SALA_PARTO_3', 'Sala de Parto 3', 1),
            ('BOX_URGENCIA', 'Box Urgencia', 2)
        ]
        for cod, nom, cap in salas_fisicas:
            Sala.objects.get_or_create(
                codigo=cod,
                defaults={
                    'nombre': nom, 
                    'capacidad_maxima': cap, 
                    'estado': 'DISPONIBLE'
                }
            )
        print_success("Salas Físicas (Camas)")

        # ══════════════════════════════════════════════════════════════
        # 4. CONFIGURACIÓN DEL SISTEMA
        # ══════════════════════════════════════════════════════════════
        print_header("4. CONFIGURACIÓN DEL SISTEMA")

        # Generadores de Código
        generadores = [
            ('FO', 'FO', 0, 6, 'Ficha Obstétrica'),
            ('FP', 'FP', 0, 6, 'Ficha Parto'),
            ('RN', 'RN', 0, 6, 'Registro Recién Nacido'),
            ('IP', 'IP', 0, 6, 'Ingreso Paciente'),
            ('PARTO', 'PARTO', 0, 6, 'Registro Parto')
        ]
        for tipo, pref, ini, digs, desc in generadores:
            if not GeneradorCodigo.objects.filter(tipo=tipo).exists():
                GeneradorCodigo.objects.create(
                    tipo=tipo, 
                    prefijo=pref, 
                    ultimo_numero=ini, 
                    digitos_minimos=digs
                )
                print_success(f"Generador {tipo} creado")
            else:
                print_info(f"Generador {tipo} ya existe")

        # ══════════════════════════════════════════════════════════════
        # 5. MATRONA APP (GESTIÓN MÉDICA)
        # ══════════════════════════════════════════════════════════════
        print_header("5. GESTIÓN MÉDICA (MATRONA)")

        # 5.1 Vías Administración
        vias = [
            ('VO', 'Vía Oral', 1),
            ('IV', 'Endovenosa', 2),
            ('IM', 'Intramuscular', 3),
            ('SC', 'Subcutánea', 4),
            ('VAG', 'Vaginal', 5),
            ('REC', 'Rectal', 6),
            ('TOP', 'Tópica', 7),
            ('INHAL', 'Inhalatoria', 8),
            ('PERID', 'Peridural / Epidural', 9)
        ]
        for cod, nom, orden in vias:
            CatalogoViaAdministracion.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Vías de Administración")

        # 5.2 Consultorios (Región de Ñuble)
        consultorios = [
            ('CESFAM_CHILLAN', 'CESFAM Chillán', 1),
            ('CESFAM_VIOLETA', 'CESFAM Violeta Parra', 2),
            ('CESFAM_ISABEL', 'CESFAM Isabel Riquelme', 3),
            ('CESFAM_BULNES', 'CESFAM Bulnes', 4),
            ('CESFAM_QUILLAN', 'CESFAM Quillón', 5),
            ('CESFAM_COBQUECURA', 'CESFAM Cobquecura', 6),
            ('CESFAM_QUIRIHUE', 'CESFAM Quirihue', 7),
            ('CESFAM_COIHUECO', 'CESFAM Coihueco', 8),
            ('HOSPITAL_HHM', 'Hospital Herminda Martín', 9),
            ('OTRO', 'Otro', 99)
        ]
        for cod, nom, orden in consultorios:
            CatalogoConsultorioOrigen.objects.get_or_create(
                codigo=cod, 
                defaults={'nombre': nom, 'orden': orden, 'activo': True}
            )
        print_success("Consultorios de Origen (Región Ñuble)")
        
        # 5.3 Medicamentos (Catálogo Básico Obstétrico)
        medicamentos = [
            # Analgésicos
            ('PARACETAMOL_500', 'Paracetamol', '500mg', 'Comprimido'),
            ('PARACETAMOL_1G', 'Paracetamol', '1g', 'Frasco'),
            ('IBUPROFENO_400', 'Ibuprofeno', '400mg', 'Comprimido'),
            ('IBUPROFENO_600', 'Ibuprofeno', '600mg', 'Comprimido'),
            ('KETOROLACO_30', 'Ketorolaco', '30mg', 'Ampolla'),
            ('TRAMADOL_100', 'Tramadol', '100mg', 'Ampolla'),
            # Uterotónicos
            ('OXITOCINA_5', 'Oxitocina', '5 UI', 'Ampolla'),
            ('OXITOCINA_10', 'Oxitocina', '10 UI', 'Ampolla'),
            ('MISOPROSTOL_200', 'Misoprostol', '200 mcg', 'Comprimido'),
            ('CARBETOCINA_100', 'Carbetocina', '100 mcg', 'Ampolla'),
            # Antibióticos
            ('AMPICILINA_500', 'Ampicilina', '500mg', 'Frasco'),
            ('CEFAZOLINA_1G', 'Cefazolina', '1g', 'Frasco'),
            ('CLINDAMICINA_600', 'Clindamicina', '600mg', 'Ampolla'),
            # Otros
            ('METOCLOPRAMIDA_10', 'Metoclopramida', '10mg', 'Ampolla'),
            ('RANITIDINA_50', 'Ranitidina', '50mg', 'Ampolla'),
            ('DICLOFENACO_75', 'Diclofenaco', '75mg', 'Ampolla')
        ]
        for cod, nom, conc, pres in medicamentos:
            CatalogoMedicamento.objects.get_or_create(
                codigo=cod,
                defaults={
                    'nombre': nom, 
                    'concentracion': conc, 
                    'presentacion': pres,
                    'activo': True
                }
            )
        print_success("Medicamentos Básicos (16 medicamentos)")

        # 5.4 Tipos de Paciente (Matrona App)
        tipos_paciente = ['Obstétrica', 'Ginecológica', 'Oncológica', 'Otras']
        for nom in tipos_paciente:
            CatalogoTipoPaciente.objects.get_or_create(
                nombre=nom, 
                defaults={'activo': True}
            )
        print_success("Tipos de Paciente")

        # 5.5 Discapacidades (Matrona App)
        discapacidades = ['Física', 'Auditiva', 'Visual', 'Intelectual', 'Psíquica', 'Visceral', 'Ninguna']
        for nom in discapacidades:
            CatalogoDiscapacidad.objects.get_or_create(
                nombre=nom, 
                defaults={'activo': True}
            )
        print_success("Tipos de Discapacidad")

        # 5.6 Clasificación ARO (Matrona App)
        aros = ['Bajo Riesgo', 'Alto Riesgo Obstétrico (ARO)', 'Alto Riesgo I', 'Alto Riesgo II']
        for nom in aros:
            CatalogoARO.objects.get_or_create(
                nombre=nom, 
                defaults={'activo': True}
            )
        print_success("Clasificación ARO")

        # 5.7 Patologías CIE-10 (Si el modelo existe)
        if MEDICO_APP_AVAILABLE:
            patologias = [
                ('O14', 'Preeclampsia', 'Hipertensión inducida por embarazo', 'Alto'),
                ('O15', 'Eclampsia', 'Convulsiones en embarazo', 'Alto'),
                ('O24', 'Diabetes Gestacional', 'Diabetes mellitus en el embarazo', 'Medio'),
                ('O99', 'Anemia', 'Anemia en el embarazo', 'Bajo'),
                ('O20', 'Hemorragia precoz', 'Hemorragia inicio embarazo', 'Alto'),
                ('O10', 'HTA Crónica', 'Hipertensión preexistente', 'Medio'),
                ('O42', 'RPM', 'Ruptura prematura de membranas', 'Medio'),
                ('O60', 'Parto Prematuro', 'Amenaza de parto prematuro', 'Alto'),
                ('O41', 'Polihidroamnios', 'Exceso de líquido amniótico', 'Medio'),
                ('O36', 'RCIU', 'Restricción crecimiento intrauterino', 'Alto')
            ]
            for cod, nom, desc, riesgo in patologias:
                Patologias.objects.get_or_create(
                    codigo_cie_10=cod,
                    defaults={
                        'nombre': nom,
                        'descripcion': desc, 
                        'nivel_de_riesgo': riesgo, 
                        'estado': 'Activo'
                    }
                )
            print_success("Patologías CIE-10 (10 patologías)")
        else:
            print_info("Patologías CIE-10 omitidas (modelo no disponible)")

        # ══════════════════════════════════════════════════════════════
        # 6. PARTOS APP (CATÁLOGOS COMPLETOS)
        # ══════════════════════════════════════════════════════════════
        print_header("6. CATÁLOGOS DE PARTOS")
        
        # 6.1 Tipo Esterilización
        tipos_est = [
            ('LIGADURA', 'Ligadura Tubaria'),
            ('VASECTOMIA', 'Vasectomía'),
            ('SALPINGECTOMIA', 'Salpingectomía'),
            ('ESSURE', 'Essure'),
            ('OTRO', 'Otro')
        ]
        for cod, desc in tipos_est:
            CatalogoTipoEsterilizacion.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Tipos de Esterilización (5)")

        # 6.2 Tipo Parto
        tipos_parto = [
            ('EUTOCICO', 'Vaginal Eutócico'),
            ('DISTOCICO', 'Vaginal Distócico'),
            ('CESAREA', 'Cesárea'),
            ('FORCEPS', 'Fórceps'),
            ('VENTOSA', 'Ventosa Obstétrica')
        ]
        for cod, desc in tipos_parto:
            CatalogoTipoParto.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Tipos de Parto (5)")

        # 6.3 Clasificación de Robson (COMPLETO - 10 grupos)
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
                defaults={
                    'numero_grupo': num, 
                    'descripcion': desc,
                    'activo': True
                }
            )
        print_success("Clasificación de Robson (10 grupos)")

        # 6.4 Posiciones de Parto
        pos_parto = [
            ('LITOTOMIA', 'Litotomía'),
            ('SENTADA', 'Sentada'),
            ('DE_PIE', 'De pie'),
            ('CUCLILLAS', 'Cuclillas'),
            ('LATERAL', 'Decúbito Lateral'),
            ('CUATRO_APOYOS', 'Cuatro Apoyos'),
            ('VERTICAL', 'Vertical'),
            ('SEMI_SENTADA', 'Semi-sentada')
        ]
        for cod, desc in pos_parto:
            CatalogoPosicionParto.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Posiciones de Parto (8)")

        # 6.5 Estado Periné
        perines = [
            ('INTACTO', 'Intacto'),
            ('DESGARRO_I', 'Desgarro Grado I'),
            ('DESGARRO_II', 'Desgarro Grado II'),
            ('DESGARRO_III', 'Desgarro Grado III'),
            ('DESGARRO_IV', 'Desgarro Grado IV'),
            ('EPISIOTOMIA', 'Episiotomía'),
            ('EPIS_DESGARRO', 'Episiotomía + Desgarro')
        ]
        for cod, desc in perines:
            CatalogoEstadoPerine.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Estados de Periné (7)")
            
        # 6.6 Causas de Cesárea
        causas = [
            ('SFA', 'Sufrimiento Fetal Agudo'),
            ('DCP', 'Desproporción Cefalo-Pélvica'),
            ('PODALICA', 'Presentación Podálica'),
            ('ANTERIOR', 'Cesárea Anterior'),
            ('ESTACIONARIA', 'Dilatación Estacionaria'),
            ('PROLAPSO', 'Prolapso de Cordón'),
            ('PLACENTA_PREVIA', 'Placenta Previa'),
            ('DPPNI', 'DPPNI (Desprendimiento Placenta)'),
            ('MACROSOMIA', 'Macrosomía Fetal'),
            ('OTRA', 'Otra')
        ]
        for cod, desc in causas:
            CatalogoCausaCesarea.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Causas de Cesárea (10)")

        # 6.7 Motivo Parto No Acompañado
        motivos_no_acomp = [
            ('ELECCION', 'Elección Materna'),
            ('NO_TIENE', 'No tiene acompañante'),
            ('AFORO', 'Restricción de aforo'),
            ('URGENCIA', 'Urgencia Médica'),
            ('COVID', 'Protocolo COVID-19'),
            ('OTRO', 'Otro')
        ]
        for cod, desc in motivos_no_acomp:
            CatalogoMotivoPartoNoAcompanado.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Motivos Parto No Acompañado (6)")

        # 6.8 Persona Acompañante
        acomp = [
            ('PAREJA', 'Pareja'),
            ('MADRE', 'Madre'),
            ('PADRE', 'Padre'),
            ('HERMANA', 'Hermana'),
            ('HERMANO', 'Hermano'),
            ('DOULA', 'Doula'),
            ('AMIGA', 'Amiga'),
            ('OTRO', 'Otro Familiar/Amigo')
        ]
        for cod, desc in acomp:
            CatalogoPersonaAcompanante.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Personas Acompañantes (8)")

        # 6.9 Métodos No Farmacológicos
        metodos = [
            ('BALON', 'Balón Kinésico'),
            ('MASAJE', 'Masaje'),
            ('DUCHA', 'Ducha/Agua Caliente'),
            ('GUATERO', 'Guatero Semillas'),
            ('AROMA', 'Aromaterapia'),
            ('MOVIMIENTO', 'Movimiento Libre'),
            ('MUSICA', 'Musicoterapia'),
            ('RESPIRACION', 'Técnicas de Respiración'),
            ('TENS', 'TENS (Electroestimulación)')
        ]
        for cod, desc in metodos:
            CatalogoMetodoNoFarmacologico.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Métodos No Farmacológicos (9)")

        # 6.10 Régimen de Parto ✅ NUEVO
        regimenes = [
            ('CERO', 'Régimen Cero (NPO)'),
            ('LIQUIDO', 'Régimen Líquido'),
            ('COMUN', 'Régimen Común'),
            ('OTRO', 'Otro')
        ]
        for cod, desc in regimenes:
            CatalogoRegimenParto.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Regímenes de Parto (4) ✅ NUEVO")

        # 6.11 Tipo Rotura Membrana ✅ NUEVO
        roturas = [
            ('IOP', 'Íntegra en el Parto (IOP)'),
            ('RAM', 'Rotura Artificial de Membranas (RAM)'),
            ('REM', 'Rotura Espontánea de Membranas (REM)'),
            ('RPM', 'Rotura Prematura de Membranas (RPM)')
        ]
        for cod, desc in roturas:
            CatalogoTipoRoturaMembrana.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Tipos de Rotura de Membrana (4) ✅ NUEVO")

        # ══════════════════════════════════════════════════════════════
        # 7. RECIÉN NACIDO APP (CATÁLOGOS COMPLETOS)
        # ══════════════════════════════════════════════════════════════
        print_header("7. CATÁLOGOS DE RECIÉN NACIDO")

        # 7.1 Sexo RN
        sexos_rn = [
            ('M', 'Masculino'),
            ('F', 'Femenino'),
            ('I', 'Indeterminado')
        ]
        for cod, desc in sexos_rn:
            CatalogoSexoRN.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Sexo RN (3)")

        # 7.2 Complicaciones RN
        comps_rn = [
            ('TRAUMA', 'Traumatismo Obstétrico'),
            ('DIFF_RESP', 'Dificultad Respiratoria'),
            ('HIPOGLUCEMIA', 'Hipoglucemia'),
            ('HIPOTERMIA', 'Hipotermia'),
            ('ICTERICIA', 'Ictericia'),
            ('SEPSIS', 'Sepsis Neonatal'),
            ('MECONIO', 'Aspiración Meconio'),
            ('APNEA', 'Apnea'),
            ('OTRO', 'Otra')
        ]
        for cod, desc in comps_rn:
            CatalogoComplicacionesRN.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Complicaciones RN (9)")

        # 7.3 Motivos Hospitalización RN
        motivos_hosp_rn = [
            ('PREMATUREZ', 'Prematurez'),
            ('SDR', 'Síndrome de Dificultad Respiratoria'),
            ('ASFIXIA', 'Asfixia Perinatal'),
            ('MALFORMACION', 'Malformación Congénita'),
            ('ICTERICIA', 'Ictericia Patológica'),
            ('OBSERVACION', 'Observación'),
            ('SEPSIS', 'Sepsis / Infección'),
            ('BAJO_PESO', 'Bajo Peso al Nacer'),
            ('HIPOGLUCEMIA', 'Hipoglucemia'),
            ('OTRO', 'Otro')
        ]
        for cod, desc in motivos_hosp_rn:
            CatalogoMotivoHospitalizacionRN.objects.get_or_create(
                codigo=cod, 
                defaults={'descripcion': desc, 'activo': True}
            )
        print_success("Motivos Hospitalización RN (10)")

        # ══════════════════════════════════════════════════════════════
        # 8. GRUPOS DE USUARIO
        # ══════════════════════════════════════════════════════════════
        print_header("8. GRUPOS DE USUARIO")

        grupos = ['Administrator', 'Medico', 'Matrona', 'TENS']
        for nombre_grupo in grupos:
            Group.objects.get_or_create(name=nombre_grupo)
            print_success(f"Grupo '{nombre_grupo}'")

# ============================================
# EJECUTAR
# ============================================

if __name__ == '__main__':
    try:
        populate_all()
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
