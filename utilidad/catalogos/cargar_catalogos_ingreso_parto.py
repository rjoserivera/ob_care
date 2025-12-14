"""
ingresoPartoApp/management/commands/cargar_catalogos_ingreso_parto.py
Comando para cargar los catálogos de ingresoPartoApp
"""

from django.core.management.base import BaseCommand
from ingresoPartoApp.models import (
    CatalogoEstadoCervical,
    CatalogoEstadoFetal,
    CatalogoPosicionFetal,
    CatalogoAlturaPresentacion,
    CatalogoCaracteristicasLiquido,
    CatalogoResultadoCTG,
    CatalogoResultadoExamen,
    CatalogoSalaAsignada,
)


class Command(BaseCommand):
    help = 'Carga los catálogos iniciales para ingresoPartoApp'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Cargando catálogos de Ingreso a Parto...\n')

        # =============================================
        # CATÁLOGO: ESTADO CERVICAL
        # =============================================
        estados_cervicales = [
            {'codigo': 'CERRADO', 'nombre': 'Cerrado', 'descripcion': 'Cuello uterino cerrado'},
            {'codigo': 'PERMEABLE', 'nombre': 'Permeable', 'descripcion': 'Cuello permeable al dedo'},
            {'codigo': 'BORRADO_25', 'nombre': 'Borrado 25%', 'descripcion': 'Borramiento del 25%'},
            {'codigo': 'BORRADO_50', 'nombre': 'Borrado 50%', 'descripcion': 'Borramiento del 50%'},
            {'codigo': 'BORRADO_75', 'nombre': 'Borrado 75%', 'descripcion': 'Borramiento del 75%'},
            {'codigo': 'BORRADO_100', 'nombre': 'Completamente borrado', 'descripcion': 'Borramiento completo'},
        ]
        
        for i, item in enumerate(estados_cervicales):
            obj, created = CatalogoEstadoCervical.objects.update_or_create(
                codigo=item['codigo'],
                defaults={'nombre': item['nombre'], 'descripcion': item['descripcion'], 'orden': i}
            )
            status = '✅ Creado' if created else '🔄 Actualizado'
            self.stdout.write(f"  {status}: Estado Cervical - {item['nombre']}")

        # =============================================
        # CATÁLOGO: ESTADO FETAL
        # =============================================
        estados_fetales = [
            {'codigo': 'VIVO', 'nombre': 'Vivo', 'descripcion': 'Feto vivo con FCF presente'},
            {'codigo': 'ESTABLE', 'nombre': 'Estable', 'descripcion': 'Feto estable, sin signos de sufrimiento'},
            {'codigo': 'SFA_LEVE', 'nombre': 'SFA Leve', 'descripcion': 'Sufrimiento fetal agudo leve'},
            {'codigo': 'SFA_MODERADO', 'nombre': 'SFA Moderado', 'descripcion': 'Sufrimiento fetal agudo moderado'},
            {'codigo': 'SFA_SEVERO', 'nombre': 'SFA Severo', 'descripcion': 'Sufrimiento fetal agudo severo'},
            {'codigo': 'OBITO', 'nombre': 'Óbito Fetal', 'descripcion': 'Muerte fetal intrauterina'},
        ]
        
        for i, item in enumerate(estados_fetales):
            obj, created = CatalogoEstadoFetal.objects.update_or_create(
                codigo=item['codigo'],
                defaults={'nombre': item['nombre'], 'descripcion': item['descripcion'], 'orden': i}
            )
            status = '✅ Creado' if created else '🔄 Actualizado'
            self.stdout.write(f"  {status}: Estado Fetal - {item['nombre']}")

        # =============================================
        # CATÁLOGO: POSICIÓN FETAL
        # =============================================
        posiciones_fetales = [
            {'codigo': 'CEFALICA', 'nombre': 'Cefálica', 'descripcion': 'Presentación cefálica'},
            {'codigo': 'CEFALICA_FLEXIONADA', 'nombre': 'Cefálica Flexionada', 'descripcion': 'Presentación cefálica bien flexionada'},
            {'codigo': 'CEFALICA_DEFLEXIONADA', 'nombre': 'Cefálica Deflexionada', 'descripcion': 'Presentación cefálica deflexionada'},
            {'codigo': 'PODALICA', 'nombre': 'Podálica', 'descripcion': 'Presentación podálica'},
            {'codigo': 'PODALICA_COMPLETA', 'nombre': 'Podálica Completa', 'descripcion': 'Presentación podálica completa'},
            {'codigo': 'PODALICA_INCOMPLETA', 'nombre': 'Podálica Incompleta', 'descripcion': 'Presentación podálica incompleta'},
            {'codigo': 'TRANSVERSA', 'nombre': 'Transversa', 'descripcion': 'Situación transversa'},
            {'codigo': 'OBLICUA', 'nombre': 'Oblicua', 'descripcion': 'Situación oblicua'},
            {'codigo': 'CARA', 'nombre': 'Cara', 'descripcion': 'Presentación de cara'},
            {'codigo': 'FRENTE', 'nombre': 'Frente', 'descripcion': 'Presentación de frente'},
        ]
        
        for i, item in enumerate(posiciones_fetales):
            obj, created = CatalogoPosicionFetal.objects.update_or_create(
                codigo=item['codigo'],
                defaults={'nombre': item['nombre'], 'descripcion': item['descripcion'], 'orden': i}
            )
            status = '✅ Creado' if created else '🔄 Actualizado'
            self.stdout.write(f"  {status}: Posición Fetal - {item['nombre']}")

        # =============================================
        # CATÁLOGO: ALTURA DE PRESENTACIÓN (Planos de Hodge)
        # =============================================
        alturas_presentacion = [
            {'codigo': 'LIBRE', 'nombre': 'Libre/Móvil', 'valor': '-4', 'descripcion': 'Por encima del estrecho superior'},
            {'codigo': 'INSINUADA', 'nombre': 'Insinuada', 'valor': '-3', 'descripcion': 'En el estrecho superior'},
            {'codigo': 'FIJA', 'nombre': 'Fija', 'valor': '-2', 'descripcion': 'Primer plano de Hodge'},
            {'codigo': 'ENCAJADA', 'nombre': 'Encajada', 'valor': '-1 a 0', 'descripcion': 'Segundo plano de Hodge'},
            {'codigo': 'PROFUNDA', 'nombre': 'Profundamente encajada', 'valor': '+1', 'descripcion': 'Tercer plano de Hodge'},
            {'codigo': 'MUY_PROFUNDA', 'nombre': 'Muy profunda', 'valor': '+2', 'descripcion': 'Cuarto plano de Hodge'},
            {'codigo': 'PERINEO', 'nombre': 'En periné', 'valor': '+3 a +4', 'descripcion': 'A nivel del periné'},
        ]
        
        for i, item in enumerate(alturas_presentacion):
            obj, created = CatalogoAlturaPresentacion.objects.update_or_create(
                codigo=item['codigo'],
                defaults={
                    'nombre': item['nombre'], 
                    'valor_numerico': item['valor'],
                    'descripcion': item['descripcion'], 
                    'orden': i
                }
            )
            status = '✅ Creado' if created else '🔄 Actualizado'
            self.stdout.write(f"  {status}: Altura Presentación - {item['nombre']}")

        # =============================================
        # CATÁLOGO: CARACTERÍSTICAS LÍQUIDO AMNIÓTICO
        # =============================================
        caracteristicas_liquido = [
            {'codigo': 'CLARO', 'nombre': 'Claro', 'descripcion': 'Líquido amniótico claro', 'patologico': False},
            {'codigo': 'CLARO_ESCASO', 'nombre': 'Claro Escaso', 'descripcion': 'Líquido claro en poca cantidad', 'patologico': False},
            {'codigo': 'CLARO_ABUNDANTE', 'nombre': 'Claro Abundante', 'descripcion': 'Líquido claro en abundante cantidad', 'patologico': False},
            {'codigo': 'MECONIAL_LEVE', 'nombre': 'Meconial Leve (+)', 'descripcion': 'Teñido de meconio leve', 'patologico': True},
            {'codigo': 'MECONIAL_MODERADO', 'nombre': 'Meconial Moderado (++)', 'descripcion': 'Teñido de meconio moderado', 'patologico': True},
            {'codigo': 'MECONIAL_ESPESO', 'nombre': 'Meconial Espeso (+++)', 'descripcion': 'Meconio espeso "puré de arvejas"', 'patologico': True},
            {'codigo': 'SANGUINOLENTO', 'nombre': 'Sanguinolento', 'descripcion': 'Teñido de sangre', 'patologico': True},
            {'codigo': 'PURULENTO', 'nombre': 'Purulento', 'descripcion': 'Aspecto purulento, infección', 'patologico': True},
            {'codigo': 'FETIDO', 'nombre': 'Fétido', 'descripcion': 'Mal olor, sospecha de infección', 'patologico': True},
            {'codigo': 'AUSENTE', 'nombre': 'Ausente/Anhidramnios', 'descripcion': 'Sin líquido amniótico', 'patologico': True},
        ]
        
        for i, item in enumerate(caracteristicas_liquido):
            obj, created = CatalogoCaracteristicasLiquido.objects.update_or_create(
                codigo=item['codigo'],
                defaults={
                    'nombre': item['nombre'], 
                    'descripcion': item['descripcion'], 
                    'es_patologico': item['patologico'],
                    'orden': i
                }
            )
            status = '✅ Creado' if created else '🔄 Actualizado'
            self.stdout.write(f"  {status}: Líquido Amniótico - {item['nombre']}")

        # =============================================
        # CATÁLOGO: RESULTADO CTG
        # =============================================
        resultados_ctg = [
            {'codigo': 'CATEGORIA_I', 'nombre': 'Categoría I (Normal)', 'descripcion': 'Trazado normal, no requiere intervención', 'accion': False},
            {'codigo': 'CATEGORIA_II', 'nombre': 'Categoría II (Indeterminado)', 'descripcion': 'Trazado indeterminado, requiere vigilancia', 'accion': True},
            {'codigo': 'CATEGORIA_III', 'nombre': 'Categoría III (Anormal)', 'descripcion': 'Trazado anormal, requiere intervención inmediata', 'accion': True},
            {'codigo': 'REACTIVO', 'nombre': 'Reactivo', 'descripcion': 'Test reactivo (NST)', 'accion': False},
            {'codigo': 'NO_REACTIVO', 'nombre': 'No Reactivo', 'descripcion': 'Test no reactivo (NST)', 'accion': True},
            {'codigo': 'SOSPECHOSO', 'nombre': 'Sospechoso', 'descripcion': 'Patrón sospechoso', 'accion': True},
            {'codigo': 'PATOLOGICO', 'nombre': 'Patológico', 'descripcion': 'Patrón patológico', 'accion': True},
        ]
        
        for i, item in enumerate(resultados_ctg):
            obj, created = CatalogoResultadoCTG.objects.update_or_create(
                codigo=item['codigo'],
                defaults={
                    'nombre': item['nombre'], 
                    'descripcion': item['descripcion'], 
                    'requiere_accion': item['accion'],
                    'orden': i
                }
            )
            status = '✅ Creado' if created else '🔄 Actualizado'
            self.stdout.write(f"  {status}: Resultado CTG - {item['nombre']}")

        # =============================================
        # CATÁLOGO: RESULTADO EXÁMENES
        # =============================================
        resultados_examen = [
            {'codigo': 'PENDIENTE', 'nombre': 'Pendiente', 'descripcion': 'Resultado pendiente'},
            {'codigo': 'NEGATIVO', 'nombre': 'Negativo', 'descripcion': 'Resultado negativo'},
            {'codigo': 'POSITIVO', 'nombre': 'Positivo', 'descripcion': 'Resultado positivo'},
            {'codigo': 'INDETERMINADO', 'nombre': 'Indeterminado', 'descripcion': 'Resultado indeterminado'},
            {'codigo': 'NO_REACTIVO', 'nombre': 'No Reactivo', 'descripcion': 'Resultado no reactivo'},
            {'codigo': 'REACTIVO', 'nombre': 'Reactivo', 'descripcion': 'Resultado reactivo'},
        ]
        
        for i, item in enumerate(resultados_examen):
            obj, created = CatalogoResultadoExamen.objects.update_or_create(
                codigo=item['codigo'],
                defaults={'nombre': item['nombre'], 'descripcion': item['descripcion'], 'orden': i}
            )
            status = '✅ Creado' if created else '🔄 Actualizado'
            self.stdout.write(f"  {status}: Resultado Examen - {item['nombre']}")

        # =============================================
        # CATÁLOGO: SALAS ASIGNADAS
        # =============================================
        salas = [
            {'codigo': 'SALA_1', 'nombre': 'Sala 1', 'tipo': 'Parto', 'capacidad': 1},
            {'codigo': 'SALA_2', 'nombre': 'Sala 2', 'tipo': 'Parto', 'capacidad': 1},
            {'codigo': 'SALA_3', 'nombre': 'Sala 3', 'tipo': 'Parto', 'capacidad': 1},
            {'codigo': 'SALA_4', 'nombre': 'Sala 4', 'tipo': 'Parto', 'capacidad': 1},
            {'codigo': 'PABELLON_1', 'nombre': 'Pabellón 1', 'tipo': 'Quirófano', 'capacidad': 1},
            {'codigo': 'PABELLON_2', 'nombre': 'Pabellón 2', 'tipo': 'Quirófano', 'capacidad': 1},
            {'codigo': 'URGENCIAS', 'nombre': 'Box Urgencias', 'tipo': 'Urgencias', 'capacidad': 2},
            {'codigo': 'PREPARTOS', 'nombre': 'Prepartos', 'tipo': 'Preparación', 'capacidad': 4},
        ]
        
        for item in salas:
            obj, created = CatalogoSalaAsignada.objects.update_or_create(
                codigo=item['codigo'],
                defaults={'nombre': item['nombre'], 'tipo': item['tipo'], 'capacidad': item['capacidad']}
            )
            status = '✅ Creado' if created else '🔄 Actualizado'
            self.stdout.write(f"  {status}: Sala - {item['nombre']}")

        self.stdout.write(self.style.SUCCESS('\n✅ Catálogos de Ingreso a Parto cargados exitosamente!'))
